import datetime

import requests

import settings


class GitHubAPI:
    END_POINT = 'https://api.github.com/graphql'

    def __init__(self):
        self._headers = {
            'Authorization': 'bearer ' + settings.GITHUB_ACCESS_TOKEN
        }

    def post(self, query, variables):
        res = requests.post(
            self.END_POINT,
            headers=self._headers,
            json={
                'query': query,
                'variables': variables
            },
        )
        if res.status_code != 200:
            raise Exception('fail : {}'.format(res.status_code))

        print("GitHubAPI post return ", res.json())

        return res
