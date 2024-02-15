from flask import Blueprint, Response
from logging import getLogger

import ckan.lib.navl.dictization_functions as dict_fns

from ckan.plugins.toolkit import (
    request,
    get_validator,
    abort,
    _,
    ObjectNotFound,
    NotAuthorized,
    get_action,
    g,
)
from ckanext.datastore.blueprint import (
    DUMP_FORMATS,
    PAGINATE_BY,
    dump,
    dump_schema,
)
from ckanext.ds_formats.formats import FormatBase


one_of = get_validator('one_of')

datastore_formats = Blueprint(u'datastore_formats', __name__)
log = getLogger(__name__)


def dump_more_formats_schema(more_formats):
    # type: (list[FormatBase]) -> dict[str, list]
    schema = dump_schema()
    schema['format'] = [one_of(DUMP_FORMATS +
                               tuple([f.format for f in more_formats]))]
    return schema


@datastore_formats.route('/datastore/dump/<resource_id>')
def dump_more_formats(resource_id):
    args = request.args.to_dict()
    if args.get('format', 'csv') in DUMP_FORMATS:
        return dump(resource_id)

    try:
        more_formats = get_action('get_ds_dump_formats')({'user': g.user},{})
    except NotAuthorized:
        abort(400, _('Unsupported format %s') % fmt)

    data, errors = dict_fns.validate(request.args.to_dict(),
                                     dump_more_formats_schema(more_formats))
    if errors:
        abort(
            400, '\n'.join(
                '{0}: {1}'.format(k, ' '.join(e)) for k, e in errors.items()
            )
        )

    fmt = data['format']
    offset = data['offset']
    limit = data.get('limit')
    options = {'bom': data['bom']}
    sort = data['sort']
    search_params = {
        k: v
        for k, v in data.items()
        if k in [
            'filters', 'q', 'distinct', 'plain', 'language',
            'fields'
        ]
    }

    user_context = g.user

    format_class = None

    for i, f in enumerate(more_formats):
        if fmt == f.format:
            format_class = more_formats[i]
            break

    if not format_class:
        abort(400, _('Unsupported format %s') % fmt)

    headers = {
        'Content-Type':
            format_class.get_content_type(),
        'Content-disposition':
            format_class.get_content_disposition(resource_id),
    }

    try:
        return Response(dump_to(resource_id,
                                fmt=fmt,
                                offset=offset,
                                limit=limit,
                                options=options,
                                sort=sort,
                                search_params=search_params,
                                user=user_context,
                                more_formats=more_formats),
                        mimetype='application/octet-stream',
                        headers=headers)
    except ObjectNotFound:
        abort(404, _('DataStore resource not found'))


def dump_to(
    resource_id, fmt, offset, limit, options,
    sort, search_params, user, more_formats
):

    format_class = None

    for i, f in enumerate(more_formats):
        if fmt == f.format:
            format_class = more_formats[i]
            break

    if not format_class:
        assert False, 'Unsupported format'

    bom = options.get('bom', False)

    def start_stream_writer(fields):
        return format_class.writer_factory(fields, bom=bom)

    def stream_result_page(offs, lim):
        return get_action('datastore_search')(
            {'user': user},
            dict({
                'resource_id': resource_id,
                'limit': PAGINATE_BY
                if limit is None else min(PAGINATE_BY, lim),  # type: ignore
                'offset': offs,
                'sort': sort,
                'records_format': format_class.ds_record_format,
                'include_total': False,
            }, **search_params)
        )

    def stream_dump(offset, limit, paginate_by, result):
        with start_stream_writer(result['fields']) as writer:
            while True:
                if limit is not None and limit <= 0:
                    break

                records = result['records']

                yield writer.write_records(records)

                if format_class.ds_record_format == 'objects' \
                        or format_class.ds_record_format == 'lists':
                    if len(records) < paginate_by:
                        break
                elif not records:
                    break

                offset += paginate_by
                if limit is not None:
                    limit -= paginate_by
                    if limit <= 0:
                        break

                result = stream_result_page(offset, limit)

            yield writer.end_file()

    result = stream_result_page(offset, limit)

    if result['limit'] != limit:
        # `limit` (from PAGINATE_BY) must have been more than
        # ckan.datastore.search.rows_max, so datastore_search responded
        # with a limit matching ckan.datastore.search.rows_max.
        # So we need to paginate by that amount instead, otherwise
        # we'll have gaps in the records.
        paginate_by = result['limit']
    else:
        paginate_by = PAGINATE_BY

    return stream_dump(offset, limit, paginate_by, result)
