from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI клиентін баптау
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def check_phishing_with_ai(text: str) -> str:
    prompt = f"""
Сен Warden-X атты кәсіби киберқауіпсіздік маманысың.

Тексерілетін мәтін:
{text}

Талдау міндеттері:
1) Фишинг немесе алаяқтық белгілері
2) Зиянды сілтемелер, XSS, SQL injection, exploit
3) Әлеуметтік инженерия тәсілдері

Нәтиже форматы:
Қауіп деңгейі: (0-100)
Сипаттама:
Ұсыныс:

Маңызды:
- Жауап тек қазақ тілінде болсын
- Қысқа әрі нақты жаз
"""

    try:
        # Chat completions қолдану керек
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Модель атауы түзетілді
            messages=[
                {"role": "system", "content": "Сен киберқауіпсіздік сарапшысысың."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500 # max_output_tokens емес, max_tokens
        )

        # Жауапты алу жолы түзетілді
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"ЖИ қатесі: {str(e)}"