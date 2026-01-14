from openai import OpenAI
import os
from dotenv import load_dotenv

# .env файлын жүктеу
load_dotenv()

# OpenAI клиенті
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def check_phishing_with_ai(text: str) -> str:
    """
    WARDEN-X AI
    Мәтінді киберқауіпсіздік тұрғысынан талдайды
    """

    prompt = f"""
Сен Warden-X атты кәсіби киберқауіпсіздік маманысың.

Тексерілетін мәтін:
{text}

Талдау міндеттері:
1) Фишинг немесе алаяқтық белгілері
2) Зиянды сілтемелер, XSS, SQL injection, exploit
3) SCADA немесе өндірістік жүйелерге қауіп
4) Әлеуметтік инженерия тәсілдері

Нәтиже форматы:
Қауіп деңгейі: (0-100)
Сипаттама:
Ұсыныс:

Маңызды:
- Жауап тек қазақ тілінде болсын
- Қысқа әрі нақты жаз
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # арзан әрі жылдам
            messages=[
                {
                    "role": "system",
                    "content": "Сен кәсіби киберқауіпсіздік анализаторсың."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=350
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"ЖИ қатесі: {e}"
