from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import json
from datetime import datetime, timedelta

# -------------------------------
# Вставьте сюда токен своего бота
BOT_TOKEN = "8299900071:AAFukyq_HYY4Psspwq16oPIZ4wItrJld6Cc"
# -------------------------------

bot = TeleBot(BOT_TOKEN)

# Словарь для хранения очков пользователей
user_points = {}

# Дедлайн отправки прогнозов (за 2 часа до первого матча)
deadline = datetime(2025, 11, 21, 14, 0)  # пример: 21 ноября 2025, 14:00

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    web_app_info = WebAppInfo(
        url="https://modetech07-sct.github.io/guru-predictions/index.html"
    )
    button = InlineKeyboardButton(
        text="Открыть Гуру Прогнозов", web_app=web_app_info
    )
    markup = InlineKeyboardMarkup()
    markup.add(button)
    bot.send_message(
        message.chat.id,
        "Привет! Нажми кнопку, чтобы открыть Гуру Прогнозов.",
        reply_markup=markup
    )

# Обработка данных из WebApp
@bot.message_handler(func=lambda message: True, content_types=['web_app_data'])
def handle_web_app_data(message):
    now = datetime.now()
    if now > deadline:
        bot.send_message(
            message.chat.id,
            "Извините, дедлайн для отправки прогнозов уже наступил."
        )
        return

    try:
        data = json.loads(message.web_app_data.data)
        chat_id = message.chat.id

        # Начисляем очки только за прогнозы после дедлайна
        points = len(data) * 100  # временно начисляем для проверки
        if chat_id in user_points:
            user_points[chat_id] += points
        else:
            user_points[chat_id] = points

        bot.send_message(
            chat_id,
            f"Прогнозы получены! Ты заработал {points} XP. "
            f"Всего очков: {user_points[chat_id]} XP."
        )

        print(f"Пользователь {chat_id} отправил прогнозы:")
        for pred in data:
            print(f" - {pred['match']} : {pred['pred']}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке прогнозов: {e}")
        print(f"Ошибка: {e}")

# Запуск бота
print("Бот запущен...")
bot.infinity_polling()
