import requests

import settings

class SlackAPI:
    END_POINT = 'https://slack.com/api/'

    def __init__(self):
        self._headers = {
            'Authorization': 'Bearer ' + settings.SLACK_API_TOKEN,
        }

    def send_message(self, channel, text):
        data = {
            "channel": channel,
            "text": text
        }

        res = requests.post(self.END_POINT + 'chat.postMessage',
                            headers=self._headers,
                            data=data)
        print("SlackAPI send_message return ", res.json())


