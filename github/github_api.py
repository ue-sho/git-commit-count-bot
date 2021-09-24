import datetime

import pytz
import requests

import settings


END_POINT = 'https://api.github.com/graphql'


def post(query):
    headers = {"Authorization": "bearer " + settings.GITHUB_ACCESS_TOKEN}
    res = requests.post(END_POINT, json=query, headers=headers)
    if res.status_code != 200:
        raise Exception("fail : {}".format(res.status_code))
    return res


def query():
    # query
    query={ 'query' : """
      query {
        search(query: "language:python stars:>=1000 sort:stars", type: REPOSITORY, first: 10) {
          edges {
            node {
              ... on Repository {
                nameWithOwner
                url
                createdAt
                description
                stargazers{
                  totalCount
                }
              }
            }
          }
        }
      }
      """
    }

    res = post(query)
    print(res.json())


def iso_to_jstdt(iso_str):
    dt = None
    try:
        dt = datetime.datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%SZ')
        dt = pytz.utc.localize(dt).astimezone(pytz.timezone("Asia/Tokyo"))
    except ValueError:
        try:
            dt = datetime.datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%S.%f%z')
            dt = dt.astimezone(pytz.timezone("Asia/Tokyo"))
        except ValueError:
            pass
    return dt


def commit_count(day=0):
    commit_count = 0

    res = requests.get('https://api.github.com/users/ue-sho/events')
    json_data = res.json()
    for data in json_data:
        if data["type"] != "PushEvent":
            continue

        dt = iso_to_jstdt(data["created_at"])
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=day)
        if dt.strftime('%Y/%m/%d') != yesterday.strftime('%Y/%m/%d'):
            continue

        comit_list = data["payload"]["commits"]
        commit_count += len(comit_list)
        print("commit数は : ", commit_count)
    return commit_count
