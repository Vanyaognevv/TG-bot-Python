import telebot
from config import keys, TOKEN
from Exceptionapp import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Привет, {0.first_name}!' \
                                      '\n Ты нашел самого умного бота, который поможет тебе конвектировать валюты.' \
                                      '\n Ты спросишь как я то делаю?. Легко, выполни эти действия через пробел и узнаешь' \
                                      '\n Введи название валюты, цену которой ты хочешь узнать' \
                                      '\n Потом введи валюту, которую хотел бы сконвектировать, А теперь введи значение первой валюты которую хочешь сконвектировать' \
                                      '\n Для помощи вот тебе доступный список валют /values'.format(message.from_user)

    bot.reply_to(message, text)



@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Пример: доллар биткоин 1000'\
           '\nВалюты которые доступны для конвертации:'
    for key in keys.keys():
        text = '\n'.join((text, key,))

    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверно ты вводишь парметры, для правильности ввода обратис к команде /values')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Будь повнимательней. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Тут сервис Телеграма поплыл, попробуй снова или подожди 5 минут:)\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote}: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)