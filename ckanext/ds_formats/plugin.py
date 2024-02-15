from flask import Blueprint

import ckan.plugins as plugins

from ckanext.ds_formats.blueprint import datastore_formats
from ckanext.ds_formats import actions, auth, helpers


class DSFormatsPlugin(plugins.SingletonPlugin):
    """
    Plugin for extending the DataStore Dump blueprint.
    """
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.ITemplateHelpers)

    # IBlueprint

    def get_blueprint(self):
        # type: () -> list[Blueprint]
        return [datastore_formats]

    # IConfigurer

    def update_config(self, config):
        plugins.toolkit.add_template_directory(config, 'templates')

    # IActions

    def get_actions(self):
        # type: () -> dict[str, callable]
        return {'get_ds_dump_formats': actions.get_ds_dump_formats,}

    # IAuthFunctions

    def get_auth_functions(self):
        # type: () -> dict[str, callable]
        return {'get_ds_dump_formats': auth.get_ds_dump_formats,}

    # ITemplateHelpers

    def get_helpers(self):
        return {'get_ds_dump_formats': helpers.get_ds_dump_formats,}


