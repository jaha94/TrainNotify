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
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException
import time
from telebot import types



def train_def(message):
    mark1 = types.KeyboardButton("Пропустить")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark1)
    msg = bot.send_message(message.chat.id, "Время отправления:", reply_markup=markup)
    bot.register_next_step_handler(msg, city_1_def)


def city_1_def(message):
    user_id = message.chat.id
    if message.text == "Пропустить":
        pass
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"""UPDATE passengers SET out_time = "{message.text}" WHERE userid = {user_id}""")
        connect.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark1 = types.KeyboardButton("Ташкент")
    mark2 = types.KeyboardButton("Навои")
    mark3 = types.KeyboardButton("Пропустить")
    markup.add(mark1, mark2, mark3)
    msg = bot.send_message(message.chat.id, "Выберите город отправления:", reply_markup=markup)
    bot.register_next_step_handler(msg, city_2_def)


def city_2_def(message):
    user_id = message.chat.id
    if message.text == "Пропустить":
        pass
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"""UPDATE passengers SET city_1 = "{message.text}" WHERE userid = {user_id}""")
        connect.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark1 = types.KeyboardButton("Ташкент")
    mark2 = types.KeyboardButton("Навои")
    mark3 = types.KeyboardButton("Пропустить")
    markup.add(mark1, mark2, mark3)
    msg = bot.send_message(message.chat.id, "Выберите город прибытия:", reply_markup=markup)
    bot.register_next_step_handler(msg, day_def)


def day_def(message):
    user_id = message.chat.id
    if message.text == "Пропустить":
        pass
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"""UPDATE passengers SET city_2 = "{message.text}" WHERE userid = {user_id}""")
        connect.commit()
    mark1 = types.KeyboardButton("Пропустить")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark1)
    msg = bot.send_message(message.chat.id, "День отправления:", reply_markup=markup)
    bot.register_next_step_handler(msg, price_def)


def price_def(message):
    user_id = message.chat.id
    if message.text == "Пропустить":
        pass
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"""UPDATE passengers SET out_day = "{message.text}" WHERE userid = {user_id}""")
        connect.commit()
    mark1 = types.KeyboardButton("Пропустить")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark1)
    msg = bot.send_message(message.chat.id, "Цена билета:", reply_markup=markup)
    bot.register_next_step_handler(msg, surname_def)


def surname_def(message):
    user_id = message.chat.id
    if message.text == "Пропустить":
        pass
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"""UPDATE passengers SET price = "{message.text}" WHERE userid = {user_id}""")
        connect.commit()
    mark1 = types.KeyboardButton("Пропустить")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark1)
    msg = bot.send_message(message.chat.id, "Фамилия:", reply_markup=markup)
    bot.register_next_step_handler(msg, name_def)


def name_def(message):
    user_id = message.chat.id
    if message.text == "Пропустить":
        pass
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"""UPDATE passengers SET pass_surname = "{message.text}" WHERE userid = {user_id}""")
        connect.commit()
    mark1 = types.KeyboardButton("Пропустить")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark1)
    msg = bot.send_message(message.chat.id, "Имя:", reply_markup=markup)
    bot.register_next_step_handler(msg, family_name_def)


def family_name_def(message):
    user_id = message.chat.id
    if message.text == "Пропустить":
        pass
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"""UPDATE passengers SET pass_name = "{message.text}" WHERE userid = {user_id}""")
        connect.commit()
    mark1 = types.KeyboardButton("Пропустить")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark1)
    msg = bot.send_message(message.chat.id, "Отчество:", reply_markup=markup)
    bot.register_next_step_handler(msg, birthday_def)


def birthday_def(message):
    user_id = message.chat.id
    if message.text == "Пропустить":
        pass
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"""UPDATE passengers SET pass_lastname = "{message.text}" WHERE userid = {user_id}""")
        connect.commit()
    mark1 = types.KeyboardButton("Пропустить")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark1)
    msg = bot.send_message(message.chat.id, "Дата рождения, в формате (01011999):", reply_markup=markup)
    bot.register_next_step_handler(msg, passport_def)


def passport_def(message):
    user_id = message.chat.id
    if message.text == "Пропустить":
        pass
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"""UPDATE passengers SET birthday = "{message.text}" WHERE userid = {user_id}""")
        connect.commit()
    mark1 = types.KeyboardButton("Пропустить")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark1)
    msg = bot.send_message(message.chat.id, "Серия и номер паспорта (AA0123456):", reply_markup=markup)
    bot.register_next_step_handler(msg, card_number_def)


