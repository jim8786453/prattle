 # -*- coding: utf-8 -*-
 
import pymongo

from flask import current_app as app, abort, request

def on_fetched_item_conversations(response):
    """Add messages into the conversation's response.

    """
    conversation_id = response['_id']
    collection = app.data.driver.db['messages']
    response['messages'] = list(
        message for message in collection
        .find({'conversation': conversation_id})
        .sort([("_created", pymongo.ASCENDING)]))


def on_insert_messages(items):
    """Validate the user is a participant in the conversation.

    """
    # Fetch all referenced conversations.
    collection = app.data.driver.db['conversations']
    conversations = list(collection.find({
        '_id': {
            '$in': [item['conversation'] for item in items]
        }}))
    # Check from value is valid for each conversation.
    for item in items:
        from_ = item['from']
        conversation = [c for c in conversations
                        if c['_id'] == item['conversation']][0]
        if from_ not in conversation['participants']:
            abort(401, "From is not a valid particpant")
