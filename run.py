import json
import datetime

import requests
import schedule

from slack.slack_api import SlackAPI
from github.github_api import GitHubAPI


def get_commit_count(user_name, dt_from, dt_to):
    # query
    contributions_query = """
        query (
            $name: String!,
            $from: DateTime!,
            $to: DateTime!
        ) {
            user(login: $name) {
                name
                contributionsCollection(from: $from, to: $to) {
                    totalRepositoryContributions
                    totalCommitContributions
                    commitContributionsByRepository {
                        repository {
                            nameWithOwner
                        }
                        contributions {
                            totalCount
                        }
                    }
                }
            }
        }
    """
    variables = {
        "name": user_name,
        "from": dt_from,
        "to": dt_to
    }

    github = GitHubAPI()
    res = github.post(contributions_query, variables)
    return res.json()


def every_day_at_0am_task():  # slackに送信
    now = datetime.datetime.now()
    yesterday = now + datetime.timedelta(days=-1)

    user_name = "ue-sho"
    dt_from = str(yesterday.isoformat())
    dt_to = str(now.isoformat())

    print("from {} to {} ".format(dt_from, dt_to))


    res = get_commit_count(user_name, dt_from, dt_to)
    slack_text = "{}さんの{}のコミット数は {} です。".format(
        res['data']['user']['name'],
        yesterday.date(),
        res['data']['user']['contributionsCollection']['totalCommitContributions']
    )

    for data in res['data']['user']['contributionsCollection']['commitContributionsByRepository']:
        slack_text += "\n・ {}: {}".format(
            data['repository']['nameWithOwner'],
            data['contributions']['totalCount']
        )
    slack = SlackAPI()
    slack.send_message("#times_uesho", slack_text)


def every_day_at_8pm_task():  # Lineに送信
    # user_name = "ue-sho"
    # dt_from = "2021-09-10T00:00:00"
    # dt_to = "2021-09-15T00:00:00"

    # res = get_commit_count(user_name, dt_from, dt_to)
    # slack_text = "{}さんの今日のコミット数は {} です。".format(
    #     res['data']['user']['name'],
    #     res['data']['user']['contributionsCollection']['totalCommitContributions']
    # )

    # for data in res['data']['user']['contributionsCollection']['commitContributionsByRepository']:
    #     slack_text += "\n* {}: {}".format(
    #         data['repository']['nameWithOwner'],
    #         data['contributions']['totalCount']
    #     )
    # slack = SlackAPI()
    # slack.send_message("#times_uesho", slack_text)
    pass


def main():
    every_day_at_0am_task()
    # schedule.every().days.at("00:00").do(every_day_at_0am_task)
    # schedule.every().days.at("20:00").do(every_day_at_8pm_task)


if __name__ == "__main__":
    main()