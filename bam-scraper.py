import store
import twitter
import instagram
import discord_service

from datetime import datetime

def main():
    s = store.Store()
    s.init()
    tw = twitter.Twitter()
    insta = instagram.Instagram()
    ds = discord_service.DiscordService()

    for publisher_name in s.get_publishers():
        p = s.get_publisher(publisher_name)
        if not p.channel:
            continue
        for service in p.services:
            posts = None
            if service.name == 'twitter':
                posts, new_state = tw.get_new_posts(service.username, service.state)
            if service.name == 'instagram':
                posts, new_state = insta.get_new_posts(service.username, service.state)
            if posts is not None:
                print(publisher_name + ' ' + service.name + ', ' + str(len(posts)) + ' new posts.')
                s.update_state(p.name, service.name, new_state)
                for post in posts:
                    ds.send(p.channel, post)

if __name__ == '__main__':
    main()
