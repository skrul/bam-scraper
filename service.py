class Service:
    def __init__(self, name, username, state):
        self.name = name
        self.username = username
        self.state = state

    def __repr__(self):
        a = [
            'name: ' + self.name,
            'username: ' + self.username,
            'state: ' + str(self.state),
        ]
        return ', '.join(a)
