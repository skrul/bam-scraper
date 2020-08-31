import twitterscraper
import datetime
from post import Post
import tweepy
import pprint
import json

class Twitter:
    def __init__(self):
        with open('twitter_credentials.json') as f:
            conf = json.load(f)
        auth = tweepy.OAuthHandler(conf['consumer_key'], conf['consumer_secret'])
        auth.set_access_token(conf['access_token'], conf['access_token_secret'])
        self.api = tweepy.API(auth)

    def get_new_posts(self, username, state):
        last_id = None
        if state is not None:
            last_id = state.get('last_id')

        if last_id is None:
            tweets = self.api.user_timeline(
                screen_name=username,
                count=1,
                tweet_mode='extended'
            )
        else:
            tweets = self.api.user_timeline(
                screen_name=username,
                since_id=last_id,
                tweet_mode='extended')

        posts = []
        max_id = None
        for tweet in tweets:
            tweet_url = 'https://twitter.com/' + tweet.user.screen_name + '/status/' + tweet.id_str
            media = tweet.entities.get('media')
            if media is not None and len(media) > 0:
                image_url = media[0]['media_url_https']
            else:
                image_url = None
            post = Post(
                tweet_url,
                tweet_url,
                tweet.user.name + ' (@' + tweet.user.screen_name + ')',
                'https://twitter.com/' + tweet.user.screen_name,
                tweet.full_text,
                image_url,
                'via twitter',
                tweet.created_at
            )
            posts.append(post)
            if max_id is None or tweet.id > max_id:
                max_id = tweet.id

        if max_id is not None:
            state = { 'last_id': max_id }

        return posts, state