def card_number_def(message):
    user_id = message.chat.id
    if message.text == "Пропустить":
        pass
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"""UPDATE passengers SET passport = "{message.text}" WHERE userid = {user_id}""")
        connect.commit()
    mark1 = types.KeyboardButton("Пропустить")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark1)
    msg = bot.send_message(message.chat.id, "Номер карты (8600022672615896):", reply_markup=markup)
    bot.register_next_step_handler(msg, card_date_def)


def card_date_def(message):
    user_id = message.chat.id
    if message.text == "Пропустить":
        pass
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"""UPDATE passengers SET card = "{message.text}" WHERE userid = {user_id}""")
        connect.commit()
    mark1 = types.KeyboardButton("Пропустить")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark1)
    msg = bot.send_message(message.chat.id, "Срок действия карты (0227):", reply_markup=markup)
    bot.register_next_step_handler(msg, card_date_def_1)


def card_date_def_1(message):
    user_id = message.chat.id
    if message.text == "Пропустить":
        pass
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"""UPDATE passengers SET card_date = "{message.text}" WHERE userid = {user_id}""")
        connect.commit()
    welcome(message)


token = '5607606298:AAFnys3MvB6A5NQgWspYTCja93q3Btl-s1A'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.chat.id
    print("подключился пользователь ", user_id)
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS passengers(
        userid TEXT UNIQUE,
        out_time TEXT,
        city_1 TEXT,
        city_2 TEXT,
        out_day TEXT,
        price TEXT,
        pass_surname TEXT,
        pass_name TEXT,
        pass_lastname TEXT,
        birthday TEXT,
        passport TEXT,
        card TEXT,
        card_date TEXT
        )""")
    try:
        cursor.execute(f"""INSERT INTO passengers (userid) VALUES ({user_id})""")
    except:
        pass
    connect.commit()
    connect.close()

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Пассажир")
    item2 = types.KeyboardButton("Покупка билета")
    markup.add(item1, item2)
    bot.send_message(message.chat.id,
                     "<b>{0.first_name}</b>\nЭто главное меню бота для покупки билетов <b>{1.first_name}</b>".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == "Пассажир":
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute(f"""SELECT * FROM passengers WHERE userid = {message.chat.id}""")
            c = cursor.fetchone()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mark1 = types.KeyboardButton("Добавить пассажира")
            mark2 = types.KeyboardButton("На главную")
            markup.add(mark1, mark2)
            bot.send_message(message.chat.id, f"Время отправления: {c[1]}\n"
                                              f"Город отправления: {c[2]}\n"
                                              f"Город прибытия: {c[3]}\n"
                                              f"День прибытия: {c[4]}\n"
                                              f"Цена билета: {c[5]}\n"
                                              f"Фамилия: {c[6]}\n"
                                              f"Имя: {c[7]}\n"
                                              f"Отчество: {c[8]}\n"
                                              f"Дата рождения: {c[9]} "
                                              f"Паспорт: {c[10]}\n"
                                              f"\n"
                                              f"Номер карты: {c[11]}\n"
                                              f"Срок действия карты: {c[12]}", reply_markup=markup)

        if message.text == "Добавить пассажира":
            train_def(message)

        elif message.text == "На главную":
            welcome(message)
        elif message.text == "Покупка билета":
            train_buy_gif = open('Files/all-aboard-train.mp4', 'rb')
            bot.send_video(message.chat.id, train_buy_gif)
            while True:
                try:
                    connect = sqlite3.connect('users.db')
                    cursor = connect.cursor()
                    cursor.execute(f"""SELECT * FROM passengers WHERE userid = {message.chat.id}""")
                    b = cursor.fetchone()
                    train = b[1]
                    city_1 = b[2]
                    city_2 = b[3]
                    day = b[4]
                    price = b[5]
                    surname = b[6]
                    name = b[7]
                    family_name = b[8]
                    birthday = b[9]
                    passport = b[10]

                    card_number = b[11]
                    card_date = b[12]

                    site_login = '998903465499' #'axralovm@mail.ru'
                    site_password = 'jahangir1' #'gv6jo54kh'

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

                    driver.find_element(By.XPATH, "//input[@placeholder='Введите e-mail или телефон (998000000000)']").send_keys(site_login)
                    driver.find_element(By.XPATH, "//input[@placeholder='Введите пароль']").send_keys(
                        site_password)
                    driver.find_element(By.XPATH, "(//button[contains(text(),'ВОЙТИ')])[1]").click()
                    print('Авторизовались')
                    time.sleep(1)
                    driver.find_element(By.XPATH, "//span[contains(text(),'" + city_1 + "')]").click()
                    time.sleep(1)
                    driver.find_element(By.XPATH, "//span[contains(text(),'" + city_2 + "')]").click()
                    time.sleep(1)
                    driver.find_element(By.XPATH, "//div[@class='datepicker__layer']").click()
                    driver.find_element(By.XPATH, "//div[text()='" + day + "']").click()
                    time.sleep(1)
                    driver.find_element(By.XPATH, "//button[contains(text(),'Найти')]").click()
                    bot.send_message(message.chat.id, "Перешли к списку поездов")
                    a = 0
                except Exception as ex:
                    bot.send_message(message.chat.id, "Ошибка, добавьте пассажира заново, и повторите поиск")
                    welcome(message)
                    driver.close()
                    driver.quit()
                    break
                finally:
                    while True:
                        try:
                            driver.implicitly_wait(10)
                            action = ActionChains(driver)

                            driver.implicitly_wait(5)

                            while True:
                                driver.implicitly_wait(5)
                                try:
                                    driver.implicitly_wait(3)
                                    driver.find_element(By.XPATH,
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
                                    except:
                                        driver.implicitly_wait(4)
                                        driver.get(url="https://chipta.railway.uz/ru/pages/trains-page")
                                        driver.find_element(By.XPATH,
                                                                    "//button[contains(text(),'Найти')]").click()



                            driver.execute_script("window.scrollTo(0, 300);")
                            time.sleep(1)
                            driver.find_element(By.XPATH,
                                                               "//div[contains(text(),'" + train + "')]/following::span[contains(text(),'" + price + "')]/following::a[@class='train-select btn']").click()
                            buying = driver.find_element(By.XPATH,
                                                         "//button[contains(text(),'Продолжить')]").is_displayed()

                            driver.find_element(By.XPATH, "//button[contains(text(),'Продолжить')]").click()
                            print('Выбрали поезд')
                            try:
                                driver.find_element(By.XPATH,
                                                    "//input[@placeholder='Введите e-mail или телефон (998000000000)']").send_keys(
                                    site_login)
                                driver.find_element(By.XPATH, "//input[@placeholder='Введите пароль']").send_keys(
                                    site_password)
                                driver.find_element(By.XPATH, "(//button[contains(text(),'ВОЙТИ')])[1]").click()
                                print('Авторизовались')
                                time.sleep(1)
                                # else:
                                #     pass
                            except:
                                pass

                            driver.find_element(By.XPATH,
                                                        "(//strong[contains(text(),'" + price + "')])").click()
                            driver.find_element(By.XPATH,
                                                        "(//strong[contains(text(),'" + price + "')]/following::strong[contains(text(),'" + price + "')])").click()
                            # test = driver.find_element(By.XPATH, "//span[contains(text(),'Направление движения поезда')]").is_displayed()
                            start = driver.find_element(By.XPATH, "(//div[@class='info__time'])[1]")
                            global start_time
                            start_time = start.text
                            driver.implicitly_wait(20)
                            driver.find_element(By.XPATH, "//span[text()=' вагон']")
                            driver.execute_script("window.scrollTo(0, 3000);")
                            time.sleep(1)
                            place_1 = driver.find_element(By.CLASS_NAME, 'free').click()
                            driver.execute_script("window.scrollTo(0, 3000);")
                            time.sleep(1)
                            driver.find_element(By.XPATH, "//input[@placeholder='Фамилия']").send_keys(
                                surname)
                            driver.find_element(By.XPATH, "//input[@placeholder='Имя']").send_keys(name)
                            driver.find_element(By.XPATH,
                                                                    "//input[@placeholder='Отчество']").send_keys(
                                family_name)
                            driver.find_element(By.XPATH,
                                                                 "//input[@placeholder='__ /__ /____']").send_keys(
                                birthday)
                            driver.find_element(By.XPATH, "//div[@class='gender__man']").click()
                            driver.find_element(By.XPATH,
                                                                 "//input[@placeholder='__ - ____']").send_keys(
                                passport)
                            driver.find_element(By.XPATH, "(//span[@class='ng-arrow-wrapper'])[4]").click()
                            driver.find_element(By.XPATH,
                                                                "//span[contains(text(),'г. Ташкент')]").click()
                            driver.find_element(By.XPATH, "//button[contains(text(),'Продолжить')]").click()
                            print('Забронировали билет')
                            driver.implicitly_wait(5)
                            time.sleep(5)
                            driver.execute_script("window.scrollTo(0, 3000);")
                            time.sleep(1)
                            driver.find_element(By.XPATH, "//span[@class='checkbox-rect']").click()
                            driver.find_element(By.XPATH, "//img[@alt='Payme logo']").click()
                            driver.find_element(By.XPATH,
                                                       "//input[@placeholder='____ ____ ____ ____']").send_keys(
                                card_number)
                            driver.find_element(By.XPATH, "//input[@placeholder='__ /__']").send_keys(
                                card_date)
                            driver.find_element(By.XPATH,
                                                               "//button[contains(text(),'Оплатить')]").click()
                            time.sleep(3)
                            ticket = driver.find_element(By.XPATH, "//div[@class='part__total']//span[2]")
                            ticket_price = ticket.text

                            def sms_send_def(message):
                                try:
                                    print("начали")
                                    driver.implicitly_wait(5)
                                    sms_code = message.text
                                    driver.find_element(By.XPATH, "//input[@placeholder='_ _ _ _ _ _']").clear()
                                    driver.find_element(By.XPATH, "//input[@placeholder='_ _ _ _ _ _']").send_keys(
                                        sms_code)
                                    time.sleep(2)
                                    driver.find_element(By.XPATH, "//button[contains(text(),'Оплатить')]").click()
                                    time.sleep(6)
                                    driver.find_element(By.XPATH,
                                                        "//a[contains(text(),'Распечатать заказ/билет')]").click()
                                    time.sleep(5)
                                    list_of_files = glob.glob(
                                        r'C:\Users\Jahangir.Kurbanaliev\Downloads\*')
                                    latest_file = max(list_of_files, key=os.path.getctime)
                                    print(latest_file)
                                    ticket_file = open(latest_file, 'rb')
                                    bot.send_document(message.chat.id, ticket_file)

                                except Exception as ex:
                                    try:
                                        driver.implicitly_wait(5)
                                        if driver.find_element(By.XPATH, "//div[contains(text(),'Введенный вами SMS код неверный пожалуйста попробу')]").is_displayed() == True:
                                            confirm_message = bot.send_message(message.chat.id, "Код неверный. Проверьте и введите заново.")
                                            bot.register_next_step_handler(confirm_message, sms_send_def)
                                        else:
                                            bot.send_message(message.chat.id, "Бронь закончилась, начался новый поиск.")
                                    except:
                                        bot.send_message(message.chat.id, "Ошибка при оплате, начинаем поиск заново.")
                                        return

                            # bot.send_message(message.chat.id, ("Билет забронирован, на время: " + start_time + "\nПо цене: " + ticket_price + "\nНа пассажира: " + name))
                            confirm_message = bot.send_message(message.chat.id, ("Билет забронирован, на время: " + start_time + "\nПо цене: " + ticket_price + "\nНа пассажира: " + name + "\n\nВведите код из СМС для оплаты билета"))
                            bot.register_next_step_handler(confirm_message, sms_send_def)
                            while True:
                                try:
                                    driver.find_element(By.XPATH, "//div[@class='timer__info']").is_displayed()
                                    time.sleep(1)
                                except:
                                    time.sleep(15)
                                    break
                            driver.find_element(By.XPATH, "(//div[contains(text(),'Если скачивание документа автоматически не началас')])[1]")
                            bot.send_message(message.chat.id, ("Процесс покупки билета окончен успешно. Хорошей поездки."))
                            driver.close()
                            driver.quit()
                            a = 1

                        except NoSuchElementException as exs:
                            print("ошибка", exs)
                            driver.get(url="https://chipta.railway.uz/ru/pages/trains-page")

                        except ElementClickInterceptedException as icd:
                            print("ошибка", icd)
                            driver.get(url="https://chipta.railway.uz/ru/pages/trains-page")

                        except StaleElementReferenceException as sere:
                            print("ошибка sere", sere)
                            driver.get(url="https://chipta.railway.uz/ru/pages/trains-page")

                        except ElementNotInteractableException as intr:
                            print("ошибка intr", intr)
                            driver.get(url="https://chipta.railway.uz/ru/pages/trains-page")

                        except Exception as ex:
                            print('Ошибка', ex)
                            bot.send_message(message.chat.id, "Ошибка, добавьте пассажира заново, и повторите поиск")
                            welcome(message)
                            driver.close()
                            driver.quit()
                            break
                        # finally:
                        #     print('11232')
                        #     time.sleep(1)
                        #     driver.close()
                        #     driver.quit()
                        #     break
                        if a ==1:
                            break
                    break

        elif message.text == "id":
            bot.send_message(message.chat.id, message)


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
