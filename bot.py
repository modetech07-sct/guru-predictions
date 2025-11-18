from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from datetime import datetime, timedelta
import json

# Токен вашего бота
BOT_TOKEN = "8299900071:AAFukyq_HYY4Psspwq16oPIZ4wItrJld6Cc"
bot = TeleBot(BOT_TOKEN)

# Очки пользователей
user_points = {}

# Дата и время первого матча недели (пример)
first_match_time = datetime(2025, 11, 21, 18, 0)  # 21 ноября 2025, 18:00
deadline = first_match_time - timedelta(hours=2)  # Прогнозы можно ставить до 2 часов до матча

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    web_app_info = WebAppInfo(url="https://modetech07-sct.github.io/guru-predictions/index.html")
    button = InlineKeyboardButton(text="Открыть Гуру Прогнозов", web_app=web_app_info)
    markup = InlineKeyboardMarkup()
    markup.add(button)
    bot.send_message(message.chat.id, "Привет! Нажми кнопку, чтобы открыть Гуру Прогнозов.", reply_markup=markup)

# Обработка данных из WebApp
@bot.message_handler(func=lambda message: True, content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        chat_id = message.chat.id

        # Проверка дедлайна
        if datetime.now() > deadline:
            bot.send_message(chat_id, "Прогнозы на эту неделю уже закрыты.")
            return

        # Парсим данные
        data = json.loads(message.web_app_data.data)
        if not data or not isinstance(data, list):
            bot.send_message(chat_id, "Ошибка: прогнозы не получены или неверный формат.")
            return

        points = len(data) * 100
        user_points[chat_id] = user_points.get(chat_id, 0) + points

        bot.send_message(chat_id, f"Прогнозы получены! Ты заработал {points} XP. Всего очков: {user_points[chat_id]} XP.")

        # Вывод прогнозов в консоль
        print(f"Пользователь {chat_id} отправил прогнозы:")
        for pred in data:
            print(f" - {pred['match']} : {pred['pred']}")

    except Exception as e:
        bot.send_message(chat_id, f"Ошибка при обработке прогнозов: {e}")
        print(f"Ошибка: {e}")

# Запуск бота
print("Бот запущен...")
bot.infinity_polling()
