import requests

import settings
from slack.slack_api import SlackAPI


def main():
    slack = SlackAPI(settings.SLACK_API_TOKEN)
    slack.send_message("#times_uesho", "git commit count")

if __name__ == "__main__":
    main()