from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import telebot
import schedule
import time
from threading import Thread

token = '6208415025:AAG-9HSM5_rSZEBoy8o7RS8LeFgJSMwoWE8'
bot = telebot.TeleBot(token)


def start_schedule():
    try:
        # schedule.every().day.at("15:12").do(data_r_new)
        schedule.every(2).minutes.do(data_r_new)
    except:
        pass
    #
    while True:
        schedule.run_pending()
        time.sleep(1)


def data_r_new():
    try:
        def xpath(x):
            return driver.find_element(By.XPATH, x)

        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        now = datetime.now().strftime("-%d%m%Y")
        banknum = ['20214000004478157015', '20214000104478157011']
        print(yesterday)
        print(now)

        options = Options()
        options.add_experimental_option("prefs", {
                "download.default_directory": "C:\SAP",
                "download.prompt_for_download": False
        })

        @bot.message_handler()
        def captcha1():
            def captcha2(message):
                text_cap = message.text
                driver.find_element(By.ID, "loginform-verifycode").send_keys(text_cap)
                xpath("//button[contains(text(),'Войти')]").click()
            # msg = bot.send_message(-1001642262784, "Введите код")
            driver.find_element(By.XPATH, "//img[@id='loginform-verifycode-image']").screenshot('11.png')
            img_1 = open(f'11.png', 'rb')
            msg = bot.send_photo(-1001642262784, img_1,
                           caption=f"Введите код на картинке",
                           parse_mode='Markdown')
            bot.register_next_step_handler(msg, captcha2)

        options.add_argument("window-size=1280x800")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        #options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url='https://old-ibank.nbu.uz/')
        driver.implicitly_wait(10)
        xpath("//input[@placeholder='логин']").clear()
        xpath("//input[@placeholder='логин']").send_keys("akfa2")
        xpath("//input[@placeholder='пароль']").clear()
        xpath("//input[@placeholder='пароль']").send_keys("a123456789")
        captcha1()

        while True:
            try:
                driver.find_element(By.PARTIAL_LINK_TEXT, "Экспорт").click()
                break
            except:
                time.sleep(2)

        for i in range(len(banknum)):
            driver.find_element(By.PARTIAL_LINK_TEXT, "Экспорт").click()
            driver.find_element(By.ID, "export-date_from").clear()
            driver.find_element(By.ID, "export-date_from").send_keys(yesterday)
            driver.find_element(By.ID, "export-date_to").clear()
            driver.find_element(By.ID, "export-date_to").send_keys(yesterday)
            xpath("//span[@class='input-group-addon kv-field-separator']").click()

            # driver.find_element(By.ID, "export-file_format").click()
            xpath("//option[@value='txt3']").click()
            # xpath("//label[@for='export-account_list']").click()
            xpath("//input[@placeholder='Выберите счет(а)']").click()
            xpath(f"//li[contains(normalize-space(),'{banknum[i]}')]").click()
            xpath("//input[@id='export-file_name']").clear()
            xpath("//input[@id='export-file_name']").send_keys(banknum[i])
            xpath("//option[@value='utf-8']").click()
            xpath("//button[contains(text(),'Загрузить')]").click()
            time.sleep(3)



            print("OOOKKK")

            # baz_n = input('Базисный срок начала: ')
            # baz_k = input('Базисный срок конца: ')
            # subprocess.call(["taskkill","/f","/im","saplogon.exe"])
            # subprocess.call(["taskkill","/f","/im","EXCEL.EXE"])
        import subprocess
        import win32com.client
        subprocess.check_call(
            ['C:\Program Files (x86)\SAP\FrontEnd\SAPgui\sapshcut.exe', '-system=S4P', '-client=100', '-maxgui', '-language=ru'])  #, '-user=JKURBANALIEV', '-pw=Ghbrjkmysq86'
        time.sleep(10)
        SapGuiAuto = win32com.client.GetObject('SAPGUI')
        application = SapGuiAuto.GetScriptingEngine
        connection = application.Children(0)
        session = connection.Children(0)

        for i in range(len(banknum)):
            time.sleep(5)
            print(now)
            session.findById("wnd[0]").maximize()
            session.findById("wnd[0]/tbar[0]/okcd").text = "/nff_5"
            session.findById("wnd[0]").sendVKey(0)
            session.findById("wnd[0]/tbar[1]/btn[17]").press()
            session.findById("wnd[1]/usr/cntlALV_CONTAINER_1/shellcont/shell").currentCellRow = 8
            session.findById("wnd[1]/usr/cntlALV_CONTAINER_1/shellcont/shell").selectedRows = "8"
            session.findById("wnd[1]/usr/cntlALV_CONTAINER_1/shellcont/shell").doubleClickCurrentCell()
            session.findById("wnd[0]/usr/ctxtAUSZFILE").text = f"C:\SAP\{banknum[i]}{now}111.txt"
            session.findById("wnd[0]/tbar[1]/btn[8]").press()
            if session.findById("wnd[0]/sbar").text != "":
                session.findById("wnd[0]/tbar[0]/okcd").text = "/n"
                session.findById("wnd[0]").sendVKey(0)
                bot.send_message(-1001642262784, f"Счёт {banknum[i]}  загружен 🆗")
            else:
                bot.send_message(-1001642262784, f"Счёт {banknum[i]}  загружен 🆗")
                print("OK")
        bot.send_message(-1001642262784, f"Работа успешно завершена ✅")
    except Exception as ex:
        print(ex)
        bot.send_message(-1001642262784, "Возникла ошибка ❌")
        pass
    finally:
        try:
            driver.close()
            driver.quit()
            session.findById("wnd[0]/tbar[0]/okcd").text = "/nex"
            session.findById("wnd[0]").sendVKey(0)
        except:
            pass


def main_loop():
    thread = Thread(target=start_schedule)
    thread.start()

    while True:
        try:
            bot.polling(True)
        except:
            pass

if __name__ == '__main__':
    main_loop()