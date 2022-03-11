import requests
from datetime import timezone, datetime
import time
from playsound import playsound
# import winsound

# import RPi.GPIO as GPIO
# import os

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options

# options = Options()
# options.add_argument("user-data-dir=C:\environments\selenium")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

# driver = webdriver.Chrome('C:\\Python39\\chromedriver.exe', options=options)
# driver.get('https://web.whatsapp.com')
# time.sleep(5)
# ans = input("Ready? ")

groupsAHM = ["Vaccine Scheduling Help",
             "Vaccine Scheduling Help 2", "Vaccine Scheduling Help 3", "Vaccine Scheduling Help 4"]

# groupsAHM = ["Group1",
#              "Group2", "Group3", "Group4"]

groupsGHN = ["Gandhinagar Vaccination 1"]

groupDistricts = {770: groupsAHM, 772: groupsGHN, 153:groupsGHN}

VSCode = False

if not VSCode:
    from pynput.keyboard import Key, Controller

    keyboard = Controller()

    from pynput.mouse import Button, Controller

    mouse = Controller()

    CONNECT = False
    TYPE = True
else:
    CONNECT = False
    TYPE = False

time.sleep(2)

Already_On = False
DIML = False

RegistrationURL = "https://selfregistration.cowin.gov.in/"

foundSpots = {}
to_remove = {}

OldData = {}
NewData = {}

'''
def Light_On():

    print("On")
    GPIO.output(ON, False)
    time.sleep(delay)
    GPIO.output(ON, True)


def Light_Off():
    print("Off")
    GPIO.output(OFF, False)
    time.sleep(delay)
    GPIO.output(OFF, True)


def pressSec(pinNum):
    print("Turning", pinNum, "On")
    GPIO.output(pinNum, False)
    time.sleep(1)
    GPIO.output(pinNum, True)
    print("Turning", pinNum, "Off")


def singePress(pinNum):
    print("Turning", pinNum, "On")
    GPIO.output(pinNum, False)
    time.sleep(delay)
    GPIO.output(pinNum, True)
    print("Turning", pinNum, "Off")


def channelTest(pinNum):
    print("Turning", pinNum, "On")
    GPIO.output(pinNum, False)
    time.sleep(delay)
    GPIO.output(pinNum, True)
    print("Turning", pinNum, "Off")


def PressDown(pinNum):
    print("Turning", pinNum, "On")
    GPIO.output(pinNum, False)


def PressUp(pinNum):
    if pinNum != None:
        print("Turning", pinNum, "Off")
        GPIO.output(pinNum, True)


singePress(ALL)
'''


