from io import StringIO

BOM = "\N{bom}"

class FormatBase(object):

    format = None
    file_extension = None
    content_type = None
    charset = 'utf-8'
    ds_record_format = 'objects'
    bom = None

    def get_content_type(self):
        # type: () -> bytes
        return str.encode(self.content_type) \
            + b'; charset=%s' % str.encode(self.charset)

    def get_content_disposition(self, resource_id):
        # type: (str) -> str
        return 'attachment; filename="%s.%s"' % (resource_id,
                                                 self.file_extension)

    def writer_factory(self, fields, bom=False):
        # type: (dict[str, any], bool) -> bytes
        pass


class SHP(FormatBase):

    format = 'shp'
    file_extension = 'shp'
    content_type = 'x-gis/x-shapefile'

    def writer_factory(self, fields, bom=False):
        # type: (dict[str, any], bool) -> bytes
        output = StringIO()

        if bom:
            output.write(BOM)


class GeoJSON(FormatBase):

    format = 'geojson'
    file_extension = 'geojson'
    content_type = 'application/geo+json'

    def writer_factory(self, fields, bom=False):
        # type: (dict[str, any], bool) -> bytes
        output = StringIO()

        if bom:
            output.write(BOM)


class GPKG(FormatBase):

    format = 'gpkg'
    file_extension = 'gpkg'
    content_type = 'application/geopackage+sqlite3'

    def writer_factory(self, fields, bom=False):
        # type: (dict[str, any], bool) -> bytes
        output = StringIO()

        if bom:
            output.write(BOM)
