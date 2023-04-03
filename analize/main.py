import pandas
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
from multiprocessing import Pool

df = pandas.read_excel('fff.xlsx', sheet_name='Sheet1')
spis = []
dok1 = 2511012080
while dok1 != '*':
    pers1 = df[(df['schot'] == int(dok1)) & (df['summa'] < 0)]
    # pers2 = pers1.iloc[0]['summa']
    dok1 = pers1.iloc[0]['korresp']
    spis.append(dok1)
print(spis[-2])
print(df[df['schot'] == int(spis[-2])].iloc[0]['tekst'])
# print(p)
# pers2 = df[(df['schot'] == int(p))]
# print(pers2)