import requests
import datetime
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

class VKStats:
    def __init__(self):
        self.vk_api_key = os.getenv("VK_API_KEY")
        self.group_id = os.getenv("GROUP_ID")

    def get_stats(self, start_date: str, end_date: str, fmt: str = "%Y-%m-%d"):
        url = 'https://api.vk.com/method/stats.get'

        # Парсим даты
        start_dt = datetime.datetime.strptime(start_date, fmt)
        end_dt = datetime.datetime.strptime(end_date, fmt)

        # Привязываем к UTC и переводим в unixtime (целые секунды)
        start_dt = start_dt.replace(tzinfo=datetime.timezone.utc)
        end_dt = end_dt.replace(tzinfo=datetime.timezone.utc)

        start_unix_time = int(start_dt.timestamp())
        end_unix_time = int(end_dt.timestamp())

        params = {
            'access_token': self.vk_api_key,
            'v': '5.236',
            'group_id': self.group_id,
            'timestamp_from': start_unix_time,
            'timestamp_to': end_unix_time
        }
        response = requests.get(url, params=params).json()
        if 'error' in response:
            raise Exception(response['error']['error_msg'])

        data = response.get('response', [])
        return data[0] if data else {}

    def get_followers(self) -> int:
        url = 'https://api.vk.com/method/groups.getMembers'
        params = {
            'access_token': self.vk_api_key,
            'v': '5.236',
            'group_id': self.group_id
        }
        response = requests.get(url, params=params).json()
        if 'error' in response:
            raise Exception(response['error']['error_msg'])
        return response['response']['count']

if __name__ == "__main__":
    followers = VKStats().get_followers()
    print(followers)
