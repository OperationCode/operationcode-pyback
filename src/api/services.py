import logging
from functools import lru_cache
from typing import Dict, List

import requests
from django.urls import reverse
from slack import methods
from slack.io.requests import SlackAPI
from django.conf import settings

SLACK_TOKEN = settings.SLACK_TOKEN

slack_client = SlackAPI(token=SLACK_TOKEN, session=requests.session())
logger = logging.getLogger(__name__)


class Message:
    def __init__(self, ts, channel, text):
        self.ts = ts
        self.channel = channel
        self.text = text

    @property
    def channel_name(self) -> str:
        return Message.get_channel_name(self.channel)

    @property
    def delete_url(self) -> str:
        return reverse('delete_message', kwargs={'ts': self.ts, 'channel': self.channel})

    @classmethod
    @lru_cache(64)
    def get_channel_name(cls, channel: str) -> str:
        response = slack_client.query(methods.CONVERSATIONS_INFO, data=dict(channel=channel))
        if response['ok']:
            channel = response['channel']
            if 'name' in channel:
                return response['channel']['name']
            elif channel['is_im']:
                return cls.user_name_from_id(channel['user'])
            else:
                return channel
        else:
            return channel

    @classmethod
    @lru_cache(64)
    def user_name_from_id(cls, user_id: str):
        response = slack_client.query(methods.USERS_INFO, data=dict(user=user_id))
        try:
            if response['user']['real_name']:
                return response['user']['real_name'].title()
            elif response['user']['name']:
                return response['user']['name'].title()
        except KeyError as error:
            logger.exception(error)
        else:
            return 'New Member'

    def serialize(self) -> Dict[str, str]:
        return {
            'ts': self.ts,
            'channel': self.channel_name,
            'text': self.text,
            'delete_url': self.delete_url,
        }


def get_messages() -> List[Dict[str, str]]:
    bot_name = settings.BOT_NAME

    data = {
        'token': settings.SLACK_TOKEN,
        'query': f'from:{bot_name}',
        'count': 100,
        'sort': 'timestamp'
    }

    json_response = _call_slack_api(data)
    matches = json_response['messages']['matches']
    messages = [Message(match['ts'], match['channel']['id'], match['text']).serialize() for match in matches]
    return messages


def _call_slack_api(data):
    res = requests.post('https://slack.com/api/search.messages', data=data)
    logger.debug(f'API call method: search.messages || Result: {res.status_code}')
    res.raise_for_status()

    return res.json()


def delete(ts: str, channel: str):
    data = {
        'ts': ts,
        'channel': channel
    }
    res = slack_client.query(methods.CHAT_DELETE, data=data)
    return res
