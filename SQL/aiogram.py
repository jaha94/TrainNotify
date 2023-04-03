import random
import plyer
import telebot
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from telebot import types

token = '5583314167:AAHhVtfNfusA-68JeoWFrggfTUE7Vs4ow5Y'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.chat.id
    sti = open('Files/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
        name TEXT,
        id INTEGER,
        surname TEXT
        )""")
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
                     "Добро пожаловать, <b>{0.first_name}</b>\nЯ <b>{1.first_name}</b>, бот для покупки билетов на поезд".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == "Список пассажиров":
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute("""SELECT id FROM login_id""")
            passengers = cursor.fetchall()
            print(passengers)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mark1 = types.KeyboardButton("Добавить пассажира")
            markup.add(mark1)
            bot.send_message(message.chat.id, f"Список пассажиров: {passengers}", reply_markup=markup)
            connect.close()
        if message.text == "Добавить пассажира":
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()

            connect.commit()
            bot.send_message(message.chat.id, "Готово")
        elif message.text == "🖐 Как дела?":

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо11", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, "Отлично, как сам?", reply_markup=markup)
            print(item1, item2)
        elif message.text == "Покупка билета":
            try:
                bot.stop_polling()
                bot.send_message(message.chat.id, "Логин сайта: ")
                site_login = message.text
            finally:
                bot.send_message(message.chat.id, f"Логин сайта: {site_login}")
            site_login = '998903465499'
            site_password = 'jahangir1'

            train = 'Ф'
            city_1 = 'Ташкент'
            city_2 = 'Навои'
            day = '29'
            price = '141000'
            surname = 'ALIYEV'
            name = 'ABDUVOXID'
            family_name = 'ABDUVAXOBOVICH'
            birthday = '09061984'
            passport = "AB4213125"

            card_number = "8600022689611524"
            card_date = "0926"

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Ташкент")
            item2 = types.KeyboardButton("Навои")
            markup.add(item1, item2)
            bot.send_message(message.chat.id, "Город отправления", reply_markup=markup)
            if message.text == "Ташкент":
                city_1 = "Ташкент"
            elif message.text == "Навои":
                city_1 = "Навои"

            train_buy_gif = open('Files/all-aboard-train.mp4', 'rb')
            bot.send_video(message.chat.id, train_buy_gif)

            options = Options()
            options.add_argument("window-size=1280x800")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")
            # options.add_argument("--headless")
            url = "https://chipta.railway.uz/ru/pages/trains-page"
            buying = False
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            action = ActionChains(driver)
            driver.implicitly_wait(10)
            driver.get(url='https://chipta.railway.uz/ru/auth/login')

            login = driver.find_element(By.XPATH, "(//input[@id='usr'])[1]").send_keys(site_login)
            password = driver.find_element(By.XPATH, "(//input[@placeholder='Введите пароль'])[1]").send_keys(
                site_password)
            confirm = driver.find_element(By.XPATH, "(//button[contains(text(),'ВОЙТИ')])[1]").click()
            print('Авторизовались')
            otkuda = driver.find_element(By.XPATH, "//span[contains(text(),'" + city_1 + "')]").click()
            kuda = driver.find_element(By.XPATH, "//span[contains(text(),'" + city_2 + "')]").click()
            date_picker = driver.find_element(By.XPATH, "//div[@class='datepicker__layer']").click()
            data = driver.find_element(By.XPATH, "//div[text()='" + day + "']").click()
            time.sleep(1)
            find_button = driver.find_element(By.XPATH, "//button[contains(text(),'Найти')]").click()
            print("Перешли к списку поездов")
            while True:
                try:
                    driver.implicitly_wait(10)
                    action = ActionChains(driver)

                    check = driver.implicitly_wait(5)

                    while True:
                        try:
                            ticket_end = driver.implicitly_wait(1)
                            ticket_end = driver.find_element(By.XPATH,
                                                             "//span[contains(text(),'" + train + "')]/following::div[@class='train-old']").is_displayed()
                            driver.close()
                            driver.quit()
                            bot.send_message(message.chat.id, (
                                    "Продажа билета по условиям:\n" + city_1 + " --->> " + city_2 + "\nДля: " + name + " " + surname + "\nПо цене: " + price + "\nНа поезд " + train + " завершена."))
                            break
                        except NoSuchElementException:
                            try:
                                ticket_price = driver.find_element(By.XPATH,
                                                                   "//span[contains(text(),'" + train + "')]/following::span[contains(text(),'" + price + "')]").is_displayed()
                                break
                            except NoSuchElementException:
                                check = driver.find_element(By.XPATH, "//button[contains(text(),'Найти')]").click()

                    driver.execute_script("window.scrollTo(0, 300);")
                    time.sleep(1)
                    ticket_price = driver.find_element(By.XPATH,
                                                       "//span[contains(text(),'" + train + "')]/following::span[contains(text(),'" + price + "')]/following::a[@class='train-select btn']").click()
                    buying = driver.find_element(By.XPATH, "//button[contains(text(),'Продолжить')]").is_displayed()

                    to_buying = driver.find_element(By.XPATH, "//button[contains(text(),'Продолжить')]").click()
                    print('Выбрали поезд')

                    place = driver.find_element(By.XPATH, "(//strong[contains(text(),'" + price + "')])").click()
                    # test = driver.find_element(By.XPATH, "//span[contains(text(),'Направление движения поезда')]").is_displayed()
                    start = driver.find_element(By.XPATH, "(//div[@class='info__time'])[1]")
                    start_time = start.text
                    find_text = driver.implicitly_wait(20)
                    find_text = driver.find_element(By.XPATH, "//span[text()=' вагон']")
                    driver.execute_script("window.scrollTo(0, 3000);")
                    time.sleep(1)
                    place_1 = driver.find_element(By.CLASS_NAME, 'free').click()
                    driver.execute_script("window.scrollTo(0, 3000);")
                    time.sleep(1)
                    surname_input = driver.find_element(By.XPATH, "//input[@placeholder='Фамилия']").send_keys(surname)
                    name_input = driver.find_element(By.XPATH, "//input[@placeholder='Имя']").send_keys(name)
                    family_name_input = driver.find_element(By.XPATH, "//input[@placeholder='Отчество']").send_keys(
                        family_name)
                    birthday_input = driver.find_element(By.XPATH, "//input[@placeholder='__ /__ /____']").send_keys(
                        birthday)
                    gender = driver.find_element(By.XPATH, "//div[@class='gender__man']").click()
                    passport_input = driver.find_element(By.XPATH, "//input[@placeholder='__ - ____']").send_keys(
                        passport)
                    arrow = driver.find_element(By.XPATH, "(//span[@class='ng-arrow-wrapper'])[4]").click()
                    passport_from = driver.find_element(By.XPATH, "//span[contains(text(),'г. Ташкент')]").click()
                    keep = driver.find_element(By.XPATH, "//button[contains(text(),'Продолжить')]").click()
                    print('Забронировали билет')
                    driver.implicitly_wait(5)
                    time.sleep(5)
                    driver.execute_script("window.scrollTo(0, 3000);")
                    time.sleep(1)
                    pay = driver.find_element(By.XPATH, "//span[@class='checkbox-rect']").click()
                    payme = driver.find_element(By.XPATH, "//img[@alt='Payme logo']").click()
                    card = driver.find_element(By.XPATH, "//input[@placeholder='____ ____ ____ ____']").send_keys(
                        card_number)
                    card_1 = driver.find_element(By.XPATH, "//input[@placeholder='__ /__']").send_keys(card_date)
                    card_confirm = driver.find_element(By.XPATH, "//button[contains(text(),'Оплатить')]").click()
                    time.sleep(3)
                    ticket = driver.find_element(By.XPATH, "//div[@class='part__total']//span[2]")
                    ticket_price = ticket.text

                    # print(start_time, ticket_price)
                    bot.send_message(message.chat.id, (
                            "Билет топилди, вакти: " + start_time + "\nНархи: " + ticket_price + "\nКимга: " + name))
                    print('Перешли к оплате')
                    plyer.notification.notify(message=('Необходимо оплатить билет!!'))
                    time.sleep(600)

                except NoSuchElementException:
                    driver.get(url=url)

                except Exception as ex:
                    print('Ошибка', ex)
                    break

                    # driver.close()
                    # driver.start_session({})


                finally:
                    time.sleep(1)
                    # driver.close()
                    # driver.quit()
        elif message.text == "id":
            bot.send_message(message.chat.id, message)
        else:
            bot.send_message(message.chat.id, "Даже не знаю что ответить.")


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
