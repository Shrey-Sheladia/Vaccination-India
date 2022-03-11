import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("user-data-dir=C:\environments\selenium")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome('C:\\Python39\\chromedriver.exe', options=options)
driver.maximize_window()
driver.get('https://web.whatsapp.com')  # Already authenticated

messages = ["COVISHIELD Found at Divine Life School NARODA on 23-05-2021", "Dose 1: 30 Dose 2: 0", "Pin Code: 382330",
            "https://selfregistration.cowin.gov.in/"]

groups = ["Group1", "Group2", "Group3", "Group4"]

v = "COVAXIN"
n = "APOLLO CVF"
d = '24-05-2021'
p = 380059
c1 = 200
c2 = 0
URL = "https://selfregistration.cowin.gov.in/"


def makeMessage(Vaccine_type, name, date, pin_code, capacity1, capacity2, URL):
    global groups

    delay1 = 1.2
    delay2 = 1.2
    delay3 = 1.5

    message = str(capacity1) + " doses of " + Vaccine_type + " Found at " + name + " on " + str(date)
    # doseInfo = "Dose 1: " + str(capacity1) + " Dose 2: " + str(capacity2)
    pinInfo = "Pin Code: " + str(pin_code) + "   " + URL

    messages = [message, pinInfo]#, URL]
    print(message)

    for name in groups:
        driver.find_element_by_xpath("//*[@title='" + name + "']").click()

        for message in messages:
            textBox = driver.find_element_by_xpath(
                '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            textBox.send_keys(message + Keys.CONTROL + Keys.ENTER)
            # textBox.send_keys(Keys.CONTROL + Keys.ENTER)
        driver.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[3]/button/span').click()
        time.sleep(0.15)

start1 = input("Ready? ")
time.sleep(2)
time.tzset()

start = time.time()
makeMessage(v, n, d, p, c1, c2, URL)
taken = time.time() - start
print(round(taken, 3), "Seconds")
time.sleep(1)
driver.close()
