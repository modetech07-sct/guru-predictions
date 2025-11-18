from telebot import TeleBot, types
import json
from datetime import datetime, timedelta

BOT_TOKEN = "8299900071:AAFukyq_HYY4Psspwq16oPIZ4wItrJld6Cc"
bot = TeleBot(BOT_TOKEN)

user_points = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    web_app_info = types.WebAppInfo(url="https://modetech07-sct.github.io/guru-predictions/index.html")
    button = types.InlineKeyboardButton(text="Открыть Гуру Прогнозов", web_app=web_app_info)
    markup = types.InlineKeyboardMarkup()
    markup.add(button)
    bot.send_message(message.chat.id, "Привет! Нажми кнопку, чтобы открыть Гуру Прогнозов.", reply_markup=markup)

@bot.message_handler(func=lambda message: True, content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = json.loads(message.web_app_data.data)
        chat_id = message.chat.id

        now = datetime.utcnow()
        # Проверка времени: принимаем только прогнозы до 2 часов до первого матча
        with open("matches.json", "r", encoding="utf-8") as f:
            matches = json.load(f)
        first_match_time = datetime.fromisoformat(matches[0]['date'])
        deadline = first_match_time - timedelta(hours=2)

        if now > deadline:
            bot.send_message(chat_id, f"Прогнозы больше не принимаются. Дедлайн был {deadline}")
            return

        points = len(data) * 100
        if chat_id in user_points:
            user_points[chat_id] += points
        else:
            user_points[chat_id] = points

        bot.send_message(chat_id, f"Прогнозы получены! Ты заработал {points} XP. Всего очков: {user_points[chat_id]} XP.")
        print(f"Пользователь {chat_id} отправил прогнозы:")
        for pred in data:
            print(f" - {pred['match']} : {pred['pred']}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке прогнозов: {e}")
        print(f"Ошибка: {e}")

print("Бот запущен...")
bot.infinity_polling()

