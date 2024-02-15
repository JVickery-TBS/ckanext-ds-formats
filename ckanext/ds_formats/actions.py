from ckan.plugins.toolkit import check_access

from ckanext.ds_formats import formats


def get_ds_dump_formats(context, data_dict):
    # type: (dict[str, any], dict[str, any]) -> list[formats.FormatBase]
    check_access('get_ds_dump_formats', context, data_dict)
    return [
        formats.SHP(),
        formats.GeoJSON(),
        formats.GPKG(),
    ]
