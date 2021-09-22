import datetime

import pytz
import requests
from github import Github
from slackbot.bot import (
    Bot,
    respond_to,
    listen_to
)


# GITHUB_ACCESS_TOKEN = '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'


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


def main():
    bot = Bot()
    bot.run()


@respond_to('今日')
def today_respond_to(message):
    res = commit_count()
    message.send("今日のコミット数は {} です".format(res))


@respond_to(r'.*日前')
def before_days_respond_to(message):
    text = message.body['text']
    day = int(text[:-2])
    res = commit_count(day)
    message.send("{}日前のコミット数は {} です".format(day, res))


# @listen_to('prod')
# def test_listen_to(message):
#     message.reply("今日のコミット数は5です") # replyにすると送信者にメンションする


if __name__ == "__main__":
    main()