# -*- coding:utf-8 -*-

import requests
import json
from argparse import ArgumentParser
import logging


SLACK_API_BASE = "https://slack.com/api"
API_CHANNEL = "/channels.info?channel={channel}&token={token}"
API_USER = "/users.info?user={id}&token={token}&pretty=1"


def get_channel_members(channel, token):
    api = SLACK_API_BASE + API_CHANNEL.format(channel=channel, token=token)
    response = requests.get(api)
    data = json.loads(response.text)
    if data["ok"]:
        logging.debug(data)
    return data["channel"]["members"]


def get_users(members, token):
    for user_id in members:
        api = SLACK_API_BASE + API_USER.format(id=user_id, token=token)
        response = requests.get(api)
        data = json.loads(response.text)
        if data["ok"]:
            print(data["user"]["name"])
        else:
            logging.error("error! : {}".format(api))
            break


if __name__ == '__main__':
    usage = 'Usage: python {} [--channel <channel ID>] [--token <token>] [--help]'.format(__file__)
    parser = ArgumentParser(usage=usage)
    parser.add_argument('-c', '--channel', type=str, dest='channel', help='Slack Channel ID', required=True)
    parser.add_argument('-t', '--token', type=str, dest='token', help='Slack API Token', required=True)
    args = parser.parse_args()

    members = get_channel_members(args.channel, args.token)
    get_users(members, args.token)
