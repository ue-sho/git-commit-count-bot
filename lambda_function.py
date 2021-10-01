from datetime import datetime, timedelta, timezone

from github.github_api import GitHubAPI
from slack.slack_api import SlackAPI


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


def get_isoformat_time_a_day_ahead():
    jst = timezone(timedelta(hours=+9), 'JST')

    now = datetime.now(jst)
    yesterday = now + timedelta(days=-1)

    dt_from = str(yesterday.isoformat())
    dt_to = str(now.isoformat())
    print("from {} to {} ".format(dt_from, dt_to))

    return dt_from, dt_to


def notify_slack_of_commit_count(dt_from, dt_to):

    user_name = "ue-sho"
    res = get_commit_count(user_name, dt_from, dt_to)

    commit_data = res['data']['user']['contributionsCollection']

    slack_text = "{}さんの {} ~ {} のコミット数は {} です。".format(
        res['data']['user']['name'],
        dt_from.replace('-', '/').replace('T', ' ')[:16],
        dt_to.replace('-', '/').replace('T', ' ')[:16],
        commit_data['totalCommitContributions']
    )
    for data in commit_data['commitContributionsByRepository']:
        slack_text += "\n・ {}: {}".format(
            data['repository']['nameWithOwner'],
            data['contributions']['totalCount']
        )

    slack = SlackAPI()
    res = slack.send_message("#times_uesho", slack_text)

    return res


def lambda_handler(event, context):
    print("event: ", event)
    print("context: ", context)

    dt_from, dt_to = get_isoformat_time_a_day_ahead()
    notify_slack_of_commit_count(dt_from, dt_to)
