import json
import os

from eve.tests import TestMinimal
from pymongo import MongoClient

import prattle

from prattle.settings import MONGO_HOST, MONGO_PORT, MONGO_DBNAME


class TestPrattle(TestMinimal):

    def setUp(self):
        self.this_directory = os.path.dirname(os.path.realpath(__file__))
        self.settings_file = os.path.join(self.this_directory,
                                     '../../settings.py')
        self.connection = None
        self.setupDB()
        self.app = prattle.create_app()
        self.test_client = self.app.test_client()
        self.domain = self.app.config['DOMAIN']

    def setupDB(self):
        self.connection = MongoClient(MONGO_HOST, MONGO_PORT)
        self.connection.drop_database(MONGO_DBNAME)

    def dropDB(self):
        self.connection = MongoClient(MONGO_HOST, MONGO_PORT)
        self.connection.drop_database(MONGO_DBNAME)
        self.connection.close()

    def get(self, url, headers=None, content_type='application/json'):
        if headers is None:
            headers = []
        headers.append(('Content-Type', content_type))
        r = self.test_client.get(url, headers=headers)
        return self.parse_response(r)

    def test_swagger(self):
        r = self.get('api-docs')
        self.assertEqual(r[1], 200)

    def test_conversations(self):
        # Check no data exists.
        r = self.get('conversations')
        self.assertEqual(r[1], 200)
        result = r[0]
        self.assertEqual(result['_meta']['total'], 0)

        # Create a conversation.
        data = {
            'participants': ['foo', 'bar']
        }
        r = self.post('conversations', data=data)
        self.assertEqual(r[1], 201)
        conversation_id = r[0]['_id']

        # Check conversation exists.
        r = self.get('conversations')
        self.assertEqual(r[1], 200)
        result = r[0]
        self.assertEqual(result['_meta']['total'], 1)

        # Now fetch an individual conversation.
        id_ = result['_items'][0]['_id']
        r = self.get('conversations/%s' % id_)
        self.assertEqual(r[1], 200)
        result = r[0]
        
        # Check we have two participants.
        self.assertEqual(len(result['participants']), 2)

    def test_messages(self):
        # Create a conversation.
        data = {
            'participants': ['foo', 'bar']
        }
        r = self.post('conversations', data=data)
        self.assertEqual(r[1], 201)
        conversation_id = r[0]['_id']

        # Invalid message.
        data = {
            'from': 'baz',
            'text': 'test'
        }
        r = self.post('conversations/%s/messages' % conversation_id, data=data)
        self.assertEqual(r[1], 401)
        
        # Create a message.
        data = {
            'from': 'foo',
            'text': 'test'
        }
        r = self.post('conversations/%s/messages' % conversation_id, data=data)
        self.assertEqual(r[1], 201)

        # Check message is returned with conversation.
        r = self.get('conversations/%s' % conversation_id)
        self.assertEqual(r[1], 200)
        result = r[0]
        self.assertEqual(len(result['messages']), 1)
