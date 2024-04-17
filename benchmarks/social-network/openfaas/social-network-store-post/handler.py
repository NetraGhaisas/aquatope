import json
import os
import random
import string
import sys
from datetime import datetime, timezone
from urllib.parse import quote_plus

from pymongo import MongoClient

mongo_client = None

def get_uri():
    password=""
    with open("/var/openfaas/secrets/mongo-db-password") as f:
        password = f.read()

    return "mongodb://%s:%s@%s" % (
    quote_plus("root"), quote_plus(password), os.getenv("mongo_host"))


def get_timestamp_ms() -> int:
    return int(round(datetime.now(timezone.utc).timestamp() * 1000))


def handle(req):
    global mongo_client

    # --------------------------------------------------------------------------
    # Parse args
    # --------------------------------------------------------------------------
    args = json.loads(req)
    post = args.get('post', None)
    if post is None:
        user_id = random.randint(1, 962)
        post_id = random.randint(1, sys.maxsize)
        text = ''.join(random.choices(
            string.ascii_letters + string.digits, k=100))
        num_user_mentions = random.randint(0, 3)
        user_mention_ids = list()
        timestamp = get_timestamp_ms()
        for _ in range(num_user_mentions):
            while True:
                user_mention_id = random.randint(1, 962)
                if (user_mention_id != user_id and
                        user_mention_id not in user_mention_ids):
                    user_mention_ids.append(user_mention_id)
                    break
        for user_mention_id in user_mention_ids:
            text = text + ' @username_' + str(user_mention_id)
        num_medias = random.randint(0, 5)
        medias = list()
        for _ in range(num_medias):
            medias.append({
                'media_id': random.randint(1, sys.maxsize),
                'media_type': 'png'
            })
        post = {
            'post_id': post_id,
            'author': {
                'user_id': user_id,
                'username': 'username_' + str(user_id)
            },
            'text': text,
            'medias': medias,
            'timestamp': timestamp,
            'post_type': 'POST'
        }
    # mongo_config = args.get('mongo_config', dict())
    # mongodb_addr = mongo_config.get('mongodb_addr',
    #                                 'mongodb.faas.svc.cluster.local')
    # mongodb_port = mongo_config.get('mongodb_port', 27017)

    # --------------------------------------------------------------------------
    # Function
    # --------------------------------------------------------------------------
    if mongo_client is None:
        uri = get_uri()
        mongo_client = MongoClient(uri)

    social_network_db = mongo_client['social_network']
    post_collection = social_network_db['post']
    post_collection.create_index('post_id', unique=True)
    res = post_collection.insert_one(post)

    # --------------------------------------------------------------------------
    # Return result
    # --------------------------------------------------------------------------
    return json.dumps({'post_inserted_id': str(res.inserted_id)})
