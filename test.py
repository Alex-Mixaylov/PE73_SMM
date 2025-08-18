from config import openai_key
from generators.text_gen import PostGenerator
from generators.image_gen import ImageGenerator

post_gen = PostGenerator(openai_key, tone="Позитивный", topic="Кожаные сумки ручной работы")
content = post_gen.generate_post()
img_desc = post_gen.generate_post_image_description()

img_gen = ImageGenerator(openai_key)
image_url = img_gen.generate_image(img_desc)

print(content)
print(img_desc)
print(image_url)