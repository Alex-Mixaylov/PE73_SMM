import os
from dotenv import load_dotenv

from generators.text_gen import PostGenerator
from generators.image_gen import ImageGenerator
from social_publishers.vk_publisher import VKPublisher

# Загружаем переменные из .env
load_dotenv()

openai_key = os.getenv("openai_key")
vk_api_key = os.getenv("VK_API_KEY")
group_id = os.getenv("GROUP_ID")

post_gen = PostGenerator(openai_key, tone="Позитивный", topic="Кожаные сумки ручной работы")
content = post_gen.generate_post()
img_desc = post_gen.generate_post_image_description()

img_gen = ImageGenerator(openai_key)
image_url = img_gen.generate_image(img_desc)

#Смотрим что  будет публиковаться  перед публикацией.
print(content)
print(image_url)

vk_pub = VKPublisher()
vk_pub.publish_post(content, image_url)


