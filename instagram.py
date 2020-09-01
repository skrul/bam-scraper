import hashlib
import string
import random
import pprint
import json
from post import Post
from datetime import datetime

from instagram_web_api import Client

class MyClient(Client):
    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = ''.join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode()).hexdigest()

class Instagram:
    def __init__(self):
        self.web_api = MyClient(auto_patch=True, drop_incompat_keys=False)

    def get_new_posts(self, username, state):
        count = 1
        last_ts = 0
        if state is not None:
            last_ts = state.get('last_ts', 0)
            count = 10
        user_info = self.web_api.user_info2(username)
        user_id = user_info['id']
        full_name = user_info['full_name']
        user_feed_info = self.web_api.user_feed(user_id, count=count)
        created_ms_max = None
        posts = []
        for node in user_feed_info:
            post_url = node['node']['link']
            created_ms = int(node['node']['created_time'])
            if created_ms > last_ts:
                post = Post(
                    post_url,
                    post_url,
                    full_name + ' (@' + username + ')',
                    'https://instagram.com/' + username,
                    node['node']['caption']['text'],
                    node['node']['display_url'],
                    'via instagram',
                    datetime.fromtimestamp(created_ms)
                )
                posts.append(post)
            if created_ms_max is None or created_ms > created_ms_max:
                created_ms_max = created_ms

        if created_ms_max is not None:
            state = { 'last_ts': created_ms_max }
        return posts, state

if __name__ == '__main__':
    instagram = Instagram()
    print(instagram.get_new_posts('cafedunord', None))
