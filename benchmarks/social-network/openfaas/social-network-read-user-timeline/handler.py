import json
import os
import random
from urllib.parse import quote_plus

from pymongo import MongoClient

mongo_client = None

def get_uri():
    password=""
    with open("/var/openfaas/secrets/mongo-db-password") as f:
        password = f.read()

    return "mongodb://%s:%s@%s" % (
    quote_plus("root"), quote_plus(password), os.getenv("mongo_host"))


def handle(req):
    global mongo_client

    # --------------------------------------------------------------------------
    # Parse args
    # --------------------------------------------------------------------------
    args = json.loads(req)
    user_id = args.get('user_id', random.randint(1, 962))
    start = args.get('start', 0)
    stop = args.get('stop', 10)
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
    user_timeline_collection = social_network_db['user_timeline']
    user_timeline = user_timeline_collection.find_one(
        filter={'user_id': user_id})
    post_ids = list()
    if user_timeline is not None:
        for post in user_timeline['posts']:
            post_ids.append(post['post_id'])
        if 0 <= start and start < stop:
            post_ids = post_ids[start:stop]

    # --------------------------------------------------------------------------
    # Return result
    # --------------------------------------------------------------------------
    return json.dumps({'post_ids': post_ids})