def makeMessage(Vaccine_type, name, date, pin_code, capacity1, capacity2, URL, ID):
    for i in range(5):

        playsound('point.wav')
        time.sleep(1)
        playsound('hit.wav')

    global groupDistricts

    delay1 = 1.2
    delay2 = 1.2
    delay3 = 1.5

    message = str(capacity1) + " doses of " + Vaccine_type + " Found at " + name + " on " + str(date)
    pinInfo = "Pin Code: " + str(pin_code) + "   " + URL

    messages = [message, pinInfo]  # , URL]

    # message = Vaccine_type + " Found at " + name + " on " + str(date)
    # doseInfo = "Dose 1: " + str(capacity1) + " Dose 2: " + str(capacity2)
    # pinInfo = "Pin Code: " + str(pin_code)

    # messages = [message, doseInfo, pinInfo, URL]
    print(message)

    groups = groupDistricts[ID]

    for name in groups:
        driver.find_element_by_xpath("//*[@title='" + name + "']").click()

        for message in messages:
            textBox = driver.find_element_by_xpath(
                '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            textBox.send_keys(message + Keys.CONTROL + Keys.ENTER)
        driver.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[3]/button/span').click()
        time.sleep(0.15)


'''
def ErrorLights(dely=0.9):
    for i in range(5):
        Light_Off()
        time.sleep(delay)
        if DIML:
            singePress(DIM)
        else:
            Light_On()
        time.sleep(delay)
'''


def ringRepeat(num=5):
    try:
        global Already_On

        for i in range(num):
            winsound.PlaySound("point.wav", winsound.SND_ASYNC)
            time.sleep(0.6)
            winsound.PlaySound("hit.wav", winsound.SND_ASYNC)

        time.sleep(200)
        Already_On = False
    except Exception as e:
        print(str(e))
        print("RING REPEAT ERROR")


'''
def on_and_off(delay=1.5):
    singePress(BRIGHT)
    try:
        if CONNECT:
            global Already_On

            singePress(BRIGHT)

            for i in range(2):
                Light_Off()
                time.sleep(delay)
                if DIML:
                    singePress(DIM)
                else:
                    Light_On()
                time.sleep(delay)

            time.sleep(0.5)
            Already_On = False

    except Exception as e:
        print(str(e))
'''


def GetSlots(Days1, ID):
    global Already_On, foundSpots, OldData, NewData
    Found = False

    URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=' + str(
        ID) + '&date=' + Days1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

    r = requests.get(URL, headers=headers)

    if str(r) != "<Response [200]>":
        print("ERROORRRRR")
        print(str(r))
        time.sleep(5)
        return Found, Found

    data = r.json()
    if "calendar" in URL:
        centers = data["centers"]
    elif "find" in URL:
        centers = data["sessions"]
    else:
        print("Could not find proper data")
        print(data)
        return
    counts = 0
    NewData = data

    if NewData == OldData:
        return 'Samee', 'Found'

    else:
        OldData = NewData

    for center in centers:

        name = center["name"]
        pin_code = center["pincode"]
        date = center["date"]
        min_age_limit = center["min_age_limit"]
        capacity1 = center["available_capacity_dose1"]
        capacity2 = center["available_capacity_dose2"]
        capacity = capacity2 + capacity1
        Vaccine_type = center["vaccine"]

        if capacity1 > 4:
            # print(
            #     "Name: " + name + "     Capacity: " + str(capacity) + "     Date: " + str(
            #         date) + "     Age Limit: " + str(min_age_limit) + "     Pincode: " + str(pin_code))
            print("Time: " + str(time.strftime("%I: %M: %S")))
            Found = True

            if min_age_limit < 45 and Vaccine_type != "COVISHIELD":

                if name not in foundSpots:
                    try:
                        makeMessage(Vaccine_type, name, date, pin_code,
                                    capacity1, capacity2, RegistrationURL, ID)
                    except Exception as e:
                        print(str(e))
                        print("Error occured while trying to send message")
                        # ringRepeat(5)

                    foundSpots[name] = time.time()
                    print("Added " + name)

                    if not Already_On:
                        Already_On = True

            print()
            print()
        counts += 1
    return Found, counts


# os.environ['TZ'] = 'Asia/Kolkata'
# time.tzset()


AHM = 770
GHN = 772
GHN2 = 153

loops = 0

delay = 9

print("Starting")
while True:
    loops += 1



    GotSomething = False

    try:

        today = datetime.now()
        today.replace(tzinfo=timezone.utc)

        # print(today.strftime("%H: %M: %S"))
        HR = int(today.strftime("%H"))
        if HR > 14:
            change = 1
        else:
            change = 0

        Days2 = (str(int(today.strftime("%d")) + change) +
                 (today.strftime("-%m-%y")))

        found, count = GetSlots(Days2, AHM)
        time.sleep(delay)
        found1, count1 = GetSlots(Days2, GHN)
        time.sleep(delay)
        found2, count2 = GetSlots(Days2, GHN2)
        try:
            count = count1 + count2 + count
        except Exception as e:
            print("Count Error")

        if loops == 10:
            print(Days2)
            loops = 0
        GotSomething = True

    except Exception as e:

        print("ERROR OCCURRED")
        print(str(e))
        # ringRepeat(5)
        time.sleep(10)

    if GotSomething:
        # print(found, count)
        if len(foundSpots) > 0:
            for name in list(foundSpots):
                if time.time() - foundSpots[name] > 600:
                    print("Removed " + str(name))
                    del foundSpots[name]
        if not count:
            pass
            # print("NO COUNT")
            # time.sleep(3.4)
            # continue

        if str(type(found)) == "str":
            print("STRING")
            if "Samee" in found:
                print("Same Data received", str(time.strftime("%I: %M: %S")))

        if not found:

            print("No Open Slots in " + str(count) +
                  " Spaces. Time: " + str(time.strftime("%I: %M: %S")))

        if found == "False":
            print("No Open Slots in " + str(count) +
                  " Spaces. Time: " + str(time.strftime("%I: %M: %S")))
        time.sleep(delay)
