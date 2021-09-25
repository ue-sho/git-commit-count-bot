import datetime

import pytz
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
        return res


    def iso_to_jstdt(self, iso_str):
        dt = None
        try:
            dt = datetime.datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%SZ')
            dt = pytz.utc.localize(dt).astimezone(pytz.timezone('Asia/Tokyo'))
        except ValueError:
            try:
                dt = datetime.datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%S.%f%z')
                dt = dt.astimezone(pytz.timezone('Asia/Tokyo'))
            except ValueError:
                pass
        return dt


    def commit_count(self, day=0):
        commit_count = 0

        res = requests.get('https://api.github.com/users/ue-sho/events')
        json_data = res.json()
        for data in json_data:
            if data['type'] != 'PushEvent':
                continue

            dt = iso_to_jstdt(data['created_at'])
            now = datetime.datetime.now()
            yesterday = now - datetime.timedelta(days=day)
            if dt.strftime('%Y/%m/%d') != yesterday.strftime('%Y/%m/%d'):
                continue

            comit_list = data['payload']['commits']
            commit_count += len(comit_list)
            print('commit数は : ', commit_count)
        return commit_count


