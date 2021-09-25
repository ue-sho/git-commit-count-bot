import json

import requests

from slack.slack_api import SlackAPI
from github.github_api import GitHubAPI


def get_commit_count():
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
        "name": "ue-sho",
        "from": "2021-09-24T00:00:00",
        "to": "2021-09-25T00:00:00"
    }

    github = GitHubAPI()
    res = github.post(contributions_query, variables)
    return res.json()


def main():
    res = get_commit_count()

    slack_text = "昨日のコミット数は {} です。".format(
        res['data']['user']['contributionsCollection']['totalCommitContributions']
    )

    for data in res['data']['user']['contributionsCollection']['commitContributionsByRepository']:
        slack_text += "\n* {}: {}".format(
            data['repository']['nameWithOwner'],
            data['contributions']['totalCount']
        )

    print(slack_text)

    slack = SlackAPI()
    slack.send_message("#times_uesho", slack_text)


if __name__ == "__main__":
    main()