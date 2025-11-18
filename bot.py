from telebot import TeleBot, types
import json

BOT_TOKEN = "8299900071:AAFukyq_HYY4Psspwq16oPIZ4wItrJld6Cc"
bot = TeleBot(BOT_TOKEN)

user_predictions = {}  # chat_id -> список прогнозов
user_points = {}       # chat_id -> очки

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    web_app_info = types.WebAppInfo(url="https://modetech07-sct.github.io/guru-predictions/index.html")
    button = types.InlineKeyboardButton(text="Открыть Гуру Прогнозов", web_app=web_app_info)
    markup = types.InlineKeyboardMarkup()
    markup.add(button)
    bot.send_message(message.chat.id, "Привет! Нажми кнопку, чтобы открыть Гуру Прогнозов.", reply_markup=markup)

# обработка данных WebApp
@bot.message_handler(func=lambda m: True, content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = json.loads(message.web_app_data.data)
        chat_id = message.chat.id

        user_predictions[chat_id] = data  # сохраняем прогнозы
        bot.send_message(chat_id, "Прогнозы успешно приняты! Очки будут начислены после матчей.")

        # показываем в консоли
        print(f"Пользователь {chat_id} отправил прогнозы:")
        for pred in data:
            print(f" - {pred['match']} : {pred['pred']}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке прогнозов: {e}")
        print(f"Ошибка: {e}")

print("Бот запущен...")
bot.infinity_polling()

