from slackbot.bot import (
    respond_to,
    listen_to
)

from github.github_api import commit_count


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
