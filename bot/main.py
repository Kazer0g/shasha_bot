
import telebot
from src import TOKEN, GIPHYTOKEN # Импорт файла с токенами (бота и giphy)

import json
# Зададим текст сообщений бота через константы
GREETINGS = "Здравствуйте"
COMMANDS = """
Список команд:
/discount - скидка на весь ассортимент
/faq - часто задаваемые вопросы
/menu - меню
/location - местоположение
/feedback - оставить обратную связь
"""
LOCATION = [55.7610151, 37.4748494, "Описание местположения"]
FAQ = "Здесь будет просто текст"
NAME = "Чтобы получить скидку 5% неоюходимо зарегистрироваться. Введите своё имя"
NUMBER = "Введите свой номер телефона в формате +7XXXXXXXXXX"
TFREGISTRATION = "Вы успешно зарегистрированны! Ваша гифка на скидку:"
FEEDBACK = "Если у вас есть какие-то комментарии или замечания к нашей работе, пожалуйста оставьте их ниже"
TFFEEDBACK = "Спасибо! В ближайшее время мы ознакомимся с фидбэком. В случае необходимости обратиться в клиентскую поддержку, пишите на почту vkusnicofi@mail.ru"


bot = telebot.TeleBot(TOKEN)

# Запуск взаимодействия с ботом
@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(text=GREETINGS, chat_id=message.chat.id)

# Вывод функционала бота
@bot.message_handler(commands=["help"])
def help_handler(message):
    bot.send_message(text=COMMANDS, chat_id=message.chat.id)

# Функция получения данных и отправка gif в качестве уникального кода
@bot.message_handler(commands=["discount"])
def discount_handler(message):
    bot.send_message(text=NAME, chat_id=message.chat.id)
    bot.register_next_step_handler(message, get_name)

# Получение имени и запрос номера телефана или повторный запрос имени
def get_name(message):
    print(message.text)
    # Проверка имени на валидность
    if message.text[0] != "/":
        bot.send_message(text=NUMBER, chat_id=message.chat.id)
        bot.register_next_step_handler(message, get_phone)
    else:
        bot.send_message(
            text="Некорректные данные, попробуйте ещё раз", chat_id=message.chat.id
        )
        bot.register_next_step_handler(message, get_name)

# Получение номера телефона и отправка случайной гиф или повторный запрос номера телефона
def get_phone(message):
    print(message.text)
    # Проверка номера телефона на валидность
    if message.text[0] == "+":
        bot.send_message(text=TFREGISTRATION, chat_id=message.chat.id)
        bot.send_animation(message.chat.id, get_random_gif())
    else:
        bot.send_message(
            text="Некорректные данные, попробуйте ещё раз", chat_id=message.chat.id
        )
        bot.register_next_step_handler(message, get_phone)

# Получение случайной gif
def get_random_gif():
    import requests

    url = "https://api.giphy.com/v1/gifs/random"
    params = {"api_key": GIPHYTOKEN, "rating": "g"}
    response = requests.get(url, params=params)
    return response.json()["data"]["images"]["original"]["url"]

# Отправка текста с частозадаваемыми вопросами и ответами
@bot.message_handler(commands=["faq"])
def faq_handler(message):
    bot.send_message(text=FAQ, chat_id=message.chat.id)

# Отправка местоположения с помощью геопозиции и комментария
@bot.message_handler(commands=["location"])
def location_handler(message):
    bot.send_location(
        latitude=LOCATION[0], longitude=LOCATION[1], chat_id=message.chat.id
    )
    bot.send_message(text=LOCATION[2], chat_id=message.chat.id)

# Запрос обратной связи 
@bot.message_handler(commands=["feedback"])
def feedback_handler(message):
    bot.send_message(text=FEEDBACK, chat_id=message.chat.id)
    bot.register_next_step_handler(message, get_feedback)

# Получение обратной связи
def get_feedback(message):
    print(message.text)
    bot.send_message(text=TFFEEDBACK, chat_id=message.chat.id)

# Зацикливание бота
bot.polling(none_stop=True, interval=0)
