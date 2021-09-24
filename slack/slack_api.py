import requests

class SlackAPI:
    END_POINT = 'https://slack.com/api/'

    def __init__(self, token):
        self._headers = {
            'Authorization': 'Bearer ' + token,
        }

    def send_message(self, channel, text):
        data = {
            "channel": channel,
            "text": text
        }

        res = requests.post(self.END_POINT + 'chat.postMessage',
                            headers=self._headers,
                            data=data)
        print("return ", res.json())


