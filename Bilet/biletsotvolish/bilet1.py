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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException, InvalidSelectorException
import time
from telebot import types
from bot_token import *
bot = telebot.TeleBot(token)



def train_def(message):
    mark1 = types.KeyboardButton("Пропустить")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(mark1)
    msg = bot.send_message(message.chat.id, "Отправьте информацию о пассажире в виде: информация о поезде/город отправления/город прибытия/день отправления/цена билета/серия и номер паспорта/номер карты/срок годности карты:", reply_markup=markup)
    bot.register_next_step_handler(msg, city_1_def)


def city_1_def(message):
    user_id = message.chat.id
    text_old = message.text
    text = text_old.split('/')
    if message.text == "Пропустить":
        pass
    else:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute("""
                    UPDATE passenger SET 
                         out_time = ?,
                         city_1 = ?,
                         city_2 = ?,
                         out_day = ?,
                         price = ?,
                         passport = ?,
                         card = ?,
                         card_date = ?
                    WHERE userid = ?
                       """,
                         (*text, user_id))

        connect.commit()
    bot.send_message(message.chat.id, "Пассажир добавлен")
    welcome(message)

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.chat.id
    print("подключился пользователь ", user_id)
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS passenger(
        userid TEXT UNIQUE,
        out_time TEXT,
        city_1 TEXT,
        city_2 TEXT,
        out_day TEXT,
        price TEXT,
        passport TEXT,
        card TEXT,
        card_date TEXT
        )""")
    try:
        cursor.execute(f"""INSERT INTO passenger (userid) VALUES ({user_id})""")
    except:
        pass
    connect.commit()
    connect.close()

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Пассажир")
    item2 = types.KeyboardButton("Покупка билета")
    item3 = types.KeyboardButton("Обновить список пассажиров")
    markup.add(item1, item2, item3)
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
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mark1 = types.KeyboardButton("Добавить пассажира")
            mark2 = types.KeyboardButton("На главную")
            markup.add(mark1, mark2)
            try:
                cursor.execute(f"""SELECT * FROM passenger WHERE userid = {message.chat.id}""")
                c = cursor.fetchone()
                cursor.execute(f"""SELECT * FROM all_passengers WHERE userid = '{message.chat.id}' AND passport = '{str(c[6])}'""")
                d = cursor.fetchone()
                bot.send_message(message.chat.id, f"{c[1]}/{c[2]}/{c[3]}/{c[4]}/{c[5]}/{d[3]}/{c[7]}/{c[8]}")
                bot.send_message(message.chat.id, f"Время отправления: {c[1]}\n"
                                                  f"Город отправления: {c[2]}\n"
                                                  f"Город прибытия: {c[3]}\n"
                                                  f"День прибытия: {c[4]}\n"
                                                  f"Цена билета: {c[5]}\n"
                                                  f"Фамилия: {d[2]}\n"
                                                  f"Имя: {d[1]}\n"
                                                  f"Паспорт: {d[3]}\n"
                                                  f"\n"
                                                  f"Номер карты: {c[7]}\n"
                                                  f"Срок действия карты: {c[8]}", reply_markup=markup)
            except:
                bot.send_message(message.chat.id, 'Пассажира пока нет, добавьте пассажира.', reply_markup=markup)
                pass


        if message.text == "Добавить пассажира":
            train_def(message)

        elif message.text == "Обновить список пассажиров":
            try:
                options = Options()
                options.add_argument("window-size=1280x800")
                options.add_argument("--start-maximized")
                options.add_argument("--disable-blink-features=AutomationControlled")
                #options.add_argument("--headless")
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                driver.get(url='https://chipta.railway.uz/ru/cabinet/passengers')
                driver.implicitly_wait(10)
                driver.find_element(By.XPATH,"//input[@placeholder='Введите e-mail или телефон (998000000000)']").send_keys(site_login)
                driver.find_element(By.XPATH, "//input[@placeholder='Введите пароль']").send_keys(site_password)
                driver.find_element(By.XPATH, "(//button[contains(text(),'ВОЙТИ')])[1]").click()
                sps_old = driver.find_elements(By.XPATH, "//tbody/tr")
                user_id = message.chat.id
                print("подключился пользователь ", user_id)
                connect = sqlite3.connect('users.db')
                cursor = connect.cursor()
                try:
                    cursor.execute(f"""DELETE FROM all_passengers WHERE userid = {user_id}""")
                    connect.commit()
                except:
                    pass
                cursor.execute(f"""CREATE TABLE IF NOT EXISTS all_passengers(
                    userid TEXT,
                    name TEXT,
                    surname TEXT,
                    passport TEXT,
                    passport_userid TEXT UNIQUE
                    )""")
                for i in range(len(sps_old)-1):
                    sps = sps_old[i].text.split(' ')
                    try:
                        cursor.execute(f"""INSERT INTO all_passengers (userid, name, surname, passport, passport_userid) VALUES ("{user_id}", "{sps[1]}", "{sps[0]}", "{sps[-2]}", ("{str(user_id) + str(sps[-2])}"))""")
                    except:
                        pass
                connect.commit()
                connect.close()
                bot.send_message(message.chat.id, "Список пассажиров обновлен")
            except Exception as exc:
                print(f"error {exc}")

        elif message.text == "На главную":
            welcome(message)
        elif message.text == "Покупка билета":
            bot.send_message(message.chat.id, 'Запускается поиск билета.')
            while True:
                try:
                    a = 0
                    connect = sqlite3.connect('users.db')
                    cursor = connect.cursor()
                    cursor.execute(f"""SELECT * FROM passenger WHERE userid = {message.chat.id}""")
                    b = cursor.fetchone()
                    cursor.execute(f"""SELECT * FROM all_passengers WHERE passport = '{b[6]}'""")
                    d = cursor.fetchone()
                    train = b[1]
                    city_1 = b[2]
                    city_2 = b[3]
                    day = b[4]
                    price = b[5]
                    name = d[1] + ' ' + d[2]

                    card_number = b[7]
                    card_date = b[8]

                    options = Options()
                    options.add_argument("--window-size=1100,800")
                    #options.add_argument("--start-maximized")
                    options.add_argument("--disable-blink-features=AutomationControlled")
                    #options.add_argument('--auto-open-devtools-for-tabs')
                    #options.add_argument("--headless")

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
                    time.sleep(1)
                    driver.find_element(By.XPATH, f"//div[contains(@aria-label, '{day}')]").click()
                        # (By.XPATH, "//div[contains(text(),'" + day + "')]").click()
                    time.sleep(1)
                    while True:
                        try:
                            driver.implicitly_wait(5)
                            driver.find_element(By.XPATH, "//h1[contains(text(),'Выберите поезда туда и обратно')]")
                            break
                        except:
                            driver.implicitly_wait(5)
                            driver.find_element(By.XPATH, "//button[contains(text(),'Найти')]").click()

                    bot.send_message(message.chat.id, "Перешли к списку поездов")
                    a = 0
                except Exception as ex:
                    bot.send_message(message.chat.id, "Ошибка, добавьте пассажира заново, и повторите поиск")
                    welcome(message)
                    driver.close()
                    driver.quit()
                    a = 1
                    break
                while True:
                    try:
                        a = 0
                        while True:
                            try:
                                WebDriverWait(driver, 10).until(
                                    EC.invisibility_of_element_located((By.CLASS_NAME, "linear-activity"))
                                )
                                driver.implicitly_wait(0)
                                driver.find_element(By.XPATH, "//p[contains(text(),'Внимание: На данную дату поездов не обнаружено!')]").is_displayed()
                                driver.implicitly_wait(2)
                                driver.find_element(By.XPATH, "//button[contains(text(),'Найти')]").click()
                                # driver.close()
                                # driver.quit()
                                # bot.send_message(message.chat.id, (
                                #         "Продажа билета по условиям:\n" + city_1 + " --->> " + city_2 + "\nДля: " + name + "\nПо цене: " + price + "\nНа поезд " + train + " завершена."))
                                # a = 1
                                # break
                            except:
                                try:
                                    driver.implicitly_wait(1)
                                    driver.find_element(By.XPATH,
                                                        f"""//*[contains(text(),"{train}")]/following::div[@class='info__part info__part--third'][1]//span[contains(text(),"{price}")]
                                                                                 /following::div[@class='info__item'][1]//a[contains(text(),'Выбрать')]""").is_displayed()
                                    break
                                except:
                                    driver.implicitly_wait(1)
                                    driver.find_element(By.CLASS_NAME,
                                                                "selected").click()

                        driver.implicitly_wait(5)
                        driver.execute_script("window.scrollTo(0, 300);")
                        driver.find_element(By.XPATH,
                                             f"""//*[contains(text(),"{train}")]/following::div[@class='info__part info__part--third'][1]//span[contains(text(),"{price}")]
                                             /following::div[@class='info__item'][1]//a[contains(text(),'Выбрать')]""").click()
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
                        while True:
                            try:
                                try:
                                    driver.implicitly_wait(2)
                                    driver.find_element(By.XPATH, "//div[contains(@class, 'toast-error')]")
                                    driver.get(url="https://chipta.railway.uz/ru/pages/cars-page")
                                except:
                                    driver.implicitly_wait(2)
                                    driver.find_elements(By.XPATH, f"//div[@class='train__cars cars']//strong[contains(text(),'{price}')]")[-1].click()
                                    start = driver.find_element(By.XPATH, "(//div[@class='info__time'])[1]")
                                    driver.find_element(By.XPATH,
                                                        "//span[contains(text(),'Выберите до 4 мест на схеме')]").is_displayed()
                                    global start_time
                                    start_time = start.text
                                    driver.implicitly_wait(5)
                                    driver.execute_script("window.scrollTo(0, 3000);")
                                    time.sleep(1)
                                    driver.find_element(By.CLASS_NAME, 'free').click()
                                    driver.execute_script("window.scrollTo(0, 3000);")
                                    time.sleep(1)
                                    driver.find_element(By.XPATH, "(//span[@class='ng-arrow-wrapper'])[1]").click()
                                    driver.find_element(By.XPATH,
                                                        f"""//span[normalize-space()="{name}"]""").click()  #f"//span[contains(text(),'{name}')]"
                                    driver.find_element(By.XPATH, "//button[contains(text(),'Продолжить')]").click()
                                    driver.implicitly_wait(10)
                                    driver.find_element(By.XPATH, "//h2[contains(text(),'ДАННЫЕ ДЛЯ БИЛЕТА ТУДА')]")
                                    break
                            except:
                                try:
                                    driver.implicitly_wait(1)
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
                                driver.implicitly_wait(5)
                                driver.get(url="https://chipta.railway.uz/ru/pages/cars-page")

                        print('Забронировали билет')
                        while True:
                            try:
                                driver.implicitly_wait(5)
                                time.sleep(2)
                                driver.execute_script("window.scrollTo(0, 3000);")
                                time.sleep(1)
                                driver.implicitly_wait(15)
                                driver.find_element(By.XPATH, "//span[@class='checkbox-rect']").click()
                                driver.find_element(By.XPATH, "//img[@alt='Payme logo']").click()
                                break
                            except:
                                driver.implicitly_wait(5)
                                driver.get(url="https://chipta.railway.uz/ru/pages/confirm-page")
                        driver.implicitly_wait(5)
                        driver.find_element(By.XPATH, "//input[@placeholder='____ ____ ____ ____']").send_keys(card_number)
                        driver.find_element(By.XPATH, "//input[@placeholder='__ /__']").send_keys(card_date)
                        driver.find_element(By.XPATH, "//button[contains(text(),'Оплатить')]").click()
                        driver.implicitly_wait(5)
                        time.sleep(3)
                        ticket = driver.find_element(By.XPATH, "//div[@class='part__total']//span[2]")
                        ticket_price = ticket.text

                        def sms_send_def(message):
                            try:
                                print("начали")
                                driver.implicitly_wait(5)
                                sms_code = message.text
                                driver.find_element(By.XPATH, "//input[@placeholder='_ _ _ _ _ _']").clear()
                                driver.find_element(By.XPATH, "//input[@placeholder='_ _ _ _ _ _']").send_keys(sms_code)
                                time.sleep(2)
                                driver.find_element(By.XPATH, "//button[contains(text(),'Оплатить')]").click()
                                time.sleep(6)
                                driver.find_element(By.XPATH, "//a[contains(text(),'Распечатать заказ/билет')]").click()
                                time.sleep(5)
                                list_of_files = glob.glob(file)
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
                        print("ошибка exs", exs)
                        while True:
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
                            try:
                                driver.implicitly_wait(2)
                                driver.find_element(By.CLASS_NAME,
                                                    "selected").click()
                                break
                            except:
                                driver.implicitly_wait(2)
                                driver.get(url="https://chipta.railway.uz/ru/pages/trains-page")
                                driver.find_element(By.XPATH, "//button[contains(text(),'Найти')]").click()

                    except ElementClickInterceptedException as icd:
                        print("ошибка icd", icd)
                        while True:
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
                            try:
                                driver.implicitly_wait(2)
                                driver.find_element(By.CLASS_NAME,
                                                    "selected").click()
                                break
                            except:
                                driver.implicitly_wait(2)
                                driver.get(url="https://chipta.railway.uz/ru/pages/trains-page")
                                driver.find_element(By.XPATH, "//button[contains(text(),'Найти')]").click()

                    except StaleElementReferenceException as sere:
                        print("ошибка sere", sere)
                        while True:
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
                            try:
                                driver.implicitly_wait(2)
                                driver.find_element(By.CLASS_NAME,
                                                    "selected").click()
                                break
                            except:
                                driver.implicitly_wait(2)
                                driver.get(url="https://chipta.railway.uz/ru/pages/trains-page")
                                driver.find_element(By.XPATH, "//button[contains(text(),'Найти')]").click()

                    except ElementNotInteractableException as intr:
                        print("ошибка intr", intr)
                        while True:
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
                            try:
                                driver.implicitly_wait(2)
                                driver.find_element(By.CLASS_NAME,
                                                    "selected").click()
                                break
                            except:
                                driver.implicitly_wait(2)
                                driver.get(url="https://chipta.railway.uz/ru/pages/trains-page")
                                driver.find_element(By.XPATH, "//button[contains(text(),'Найти')]").click()

                    except IndexError as indx:
                        print("ошибка intr", indx)
                        while True:
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
                            try:
                                driver.implicitly_wait(2)
                                driver.find_element(By.CLASS_NAME,
                                                    "selected").click()
                                break
                            except:
                                driver.implicitly_wait(2)
                                driver.get(url="https://chipta.railway.uz/ru/pages/trains-page")
                                driver.find_element(By.XPATH, "//button[contains(text(),'Найти')]").click()

                    except InvalidSelectorException as insl:
                        print("ошибка insl", insl)
                        while True:
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
                            try:
                                driver.implicitly_wait(2)
                                driver.find_element(By.CLASS_NAME,
                                                    "selected").click()
                                break
                            except:
                                driver.implicitly_wait(2)
                                driver.get(url="https://chipta.railway.uz/ru/pages/trains-page")
                                driver.find_element(By.XPATH, "//button[contains(text(),'Найти')]").click()


                    except Exception as ex:
                        print('Ошибка ex', ex)
                        bot.send_message(message.chat.id, "Ошибка, добавьте пассажира заново, и повторите поиск")
                        welcome(message)
                        driver.close()
                        driver.quit()
                        a = 1
                        break
                    # finally:
                    #     print('11232')
                    #     time.sleep(1)
                    #     driver.close()
                    #     driver.quit()
                    #     break
                    finally:
                        if a == 1:
                            return
                        elif a == 0:
                            pass

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


bot.infinity_polling(none_stop=True, timeout=99999, skip_pending=True)
