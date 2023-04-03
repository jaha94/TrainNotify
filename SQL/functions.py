import telebot

token = '5583314167:AAHhVtfNfusA-68JeoWFrggfTUE7Vs4ow5Y'
bot = telebot.TeleBot(token)


def train_def(message):
    train_1 = bot.send_message(message.chat.id, "Введите номер поезда:")
    bot.register_next_step_handler(train_1, city_12)


def city_12(message):
    train = message.text
    print(train)
    bot.send_message(message.chat.id, "огого")
    # train = 'Ф'
    #         city_1 = 'Ташкент'
    #         city_2 = 'Навои'
    #         day = '29'
    #         price = '141000'
    #         surname = 'ALIYEV'
    #         name = 'ABDUVOXID'
    #         family_name = 'ABDUVAXOBOVICH'
    #         birthday = '09061984'
    #         passport = "AB4213125"
    #
    #         card_number = "8600022689611524"
    #         card_date = "0926"
