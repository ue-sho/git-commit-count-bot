from datetime import datetime, timedelta, timezone

from github.github_api import GitHubAPI
from slack.slack_api import SlackAPI


def get_commit_count(date):
    commit_count_query = """
        query($date: GitTimestamp!) {
          viewer {
            repositories(last: 100) {
              nodes {
                nameWithOwner
                defaultBranchRef {
                  target {
                    ... on Commit {
                      history(since: $date) {
                          totalCount
                      }
                    }
                  }
                }
              }
            }
          }
        }
    """
    variables = {
        "date": date
    }

    github = GitHubAPI()
    res = github.post(commit_count_query, variables)
    return res.json()


def get_isoformat_time_a_day_ahead():
    jst = timezone(timedelta(hours=+9), 'JST')

    now = datetime.now(jst)
    yesterday = now + timedelta(days=-1)

    yesterday_iso = str(yesterday.isoformat())
    print("from {} ".format(yesterday_iso))

    return yesterday_iso


def notify_slack_of_commit_count(date):

    res = get_commit_count(date)

    repo_date = res['data']['viewer']['repositories']['nodes']

    total_commit_count = 0
    slack_detail_text = ''
    for data in repo_date:
        nameWithOwner = data['nameWithOwner']
        if nameWithOwner == 'ue-sho/ue-sho':
            continue

        commit_count = data['defaultBranchRef']['target']['history']['totalCount']
        if commit_count == 0:
            continue

        total_commit_count += commit_count
        slack_detail_text += "\n・ {}: {}".format(
            nameWithOwner,
            commit_count
        )

    slack_text = "{}からのコミット数は {} です。".format(
        date.replace('-', '/').replace('T', ' ')[:16],
        total_commit_count
    )
    slack_text += slack_detail_text
    print(slack_text)

    slack = SlackAPI()
    res = slack.send_message("#times_uesho", slack_text)

    return res


def lambda_handler(event, context):
    print("event: ", event)
    print("context: ", context)

    date = get_isoformat_time_a_day_ahead()
    notify_slack_of_commit_count(date)


if __name__ == '__main__':
    lambda_handler(None, None)
