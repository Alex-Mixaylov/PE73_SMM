import os
from dotenv import load_dotenv
from app import create_app

# Загружаем .env один раз при старте приложения
load_dotenv()


print("OPENAI_KEY:", os.getenv("openai_key"))
print("VK_API_KEY:", os.getenv("VK_API_KEY"))
print("GROUP_ID:", os.getenv("GROUP_ID"))

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
