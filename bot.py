from telebot import TeleBot, types
import json

# Токен твоего бота
BOT_TOKEN = "8299900071:AAFukyq_HYY4Psspwq16oPIZ4wItrJld6Cc"
bot = TeleBot(BOT_TOKEN)

# Хранение очков пользователей
user_points = {}

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    web_app_info = types.WebAppInfo(url="https://modetech07-sct.github.io/guru-predictions/index.html")
    button = types.InlineKeyboardButton(text="Открыть Гуру Прогнозов", web_app=web_app_info)
    markup = types.InlineKeyboardMarkup()
    markup.add(button)
    bot.send_message(message.chat.id, "Привет! Нажми кнопку, чтобы открыть Гуру Прогнозов.", reply_markup=markup)

# Обработка данных из WebApp
@bot.message_handler(func=lambda message: True, content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = json.loads(message.web_app_data.data)
        chat_id = message.chat.id

        points = len(data) * 100
        user_points[chat_id] = user_points.get(chat_id, 0) + points

        bot.send_message(chat_id, f"Прогнозы получены! Ты заработал {points} XP. Всего очков: {user_points[chat_id]} XP.")

        # Печать прогнозов в консоль
        print(f"Пользователь {chat_id} отправил прогнозы:")
        for pred in data:
            print(f" - {pred['match']} : {pred['pred']}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке прогнозов: {e}")
        print(f"Ошибка: {e}")

# Запуск бота
print("Бот запущен...")
bot.infinity_polling()
