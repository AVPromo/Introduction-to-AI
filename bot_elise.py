import markovify
import telebot

API_TOKEN = 'API_TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# Загрузка текстового набора для создания модели
text = open('bot_elise.txt', encoding='utf8').read()


# Создание модели цепи Маркова
text_model = markovify.Text(text, state_size=2)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Элиза. Чем могу помочь?")

# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def echo_all(message):
    response = generate_response(text_model, message.text)
    if response:
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "Извините, я не могу понять ваш запрос.")

# Генерация ответа на основе полученного сообщения
def generate_response(text_model, message):
    return text_model.make_short_sentence(max_chars=40, min_chars=5, tries=100, seed=find_longest_word(message))

# Поиск в полученном сообщении самого длинного слова
def find_longest_word(message):
    words = message.split()
    longest_word = max(words, key=len)
    return longest_word

bot.polling()
