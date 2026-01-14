import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request
import analyzer  # сенің AI талдау модулі

# --- Telegram Token ---
TOKEN = os.getenv("BOT_TOKEN")  # Render-та BOT_TOKEN деп Environment Variable жаса
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable анықталмаған!")

bot = telebot.TeleBot(TOKEN)

# --- Flask сервері ---
app = Flask(__name__)

# --- Сәлемдесу мәтіні ---
WELCOME_TEXT = """
Сәлеметсіз бе! 👋  
Бұл — WARDEN-X AI киберқауіпсіздік жүйесі.

🛡️ WARDEN-X не істейді?
• Фишинг және алаяқтық мәтіндерді анықтайды
• Зиянды сілтемелер мен қауіпті код белгілерін табады
• Әлеуметтік инженерия әрекеттерін талдайды
• Қауіп деңгейін 0–100 аралығында бағалайды

📌 Қалай қолдану керек?
1) 🔍 "Мәтінді тексеру" батырмасын басыңыз
2) Тексерілетін мәтінді жіберіңіз
3) Қауіпсіздік есебі көрсетіледі
"""

# --- User state сақтау ---
user_state = {}  # {user_id: "WAITING_FOR_TEXT"}

# --- /start командасы ---
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔍 Мәтінді тексеру", callback_data="scan_text"))
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=markup)

# --- Батырмаларды басу ---
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "scan_text":
        user_state[call.from_user.id] = "WAITING_FOR_TEXT"
        bot.send_message(call.message.chat.id, "Мәтінді жіберіңіз, мен оны талдаймын:")

# --- Мәтінді қабылдау ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    if user_state.get(user_id) == "WAITING_FOR_TEXT":
        bot.send_message(message.chat.id, "Талдау жүргізілуде... ⏳")
        try:
            result = analyzer.check_phishing_with_ai(message.text)
            res_up = result.upper()
            if any(word in res_up for word in ["DANGER", "ҚАУІП", "PHISHING", "⚠️"]):
                status_emoji = "🔴 ЖОҒАРЫ ҚАУІП"
            elif any(word in res_up for word in ["MEDIUM", "ОРТАША", "⚠"]):
                status_emoji = "🟠 Орташа Қауіп"
            else:
                status_emoji = "🟢 Қауіпсіз"
            
            bot.send_message(message.chat.id, f"{status_emoji}\n\n{result}")
        except Exception as e:
            bot.send_message(message.chat.id, f"Қате орын алды: {e}")
        user_state[user_id] = None
    else:
        bot.send_message(message.chat.id, "🔹 Мәтінді тексеру үшін алдымен 'Мәтінді тексеру' батырмасын басыңыз.")

# --- Webhook ---
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL")  # Render URL
if not WEBHOOK_URL:
    raise ValueError("RENDER_EXTERNAL_URL environment variable анықталмаған!")

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@app.route('/')
def home():
    return "Bot is running!"

# --- Run Flask ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render PORT
    app.run(host="0.0.0.0", port=port)
