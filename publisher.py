class Publisher:
    def __init__(self, row, name, channel, services):
        self.row = row
        self.name = name
        self.channel = channel
        self.services = services

    def __repr__(self):
        a = [
            'row: ' + str(self.row),
            'name: ' + self.name,
            'channel: ' + self.channel,
            'services: [' + ', '.join(str(s) for s in self.services) + ']'
        ]
        return ', '.join(a)
