from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

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
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.2,
            max_output_tokens=350
        )

        return response.output_text.strip()

    except Exception as e:
        return f"ЖИ қатесі: {str(e)}"
