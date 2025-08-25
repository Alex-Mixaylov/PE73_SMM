from openai import OpenAI
import os


class PostGenerator:
    """
    Генератор текста поста для соцсетей.
    Если openai_key не передан, берётся из переменной окружения `openai_key`.
    """
    def __init__(self, openai_key: str | None, tone: str, topic: str):
        key = openai_key or os.getenv("openai_key")
        if not key:
            raise ValueError("openai_key не задан (ни аргументом, ни в переменных окружения).")
        self.client = OpenAI(api_key=key)
        self.tone = tone
        self.topic = topic

    def generate_post(self) -> str:
        resp = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                 "content": (
                    "Ты высококвалифицированный SMM-специалист, который помогает генерировать тексты "
                    "для постов во ВКонтакте с заданной тематикой и тоном."
                 )},
                {"role": "user",
                 "content": (
                    f"Сгенерируй пост для соцсетей на тему: {self.topic}. "
                    f"Используй тон: {self.tone}. "
                    "Добавь не более двух эмодзи в тексте и никогда не используй радугу."
                 )}
            ]
        )
        return resp.choices[0].message.content

    def generate_post_image_description(self) -> str:
        resp = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                 "content": (
                    "Ты ассистент, который формирует чёткий промпт для модели генерации изображений "
                    "по заданной тематике."
                 )},
                {"role": "user",
                 "content": f"Сформируй промпт для изображения к посту на тему: {self.topic}."}
            ]
        )
        return resp.choices[0].message.content
