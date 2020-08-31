import requests
from discord import Webhook, RequestsWebhookAdapter, Embed

WEBHOOKS = {
    'venue-social': 'https://discordapp.com/api/webhooks/749459816040104036/2IcOzu_y-6ApZAz2p6zk8cARBoA6Oy4IyTMzIIiHbsVvhYVDR8pb5brFtl4Z6voDhoYD'
}

class DiscordService:
    def __init__(self):
        pass

    def send(self, channel, post):
        e = Embed(
            title=post.title,
            type='rich',
            description=post.body,
            url=post.title_url,
            timestamp=post.ts
        )
        if post.image_url is not None:
            e.set_image(url=post.image_url)
        e.set_footer(text=post.footer)
        e.set_author(name=post.author, url=post.author_url)
        webhook = Webhook.from_url(WEBHOOKS[channel], adapter=RequestsWebhookAdapter())
        webhook.send(embed=e)
