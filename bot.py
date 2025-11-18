from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import json

# Вставь сюда токен своего бота Telegram
BOT_TOKEN = "8299900071:AAFukyq_HYY4Psspwq16oPIZ4wItrJld6Cc"
bot = TeleBot(BOT_TOKEN)

# Словарь для хранения очков пользователей
user_points = {}

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    web_app_info = WebAppInfo(url="https://modetech07-sct.github.io/guru-predictions/webapp.html")
    button = InlineKeyboardButton(text="Открыть Гуру Прогнозов", web_app=web_app_info)
    markup = InlineKeyboardMarkup()
    markup.add(button)
    bot.send_message(message.chat.id, "Привет! Нажми кнопку, чтобы открыть Гуру Прогнозов.", reply_markup=markup)

# Обработка данных из WebApp
@bot.message_handler(func=lambda message: True, content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = json.loads(message.web_app_data.data)
        chat_id = message.chat.id

        # Начисляем очки (по 100 за каждый прогноз)
        points = len(data) * 100
        if chat_id in user_points:
            user_points[chat_id] += points
        else:
            user_points[chat_id] = points

        # Отправляем сообщение с начисленными очками
        bot.send_message(chat_id, f"Прогнозы получены! Ты заработал {points} XP. Всего очков: {user_points[chat_id]} XP.")

        # Показываем полученные прогнозы в консоли
        print(f"Пользователь {chat_id} отправил прогнозы:")
        for pred in data:
            print(f" - {pred['match']} : {pred['pred']}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке прогнозов: {e}")
        print(f"Ошибка: {e}")

# Запуск бота
print("Бот запущен...")
bot.infinity_polling()
