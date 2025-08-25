from openai import OpenAI
import os


class ImageGenerator:
    """
    Генератор изображений (DALL·E).
    Если openai_key не передан, берётся из переменной окружения `openai_key`.
    """
    def __init__(self, openai_key: str | None = None):
        key = openai_key or os.getenv("openai_key")
        if not key:
            raise ValueError("openai_key не задан (ни аргументом, ни в переменных окружения).")
        self.client = OpenAI(api_key=key)

    def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        resp = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )
        return resp.data[0].url
