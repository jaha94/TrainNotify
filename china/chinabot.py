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



personslist = []
persons = pandas.read_excel('list.xlsx', sheet_name='queue')
for a in range(0, len(persons)):
    personslist.append(a)




def finding(i):
    def xpath(x):
        return driver.find_element(By.XPATH, x)
    name1 = persons['Name'][i]
    number1 = str(persons['Number'][i])
    mail1 = persons['Mail'][i]
    id1 = str(persons['ID'][i])
    options = Options()
    options.add_argument("window-size=1280x800")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    #options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url='https://avas.mfa.gov.cn/')
    driver.implicitly_wait(10)
    xpath("//span[@data-text='en_US']").click()
    xpath("//li[@id='AS']").click()
    xpath("//li[@value='UZBA']").click()
    xpath("//body/div[1]/div[1]").click()
    driver.execute_script("window.scrollTo(0, 3000);")
    xpath("//button[@onclick='yypersoninfo();']").click()
    driver.execute_script("window.scrollTo(0, 3000);")
    time.sleep(1)
    xpath("//input[@id='linkname']").send_keys(name1)
    time.sleep(1)
    xpath("//input[@id='linkphone']").send_keys(number1)
    time.sleep(1)
    xpath("//input[@id='mail']").send_keys(mail1)
    time.sleep(1)
    xpath("//input[@id='applyid1']").send_keys(id1)
    time.sleep(1)
    xpath("//button[@onclick='savePersionInfo();']").click()
    while True:
        try:
            time.sleep(5)
            xpath("//ul[@class='calendar-ul-box']")
            break
        except:
            pass

    driver.implicitly_wait(1)
    while True:
        try:
            id = xpath("//span[contains(@class, 'calendar-timezone-enable')]//..").get_attribute("id")
            driver.find_element(By.CSS_SELECTOR, f"li[data-date='{id}']").click()
            xpath("//span[contains(@class, 'calendar-timezone-enable')]").click()
            xpath("//button[@class='aui_state_highlight']").click()
            xpath("//button[@class='aui_state_highlight']").click()
            xpath("//td[@id='YyNo']")
            driver.execute_script("window.scrollTo(0, 3000);")
            time.sleep(2)
            xpath("//button[@onclick='downloadYyPdf();']").click()
            time.sleep(30)
            #driver.get_screenshot_as_file(f'result-{id1}.png')
            break
        except:
            driver.refresh()


if __name__ == '__main__':
    p = Pool(processes=len(personslist))
    p.map(finding, personslist)
