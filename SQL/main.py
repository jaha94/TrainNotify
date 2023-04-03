import random
import plyer
import telebot
import sqlite3
import glob
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from telebot import types

train = ''
city_1 = ''
city_2 = ''
day = ''
price = ''
surname = ''
name = ''
family_name = ''
birthday = ''
passport = ""

card_number = ""
card_date = ""


def train_def(message):
    msg = bot.send_message(message.chat.id, "Время отправления:")
    bot.register_next_step_handler(msg, city_1_def)


def city_1_def(message):
    global train
    train = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark1 = types.KeyboardButton("Ташкент")
    mark2 = types.KeyboardButton("Навои")
    markup.add(mark1, mark2)
    msg = bot.send_message(message.chat.id, "Выберите город отправления:", reply_markup=markup)
    bot.register_next_step_handler(msg, city_2_def)


def city_2_def(message):
    global city_1
    city_1 = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark1 = types.KeyboardButton("Ташкент")
    mark2 = types.KeyboardButton("Навои")
    markup.add(mark1, mark2)
    msg = bot.send_message(message.chat.id, "Выберите город прибытия:", reply_markup=markup)
    bot.register_next_step_handler(msg, day_def)


def day_def(message):
    global city_2
    city_2 = message.text
    msg = bot.send_message(message.chat.id, "День отправления:")
    bot.register_next_step_handler(msg, price_def)
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # mark1 = types.KeyboardButton("Ташкент")
    # mark2 = types.KeyboardButton("Навои")
    # markup.add(mark1, mark2)
    # msg = bot.send_message(message.chat.id, "Выберите город отправления:", reply_markup=markup)
    # bot.register_next_step_handler(msg, city_2_def)


def price_def(message):
    global day
    day = message.text
    msg = bot.send_message(message.chat.id, "Цена билета:")
    bot.register_next_step_handler(msg, surname_def)


def surname_def(message):
    global price
    price = message.text
    msg = bot.send_message(message.chat.id, "Фамилия:")
    bot.register_next_step_handler(msg, name_def)


def name_def(message):
    global surname
    surname = message.text
    msg = bot.send_message(message.chat.id, "Имя:")
    bot.register_next_step_handler(msg, family_name_def)


def family_name_def(message):
    global name
    name = message.text
    msg = bot.send_message(message.chat.id, "Отчество:")
    bot.register_next_step_handler(msg, birthday_def)


def birthday_def(message):
    global family_name
    family_name = message.text
    msg = bot.send_message(message.chat.id, "Дата рождения, в формате (01011999):")
    bot.register_next_step_handler(msg, passport_def)


def passport_def(message):
    global birthday
    birthday = message.text
    msg = bot.send_message(message.chat.id, "Серия и номер паспорта (AA0123456):")
    bot.register_next_step_handler(msg, card_number_def)


def card_number_def(message):
    global passport
    passport = message.text
    msg = bot.send_message(message.chat.id, "Номер карты (8600022672615896):")
    bot.register_next_step_handler(msg, card_date_def)


def card_date_def(message):
    global card_number
    card_number = message.text
    msg = bot.send_message(message.chat.id, "Срок действия карты (0227):")
    bot.register_next_step_handler(msg, card_date_def_1)


def card_date_def_1(message):
    global card_date
    card_date = message.text
    welcome(message)


