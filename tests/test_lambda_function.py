from unittest.mock import MagicMock, patch

import lambda_function


@patch('lambda_function.SlackAPI')
@patch('lambda_function.get_commit_count')
def test_get_commit_count(get_commit_count, slack_mock):
    get_commit_count.return_value = {
        'data': {
            'user': {
                'name': 'uesho',
                'contributionsCollection': {
                    'totalRepositoryContributions': 0,
                    'totalCommitContributions': 1,
                    'commitContributionsByRepository': [
                        {
                            'repository': {
                                'nameWithOwner': 'ue-sho/git-commit-count-bot'
                            },
                            'contributions': {'totalCount': 1}
                        }
                    ]
                }
            }
        }
    }

    slack_res = {
        'ok': True,
        'channel': 'CV7ANQBMZ',
        'ts': '1633014323.022000',
        'message': {
            'bot_id': 'B02G8NZ0UG0',
            'type': 'message',
            'text': 'ueshoさんの2021-09-29のコミット数は 1 です。\n・ ue-sho/git-commit-count-bot: 1',
            'user': 'U02FG48E06R',
            'ts': '1633014323.022000',
            'team': 'TGUDF5QVB',
            'bot_profile': {
                'id': 'B02G8NZ0UG0',
                'app_id': 'A02FK1ETM5H',
                'name': 'git_commit_count',
                'icons': {
                    'image_36': 'https://avatars.slack-edge.com/2021-09-24/2537963772132_1c2cee321ddf22fe9fef_36.png',
                    'image_48': 'https://avatars.slack-edge.com/2021-09-24/2537963772132_1c2cee321ddf22fe9fef_48.png',
                    'image_72': 'https://avatars.slack-edge.com/2021-09-24/2537963772132_1c2cee321ddf22fe9fef_72.png'
                },
                'deleted': False,
                'updated': 1632549837,
                'team_id': 'TGUDF5QVB'
            }
        }
    }
    slack_instance = MagicMock()
    slack_instance.send_message.return_value = slack_res
    slack_mock.return_value = slack_instance

    dt_from, dt_to = lambda_function.get_isoformat_time_a_day_ahead()
    res = lambda_function.notify_slack_of_commit_count(dt_from, dt_to)

    assert res == slack_res
