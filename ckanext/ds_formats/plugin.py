from flask import Blueprint

import ckan.plugins as plugins

from ckanext.ds_formats.blueprint import datastore_formats
from ckanext.ds_formats import actions, auth


class DSFormatsPlugin(plugins.SingletonPlugin):
    """
    Plugin for extending the DataStore Dump blueprint.
    """
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)

    # IBlueprint

    def get_blueprint(self):
        # type: () -> list[Blueprint]
        return [datastore_formats]

    # IActions

    def get_actions(self):
        # type: () -> dict[str, callable]
        return {'get_ds_dump_formats': actions.get_ds_dump_formats,}

    # IAuthFunctions

    def get_auth_functions(self):
        # type: () -> dict[str, callable]
        return {'get_ds_dump_formats': auth.get_ds_dump_formats,}


