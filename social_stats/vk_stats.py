import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class VKStats:
    def __init__(self, vk_api_key: str | None = None, group_id: str | None = None):
        self.vk_api_key = vk_api_key or os.getenv("VK_API_KEY")
        self.group_id = group_id or os.getenv("GROUP_ID")
        if not self.vk_api_key or not self.group_id:
            raise ValueError("VK_API_KEY или GROUP_ID не заданы (ни аргументом, ни в .env).")

    def get_stats(self, start_date: str, end_date: str, fmt: str = "%Y-%m-%d"):
        url = 'https://api.vk.com/method/stats.get'
        start_dt = datetime.datetime.strptime(start_date, fmt).replace(tzinfo=datetime.timezone.utc)
        end_dt = datetime.datetime.strptime(end_date, fmt).replace(tzinfo=datetime.timezone.utc)
        params = {
            'access_token': self.vk_api_key,
            'v': '5.236',
            'group_id': self.group_id,
            'timestamp_from': int(start_dt.timestamp()),
            'timestamp_to': int(end_dt.timestamp())
        }
        resp = requests.get(url, params=params).json()
        if 'error' in resp:
            raise Exception(resp['error']['error_msg'])
        data = resp.get('response', [])
        return data[0] if data else {}

    def get_followers(self) -> int:
        resp = requests.get(
            'https://api.vk.com/method/groups.getMembers',
            params={'access_token': self.vk_api_key, 'v': '5.236', 'group_id': self.group_id}
        ).json()
        if 'error' in resp:
            raise Exception(resp['error']['error_msg'])
        return resp['response']['count']
