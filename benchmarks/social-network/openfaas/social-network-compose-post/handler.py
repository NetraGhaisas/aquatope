import json
import random
import re
import sys
from datetime import datetime, timezone


def get_timestamp_ms() -> int:
    return int(round(datetime.now(timezone.utc).timestamp() * 1000))


def handle(args):
    # --------------------------------------------------------------------------
    # Parse args
    # --------------------------------------------------------------------------
    req = json.loads(args)
    username = req.get('username', 'username_1')
    user_id = req.get('user_id', 1)
    text = req.get('text', 'Forge ahead till the end we pray.')
    media_ids = req.get('media_ids', [random.randint(1, sys.maxsize)])
    media_types = req.get('media_types', ['png'])
    post_type = req.get('post_type', 'POST')
    mongo_config = req.get('mongo_config', {
        'mongodb_addr': 'mongodb.default.svc.cluster.local',
        'mongodb_port': 27017
    })
    # --------------------------------------------------------------------------
    # Function
    # --------------------------------------------------------------------------
    # construct post
    post_timestamp = get_timestamp_ms()
    post_id = random.getrandbits(63)
    author = {
        'user_id': user_id,
        'username': username
    }
    medias = list()
    for i in range(len(media_ids)):
        medias.append({
            'media_id': media_ids[i],
            'media_type': media_types[i]
        })
    post = {
        'post_id': post_id,
        'author': author,
        'text': text,
        'medias': medias,
        'timestamp': post_timestamp,
        'post_type': post_type
    }

    # parse user mentions
    user_mention_names = [username[1:]
                          for username in re.findall('@[a-zA-Z0-9-_]+', text)]

    # --------------------------------------------------------------------------
    # Return result
    # --------------------------------------------------------------------------
    return json.dumps({
        # Store Post
        'post': post,
        # Read social graph
        'user_id': user_id,
        'post_id': post_id,
        'post_timestamp': post_timestamp,
        'user_mention_names': user_mention_names,
        # Common
        'mongo_config': mongo_config
    })
