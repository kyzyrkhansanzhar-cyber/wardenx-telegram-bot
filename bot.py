import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import analyzer  # сенің AI талдау модулі

TOKEN = "7999401141:AAFbyZwH6rdTuTveSDKnTBYIjdgPy-m_Ak4"
bot = telebot.TeleBot(TOKEN)

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
            # AI талдау
            result = analyzer.check_phishing_with_ai(message.text)
            
            # Қауіп деңгейін анықтау (тексттен іздеу)
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

# --- Ботты іске қосу ---
bot.infinity_polling()
