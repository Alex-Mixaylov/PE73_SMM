import requests
import os
from dotenv import load_dotenv

load_dotenv()

class VKPublisher:
    def __init__(self, vk_api_key: str | None = None, group_id: str | None = None):
        # если не передали явно — возьмём из .env
        self.vk_api_key = vk_api_key or os.getenv("VK_API_KEY")
        self.group_id = group_id or os.getenv("GROUP_ID")
        if not self.vk_api_key or not self.group_id:
            raise ValueError("VK_API_KEY или GROUP_ID не заданы (ни аргументом, ни в .env).")

    def upload_photo(self, image_url: str) -> str:
        upload_url_response = requests.get(
            'https://api.vk.com/method/photos.getWallUploadServer',
            params={'access_token': self.vk_api_key, 'v': '5.236', 'group_id': self.group_id}
        ).json()
        if 'error' in upload_url_response:
            raise Exception(upload_url_response['error']['error_msg'])

        upload_url = upload_url_response['response']['upload_url']
        image_data = requests.get(image_url).content
        upload_response = requests.post(upload_url, files={'photo': ('image.jpg', image_data)}).json()

        save_response = requests.get(
            'https://api.vk.com/method/photos.saveWallPhoto',
            params={
                'access_token': self.vk_api_key,
                'v': '5.236',
                'group_id': self.group_id,
                'photo': upload_response['photo'],
                'server': upload_response['server'],
                'hash': upload_response['hash']
            }
        ).json()
        if 'error' in save_response:
            raise Exception(save_response['error']['error_msg'])

        photo_id = save_response['response'][0]['id']
        owner_id = save_response['response'][0]['owner_id']
        return f'photo{owner_id}_{photo_id}'

    def publish_post(self, content: str, image_url: str | None = None):
        params = {
            'access_token': self.vk_api_key,
            'from_group': 1,
            'v': '5.236',
            'owner_id': f'-{self.group_id}',
            'message': content
        }
        if image_url:
            params['attachments'] = self.upload_photo(image_url)
        return requests.post('https://api.vk.com/method/wall.post', params=params).json()
