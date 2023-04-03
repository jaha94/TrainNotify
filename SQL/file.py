import telebot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from telebot import types

token = '5527235154:AAEs7ywYpDJd4QVek4MyP7cVwyyLwuUnhTE'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Поиск")
    markup.add(item1)
    bot.send_message(message.chat.id,
                     "<b>{0.first_name}</b>\nЭто бот OLX <b>{1.first_name}</b>".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == "Поиск":
            while True:
                try:
                    text_to_find = ''

                    def find_text_def(message):
                        global text_to_find
                        text_to_find = message.text

                    options = Options()
                    options.add_argument("window-size=1280x800")
                    options.add_argument("--start-maximized")
                    options.add_argument("--disable-blink-features=AutomationControlled")
                    # options.add_argument("--headless")
                    buying = False
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                    action = ActionChains(driver)
                    driver.implicitly_wait(10)
                    driver.get(url='https://www.olx.uz/')
                    find_text = bot.send_message(message.chat.id, "Введите текст для поиска")
                    bot.register_next_step_handler(find_text, find_text_def)

                    driver.find_element(By.XPATH, "//input[@id='headerSearch']").send_keys(text_to_find)
                    driver.find_element(By.XPATH, "//input[@id='submit-searchmain']").click()
                    time.sleep(50)
                except Exception as ex:
                    print("Ошибка: ", ex)
                finally:
                    driver.close()
                    driver.quit()
                    break


bot.polling(none_stop=True)
