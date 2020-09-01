from datetime import datetime

from google_api import auth
from publisher import Publisher
from service import Service
import json

SPREADSHEET_ID = '1dB1-9hemkvRv-jMDqWiUUlPQkAN6TwVE9d6FzO1sWu4'

class Store:
    def __init__(self):
        self.data = None
        self.service_state_col = None

    def init(self):
        self.sheets_service = auth('sheets', 'v4')
        self._read()

    def get_publishers(self):
        return self.data.keys()

    def get_publisher(self, name):
        return self.data[name]

    def _read(self):
        result = self.sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range='data').execute()
        values = result.get('values')
        data = {}
        first_row = None
        for row, value in enumerate(values):
            if first_row is None:
                first_row = value
                self.service_state_col = {}
                for i in range(2, len(first_row), 2):
                    self.service_state_col[value[i]] = chr(ord('@') + i + 2)
                continue
            value.extend([None] * (len(first_row) - len(value)))
            services = []
            for i in range(2, len(first_row), 2):
                if not value[i]:
                    continue
                try:
                    state = json.loads(value[i + 1])
                except:
                    state = None
                services.append(Service(first_row[i], value[i], state))
            p = Publisher(row + 1, value[0], value[1], services)
            data[p.name] = p
        self.data = data

    def update_state(self, name, service, state):
        p = self.data[name]

        updated_json = json.dumps(state)
        original_json = None
        for s in p.services:
            if s.name == service:
                original_json = json.dumps(s.state)

        if updated_json == original_json:
            return

        body = {
            'values' : [[updated_json]]
            }
        range = self.service_state_col[service] + str(p.row)
        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range=range, valueInputOption='RAW',
            body=body).execute()
        services = []
        for s in p.services:
            if s.name == service:
                services.append(Service(service, s.username, state))
            else:
                services.append(s)
        self.data[p.name] = Publisher(p.row, p.name, p.channel, services)
