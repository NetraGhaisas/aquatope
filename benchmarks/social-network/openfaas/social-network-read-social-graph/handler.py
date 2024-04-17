import random
import sys
import os
import json
from datetime import datetime, timezone

from pymongo import MongoClient
from urllib.parse import quote_plus

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
    user_id = args.get('user_id', random.randint(1, 962))
    post_id = args.get('post_id', random.randint(1, sys.maxsize))
    post_timestamp = args.get('post_timestamp', get_timestamp_ms())
    user_mention_names = args.get('user_mention_names', list())
    # mongo_config = args.get('mongo_config', dict())
    # mongodb_addr = mongo_config.get('mongodb_addr',
    #                                 'mongodb.default.svc.cluster.local')
    # mongodb_port = mongo_config.get('mongodb_port', 27017)

    # --------------------------------------------------------------------------
    # Function
    # --------------------------------------------------------------------------
    if mongo_client is None:
        uri = get_uri()
        mongo_client = MongoClient(uri)

    social_network_db = mongo_client['social_network']
    user_collection = social_network_db['user']
    social_graph_collection = social_network_db['social_graph']

    home_timeline_ids = list()
    # mentioned users
    for user_mention_name in user_mention_names:
        doc = user_collection.find_one(filter={'username': user_mention_name})
        if doc is None:
            continue
        user_mention_id = doc['user_id']
        home_timeline_ids.append(user_mention_id)
    # followers
    cursor = social_graph_collection.find(filter={'followees': user_id})
    for doc in cursor:
        follower_id = doc['user_id']
        home_timeline_ids.append(follower_id)

    # --------------------------------------------------------------------------
    # Return result
    # --------------------------------------------------------------------------
    return json.dumps({
        'post_id': post_id,
        'post_timestamp': post_timestamp,
        'home_timeline_ids': home_timeline_ids
    })