token = '5583314167:AAHhVtfNfusA-68JeoWFrggfTUE7Vs4ow5Y'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.chat.id
    # sti = open('Files/welcome.webp', 'rb')
    # bot.send_sticker(message.chat.id, sti)
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
        name TEXT,
        id INTEGER,
        surname TEXT
        )""")
    # list_of_files = glob.glob(
    #     r'C:\Users\Jaha\Downloads\*')  # * means all if need specific format then *.csv
    # latest_file = max(list_of_files, key=os.path.getctime)
    # print(latest_file)
    # ticket_file = open(latest_file, 'rb')
    # bot.send_document(message.chat.id, ticket_file)
    # cursor.execute(f"SELECT id FROM login_id WHERE id = {user_id}")
    # data = cursor.fetchone()
    # if data is None:
    #     user_id = [message.chat.id]
    #     cursor.execute("INSERT INTO login_id VALUES(?);", user_id)
    #     connect.commit()
    connect.commit()
    connect.close()

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Список пассажиров")
    item2 = types.KeyboardButton("🖐 Как дела?")
    item3 = types.KeyboardButton("Покупка билета")
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id,
                     "<b>{0.first_name}</b>\nЭто главное меню бота для покупки билетов <b>{1.first_name}</b>".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == "Список пассажиров":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mark1 = types.KeyboardButton("Добавить пассажира")
            mark2 = types.KeyboardButton("На главную")
            markup.add(mark1, mark2)
            bot.send_message(message.chat.id, f"Время отправления: {train}\n"
                                              f"Город отправления: {city_1}\n"
                                              f"Город прибытия: {city_2}\n"
                                              f"День прибытия: {day}\n"
                                              f"Цена билета: {price}\n"
                                              f"Фамилия: {surname}\n"
                                              f"Имя: {name}\n"
                                              f"Отчество: {family_name}\n"
                                              f"Дата рождения: {birthday}"
                                              f"Паспорт: {passport}\n"
                                              f"\n"
                                              f"Номер карты: {card_number}\n"
                                              f"Срок действия карты: {card_date}", reply_markup=markup)
            # connect = sqlite3.connect('users.db')
            # cursor = connect.cursor()
            # cursor.execute("""SELECT id FROM login_id""")
            # passengers = cursor.fetchall()
            # print(passengers)
            # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            # bot.send_message(message.chat.id, f"Список пассажиров: {passengers}", reply_markup=markup)
            # connect.close()
        if message.text == "Добавить пассажира":
            train_def(message)
            # connect = sqlite3.connect('users.db')
            # cursor = connect.cursor()
            #
            # connect.commit()
            # bot.send_message(message.chat.id, "Готово")
        elif message.text == "🖐 Как дела?":

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо11", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, "Отлично, как сам?", reply_markup=markup)
            print(item1, item2)
        elif message.text == "На главную":
            welcome(message)
        elif message.text == "Покупка билета":
            while True:
                try:
                    site_login = 'axralovm@mail.ru'
                    site_password = 'gv6jo54kh'

                    train_buy_gif = open('Files/all-aboard-train.mp4', 'rb')
                    bot.send_video(message.chat.id, train_buy_gif)

                    options = Options()
                    options.add_argument("window-size=1280x800")
                    options.add_argument("--start-maximized")
                    options.add_argument("--disable-blink-features=AutomationControlled")
                    # options.add_argument("--headless")

                    buying = False
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                    action = ActionChains(driver)
                    driver.implicitly_wait(10)
                    driver.get(url='https://chipta.railway.uz/ru/auth/login')

                    login = driver.find_element(By.XPATH,
                                                "//input[@placeholder='Введите e-mail или телефон (998000000000)']").send_keys(
                        site_login)
                    password = driver.find_element(By.XPATH, "//input[@placeholder='Введите пароль']").send_keys(
                        site_password)
                    confirm = driver.find_element(By.XPATH, "(//button[contains(text(),'ВОЙТИ')])[1]").click()
                    print('Авторизовались')
                    otkuda = driver.find_element(By.XPATH, "//span[contains(text(),'" + city_1 + "')]").click()
                    kuda = driver.find_element(By.XPATH, "//span[contains(text(),'" + city_2 + "')]").click()
                    date_picker = driver.find_element(By.XPATH, "//div[@class='datepicker__layer']").click()
                    data = driver.find_element(By.XPATH, "//div[text()='" + day + "']").click()
                    time.sleep(1)
                    find_button = driver.find_element(By.XPATH, "//button[contains(text(),'Найти')]").click()
                    bot.send_message(message.chat.id, "Перешли к списку поездов")
                    a = 1
                except Exception as ex:
                    bot.send_message(message.chat.id, "Ошибка, добавьте пассажира заново, и повторите поиск")
                    welcome(message)
                    driver.close()
                    driver.quit()
                    a = 0
                    break
                if a == 1:
                    while True:
                        try:
                            driver.implicitly_wait(10)
                            action = ActionChains(driver)

                            check = driver.implicitly_wait(5)

                            while True:
                                driver.implicitly_wait(5)
                                try:
                                    ticket_end = driver.implicitly_wait(3)
                                    ticket_end = driver.find_element(By.XPATH,
                                                                     "//div[contains(text(),'" + train + "')]/following::div[@class='train-old']").is_displayed()
                                    driver.close()
                                    driver.quit()
                                    bot.send_message(message.chat.id, (
                                            "Продажа билета по условиям:\n" + city_1 + " --->> " + city_2 + "\nДля: " + name + " " + surname + "\nПо цене: " + price + "\nНа поезд " + train + " завершена."))
                                    break
                                except NoSuchElementException:
                                    try:
                                        ticket_price = driver.find_element(By.XPATH,
                                                                           "//div[contains(text(),'" + train + "')]/following::span[contains(text(),'" + price + "')]").is_displayed()
                                        break
                                    except NoSuchElementException:
                                        driver.implicitly_wait(5)
                                        check = driver.find_element(By.XPATH,
                                                                    "//button[contains(text(),'Найти')]").click()

                            driver.execute_script("window.scrollTo(0, 300);")
                            time.sleep(1)
                            ticket_price = driver.find_element(By.XPATH,
                                                               "//div[contains(text(),'" + train + "')]/following::span[contains(text(),'" + price + "')]/following::a[@class='train-select btn']").click()
                            buying = driver.find_element(By.XPATH,
                                                         "//button[contains(text(),'Продолжить')]").is_displayed()

                            to_buying = driver.find_element(By.XPATH, "//button[contains(text(),'Продолжить')]").click()
                            print('Выбрали поезд')

                            place = driver.find_element(By.XPATH,
                                                        "(//strong[contains(text(),'" + price + "')])").click()
                            place = driver.find_element(By.XPATH,
                                                        "(//strong[contains(text(),'" + price + "')]/following::strong[contains(text(),'" + price + "')])").click()
                            # test = driver.find_element(By.XPATH, "//span[contains(text(),'Направление движения поезда')]").is_displayed()
                            start = driver.find_element(By.XPATH, "(//div[@class='info__time'])[1]")
                            global start_time
                            start_time = start.text
                            find_text = driver.implicitly_wait(20)
                            find_text = driver.find_element(By.XPATH, "//span[text()=' вагон']")
                            driver.execute_script("window.scrollTo(0, 3000);")
                            time.sleep(1)
                            place_1 = driver.find_element(By.CLASS_NAME, 'free').click()
                            driver.execute_script("window.scrollTo(0, 3000);")
                            time.sleep(1)
                            surname_input = driver.find_element(By.XPATH, "//input[@placeholder='Фамилия']").send_keys(
                                surname)
                            name_input = driver.find_element(By.XPATH, "//input[@placeholder='Имя']").send_keys(name)
                            family_name_input = driver.find_element(By.XPATH,
                                                                    "//input[@placeholder='Отчество']").send_keys(
                                family_name)
                            birthday_input = driver.find_element(By.XPATH,
                                                                 "//input[@placeholder='__ /__ /____']").send_keys(
                                birthday)
                            gender = driver.find_element(By.XPATH, "//div[@class='gender__man']").click()
                            passport_input = driver.find_element(By.XPATH,
                                                                 "//input[@placeholder='__ - ____']").send_keys(
                                passport)
                            arrow = driver.find_element(By.XPATH, "(//span[@class='ng-arrow-wrapper'])[4]").click()
                            passport_from = driver.find_element(By.XPATH,
                                                                "//span[contains(text(),'г. Ташкент')]").click()
                            keep = driver.find_element(By.XPATH, "//button[contains(text(),'Продолжить')]").click()
                            print('Забронировали билет')
                            driver.implicitly_wait(5)
                            time.sleep(5)
                            driver.execute_script("window.scrollTo(0, 3000);")
                            time.sleep(1)
                            pay = driver.find_element(By.XPATH, "//span[@class='checkbox-rect']").click()
                            payme = driver.find_element(By.XPATH, "//img[@alt='Payme logo']").click()
                            card = driver.find_element(By.XPATH,
                                                       "//input[@placeholder='____ ____ ____ ____']").send_keys(
                                card_number)
                            card_1 = driver.find_element(By.XPATH, "//input[@placeholder='__ /__']").send_keys(
                                card_date)
                            card_confirm = driver.find_element(By.XPATH,
                                                               "//button[contains(text(),'Оплатить')]").click()
                            time.sleep(3)
                            ticket = driver.find_element(By.XPATH, "//div[@class='part__total']//span[2]")
                            ticket_price = ticket.text
                            confirm_message = bot.send_message(message.chat.id, (
                                    "Билет забронирован, на время: " + start_time + "\nПо цене: " + ticket_price + "\nНа пассажира: " + name))
                            #confirm_message = bot.send_message(message.chat.id, ("Билет забронирован, на время: " + start_time + "\nПо цене: " + ticket_price + "\nНа пассажира: " + name + "\n\nВведите код из СМС для оплаты билета"))
                            #bot.register_next_step_handler(confirm_message, sms_send_def)
                            time.sleep(500)

                            def sms_send_def(message):
                                try:
                                    print("начали")
                                    driver.implicitly_wait(20)
                                    sms_code = message.text
                                    driver.find_element(By.XPATH, "//input[@placeholder='_ _ _ _ _ _']").send_keys(
                                        sms_code)
                                    time.sleep(5)
                                    driver.find_element(By.XPATH, "//button[contains(text(),'Оплатить')]").click()
                                    driver.find_element(By.XPATH,
                                                        "//a[contains(text(),'Распечатать заказ/билет')]").click
                                    list_of_files = glob.glob(
                                        r'C:\Users\Jaha\Downloads\*')  # * means all if need specific format then *.csv
                                    latest_file = max(list_of_files, key=os.path.getctime)
                                    print(latest_file)
                                    ticket_file = open(latest_file, 'rb')
                                    bot.send_document(message.chat.id, ticket_file)

                                except Exception as ex:
                                    bot.send_message(message.chat.id, "Код неверный, начался повторный поиск билета.")

                            # try:
                            #     driver.find_element(By.XPATH, "//button[contains(text(),'Скачать')]").is_displayed()
                            #     time.sleep(10)
                            # except Exception as exs:
                            #     time.sleep(10)
                            #     print('no')

                            # print(start_time, ticket_price)



                            #print('Перешли к оплате')
                            # if b == 0:
                            #     break
                            #     message_sms = bot.send_message(message.chat.id, (
                            #         "Введите код из СМС для оплаты билета"))

                            # plyer.notification.notify(message=('Необходимо оплатить билет!!'))


                        except NoSuchElementException as exs:
                            print("ошибка", exs)
                            driver.get(url="https://chipta.railway.uz/ru/pages/trains-page")

                        except Exception as ex:
                            print('Ошибка', ex)
                            bot.send_message(message.chat.id, "Ошибка, добавьте пассажира заново, и повторите поиск")
                            welcome(message)
                            driver.close()
                            driver.quit()
                            break

                            # driver.close()
                            # driver.start_session({})
                        # finally:
                        #     time.sleep(1)
                        #     driver.close()
                        #     driver.quit()
        elif message.text == "id":
            bot.send_message(message.chat.id, message)
        else:
            bot.send_message(message.chat.id, "Даже не знаю что ответить.")


# def sms_def(message):
#



@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, "Вот и отличненько 😊")
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, "Бывает 😕")

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🖐 Как дела?",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ТЕСТОВОЕ УВЕДОМЛЕНИЕ")

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)

#bot.polling(none_stop=True)
