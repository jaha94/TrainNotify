import random
import plyer
import telebot
import sqlite3
import glob
import os
import re
import urllib
import requests as r
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException
import time
from telebot import types
token = '674694961:AAEbwjoVZAavuGY7bcJXFi0jCfg07bqrrEI'
bot = telebot.TeleBot(token)
old_name = ''

chat_id = '-1001803279197'
options = Options()
options.add_argument("window-size=1280x800")
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)
driver.get(url=f'https://www.olx.uz/d/elektronika/kompyutery/?currency=UZS&search%5Border%5D=created_at:desc')
driver.find_element(By.XPATH, "//span[contains(text(),'Закрыть')]").click()
while True:
    try:
        num = ''
        driver.get(url=f'https://www.olx.uz/d/elektronika/kompyutery/?currency=UZS&search%5Border%5D=created_at:desc')
        driver.implicitly_wait(10)
        name = driver.find_elements(By.CLASS_NAME, "css-v3vynn-Text")[3].text
        if old_name != name:
            url = driver.find_elements(By.CLASS_NAME, "css-1bbgabe")[3].get_attribute('href')
            driver.get(url=url)
            try:
                driver.implicitly_wait(10)
                driver.find_element(By.XPATH, "//span[contains(text(),'Показать телефон')]").click()
                num = driver.find_elements(By.CLASS_NAME, "css-v1ndtc")[0].text.replace(' ', '')
            except:
                pass
            price = driver.find_elements(By.CLASS_NAME, "css-okktvh-Text")[0].text
            teg = driver.find_elements(By.CLASS_NAME, 'css-tyi2d1')[3].text.replace(' ', '').lower()
            opis = driver.find_element(By.CLASS_NAME, "css-g5mtbi-Text").text.replace('\n\n', '\n')
            old_name = name
            print(old_name)
            # mark1 = types.InlineKeyboardButton(text='Saxifa', url=url)
            # mark2 = types.InlineKeyboardButton(text='Telefon', url=f'tel:{num}')
            # markup = types.InlineKeyboardMarkup()
            # markup.add(mark1, mark2)
            lot_name = re.sub("[^A-Za-z0-9]", "", old_name)
            img = driver.find_elements(By.CLASS_NAME, "css-1bmvjcs")[0].get_attribute('src')
            print(img)
            img = r.get(img)
            img_file = open(f'img/{lot_name}.png', 'wb')
            img_file.write(img.content)
            img_1 = open(f'img/{lot_name}.png', 'rb')
            # out = open(f"img/{lot_name}.webp", 'rb')
            # out.write(p.content)
            # out.close()
            # img_1 = open(f"img/{lot_name}.webp", 'rb')
            bot.send_photo('@TashkentComp_Channel', img_1, caption=f"""*{old_name}*\n\nЦена: {price}\n\n[Ссылка]({url})\n+998{num[-9:]}\n#{teg}""", parse_mode='Markdown')
        time.sleep(60)
    except Exception as ex:
        print(ex)
        time.sleep(60)


    # time.sleep(2)
    # driver.find_element(By.XPATH, "//i[normalize-space()='check']").click()
    # lot_n = driver.find_element(By.CLASS_NAME, "ea-lot-number").text.split(' ')[1]
    # for lot_num in range(int(lot_n), int(lot_n) - 5, -1):
    #     driver.implicitly_wait(5)
    #     driver.get(url=f'https://e-auksion.uz/lot-view?lot_id={lot_num}')
    #     time.sleep(1)
    #     lot_name = re.sub("[^A-Za-z0-9]", "", driver.find_element(By.CLASS_NAME, "lot-card-name-title").text)
    #     lot_name_full = driver.find_element(By.CLASS_NAME, "lot-card-name-title").text
    #     url = driver.current_url
    #     img = driver.find_element(By.CLASS_NAME, "magnifier-box")
    #     img.screenshot(f"img/{lot_name}.png")
    #     img_1 = open(f"img/{lot_name}.png", 'rb')
    #     lot_start = driver.find_element(By.XPATH, "//p[contains(text(),'Ariza qabul qilish oxirgi muddati')]/following::div[@class='lot-card-attribute-value']").text
    #     lot_price = driver.find_element(By.XPATH, "//p[contains(text(),'Boshlang‘ich narxi:')]/following::div[@class='lot-card-attribute-value']").text
    #     lot_price2 = driver.find_element(By.XPATH, "//p[contains(text(),'Zakalat')]/following::div[@class='lot-card-attribute-value']").text
    #     location = driver.find_element(By.XPATH, "//div[@class='lot-map-div q-pt-md']//a[@target='_blank']").get_attribute('href')
    #     mark1 = types.InlineKeyboardButton(text='Saxifa', url=url)
    #     mark2 = types.InlineKeyboardButton(text='Lokatsiya', url=location)
    #     markup = types.InlineKeyboardMarkup()
    #     markup.add(mark1, mark2)
    #     bot.send_photo(-1001803279197, img_1, caption=f"""{lot_name_full}\n\nBoshlang'ich narx: {lot_price}\nZakalat puli miqdori: {lot_price2}\nAriza qabul qilish oxirgi muddati: {lot_start}""", reply_markup=markup)
    # lot = driver.find_elements(By.CLASS_NAME, "lot-name")
    # img = driver.find_elements(By.XPATH, "//div[@class='q-img__content absolute-full']")
    # for lot_num in range(len(lot)):
    #     # with open(f"img/{lot[lot_num].text}.png", 'wb') as file:
    #     #     #identify image to be captured
    #     #     #write file
    #     #     file.write(img[lot_num].screenshot_as_png)
    #     img[lot_num].screenshot(f"img/{lot[lot_num].text}.png")
    #     img_1 = open(f"img/{lot[lot_num].text}.png", 'rb')
    #     bot.send_photo(message.chat.id, img_1, caption=lot[lot_num].text)
    # bot.send_message(message.chat.id, lot[0])




bot.polling(none_stop=True)
