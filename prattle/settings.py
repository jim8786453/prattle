# -*- coding: utf-8 -*-

import os

from prattle import logs


# Create a logger
logger = logs.get_logger(__name__)


# Eve Database settings
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.environ.get('MONGO_PORT', 27017))
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', '')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', '')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'prattle')
MONGO_QUERY_BLACKLIST = ['$where']


# Eve cache settings
CACHE_CONTROL = 'no-cache'
CACHE_EXPIRES = 0


# Eve general settings
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
ITEM_METHODS = []
PAGINATION_DEFAULT = 10
RESOURCE_METHODS = []
SOFT_DELETE = True
VERSIONING = True
RENDERERS = ['eve.render.JSONRenderer']
X_DOMAINS = ['*']
X_HEADERS = ['Content-type', 'If-Match']


# Eve change logging
OPLOG = True
OPLOG_ENDPOINT = 'history'
OPLOG_RETURN_EXTRA_FIELD = True


# Schema
DOMAIN = {
    'conversations': {
        'url': 'conversations',
        'resource_methods': ['GET', 'POST'],
        'item_methods': ['GET'],
        'item_title': 'Conversations',
        'description': 'Conversations between users',
        'schema': {
            'participants': {
                'type': 'list',
                'required': True,
                'schema': {
                    'type': 'string'
                }
            },
        }
    },
    'messages': {
        'url': 'conversations/<regex("(?s).*"):conversation>/messages',
        'resource_methods': ['POST'],
        'item_methods': [],
        'item_title': 'Messages',
        'description': 'Messages between users',
        'schema': {
            'conversation': {
                'type': 'objectid',
                'required': True,
                'data_relation': {
                    'resource': 'conversations',
                    'embeddable': True
                },
            },
            'from': {
                'type': 'string',
                'required': True
            },
            'text': {
                'type': 'string',
                'required': True
            }
        }
    },
}
