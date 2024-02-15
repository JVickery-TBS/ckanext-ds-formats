from ckan.plugins.toolkit import get_action, g


def get_ds_dump_formats():
    return get_action('get_ds_dump_formats')({'user': g.user},{})
