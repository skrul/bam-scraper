class Post:
    def __init__(self, title, title_url, author, author_url, body, image_url, footer, ts):
        self.title = title
        self.title_url = title_url
        self.author = author
        self.author_url = author_url
        self.body = body
        self.image_url = image_url
        self.footer = footer
        self.ts = ts

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
