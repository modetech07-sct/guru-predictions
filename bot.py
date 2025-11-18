from telebot import TeleBot, types
import json
from datetime import datetime, timedelta

# Вставь сюда токен своего бота
BOT_TOKEN = "8299900071:AAFukyq_HYY4Psspwq16oPIZ4wItrJld6Cc"
bot = TeleBot(BOT_TOKEN)

# Хранение прогнозов и очков
user_points = {}
user_predictions = {}

# Дата и время первого матча (формат: год-месяц-день часы:минуты)
first_match_time = datetime.strptime("2025-11-21 19:00", "%Y-%m-%d %H:%M")
deadline = first_match_time - timedelta(hours=2)

# Список матчей 16-го тура
matches = [
    {"date": "21 ноября", "home": "Акрон", "away": "Сочи"},
    {"date": "22 ноября", "home": "Оренбург", "away": "Балтика"},
    {"date": "22 ноября", "home": "Спартак", "away": "ЦСКА"},
    {"date": "22 ноября", "home": "Рубин", "away": "Ахмат"},
    {"date": "23 ноября", "home": "Крылья Советов", "away": "Ростов"},
    {"date": "23 ноября", "home": "Пари НН", "away": "Зенит"},
    {"date": "23 ноября", "home": "Динамо (Москва)", "away": "Динамо (Махачкала)"},
    {"date": "23 ноября", "home": "Локомотив", "away": "Краснодар"}
]

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    web_app_info = types.WebAppInfo(url="https://modetech07-sct.github.io/guru-predictions/index.html")
    button = types.InlineKeyboardButton(text="Открыть Гуру Прогнозов", web_app=web_app_info)
    markup = types.InlineKeyboardMarkup()
    markup.add(button)
    bot.send_message(chat_id, "Привет! Нажми кнопку, чтобы открыть Гуру Прогнозов.", reply_markup=markup)

# Обработка данных из WebApp
@bot.message_handler(func=lambda message: True, content_types=['web_app_data'])
def handle_web_app_data(message):
    chat_id = message.chat.id
    now = datetime.now()

    if now > deadline:
        bot.send_message(chat_id, "Сожалеем, прогнозы больше не принимаются. Дедлайн прошёл.")
        return

    try:
        data = json.loads(message.web_app_data.data)

        # Сохраняем прогнозы пользователя
        user_predictions[chat_id] = data

        bot.send_message(chat_id, f"Прогнозы успешно получены! Они будут проверены после матчей.")
        print(f"Пользователь {chat_id} отправил прогнозы:")
        for pred in data:
            print(f" - {pred['match']} : {pred['pred']}")

    except Exception as e:
        bot.send_message(chat_id, f"Ошибка при обработке прогнозов: {e}")
        print(f"Ошибка: {e}")

# Запуск бота
print("Бот запущен...")
bot.infinity_polling()
