# -*- coding: utf-8 -*-

import os

from eve import Eve
from eve_swagger import swagger, add_documentation

from prattle import hooks
from prattle import settings


_MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
_SETTINGS_PATH = os.path.join(_MODULE_PATH, 'settings.py')


def create_app():
    # Create the Eve app.
    app = Eve(settings=_SETTINGS_PATH)

    # Hooks
    app.on_fetched_item_conversations += hooks.on_fetched_item_conversations
    app.on_insert_messages += hooks.on_insert_messages

    # Register Swagger extension.
    app.register_blueprint(swagger)
    app.config['SWAGGER_INFO'] = {
        'title': 'prattle',
        'version': '0.0.1',
        'description': 'Demo backend messaging api',
        'contact': {
            'name': 'jim8786453@gmail.com',
        },
        'schemes': ['http', 'https'],
    }

    return app


app = create_app()
