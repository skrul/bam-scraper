import requests
from discord import Webhook, RequestsWebhookAdapter, Embed
import json

class DiscordService:
    def __init__(self):
        with open('webhooks.json') as f:
            self.webhooks = json.load(f)

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
        webhook = Webhook.from_url(self.webhooks[channel], adapter=RequestsWebhookAdapter())
        webhook.send(embed=e)
