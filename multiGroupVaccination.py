import requests
from datetime import timezone, datetime
import winsound
import time
import threading
import pyperclip
import socket
import json
# import RPi.GPIO as GPIO
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

options = Options()
options.add_argument("user-data-dir=C:\environments\selenium")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome('C:\\Python39\\chromedriver.exe', options=options)
driver.get('https://web.whatsapp.com')
driver.maximize_window()
# time.sleep(5)

ans = input("Ready? ")

List_18 = []
List_18_2 = []
List_45 = []
maxListLength = 6

groupsTest = ["Notification Number"]
groupsAHM = ["Ahmedabad Vaccination", "1st Dose | AMD - Group 1", "1st Dose | AMD - Group 2",
             "1st Dose | AMD - Group 3"]

groupsAHM2 = ["2nd Dose | AMD - Group 1", "2nd Dose | AMD - Group 2", "2nd Dose | AMD - Group 3"]

# groupsAHM = ["1st Dose"]
# groupsAHM2 = ["2nd dose"]

groups45 = ["Shrey"]  # "Ahmedabad 45"]
groupsGHN = ["Gandhinagar Vaccination 1", "Gandhinagar Vaccination 2"]
# groupsSUR = ["Surat Vaccination 1"]
groupsSUR = ['Surat Vaccination 1']

groupDistricts = {0: groupsTest, 770: groupsAHM, 772: groupsGHN, 153: groupsGHN, 776: groupsSUR, 45: groups45,
                  7702: groupsAHM2}

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

longDelay = {}
foundSpots = {}
foundSpots2 = {}
to_remove = {}

OldData = {}
NewData = {}

BRIGHT = DIM = 17
def Light_On():

    print("On")
    # GPIO.output(ON, False)
    time.sleep(delay)
    # GPIO.output(ON, True)


def Light_Off():
    print("Off")
    # GPIO.output(OFF, False)
    time.sleep(delay)
    # GPIO.output(OFF, True)


def pressSec(pinNum):
    print("Turning", pinNum, "On")
    # GPIO.output(pinNum, False)
    time.sleep(1)
    # GPIO.output(pinNum, True)
    print("Turning", pinNum, "Off")


def singePress(pinNum):
    print("Turning", pinNum, "On")
    # GPIO.output(pinNum, False)
    time.sleep(delay)
    # GPIO.output(pinNum, True)
    print("Turning", pinNum, "Off")


def channelTest(pinNum):
    print("Turning", pinNum, "On")
    # GPIO.output(pinNum, False)
    time.sleep(delay)
    # GPIO.output(pinNum, True)
    print("Turning", pinNum, "Off")


def PressDown(pinNum):
    print("Turning", pinNum, "On")
    # GPIO.output(pinNum, False)


def PressUp(pinNum):
    if pinNum != None:
        print("Turning", pinNum, "Off")
        # GPIO.output(pinNum, True)


# singePress(ALL)



def WhatsApp_Send(ID, messageW):
    global groupDistricts, driver
    # ID = 0
    groups = groupDistricts[ID]

    for name in groups:
        print(name)
        pyperclip.copy(messageW)

        try:
            chat = driver.find_element_by_xpath("//*[@title='" + name + "']")
            actions = ActionChains(driver)
            actions.move_to_element(chat).click()
            chat.click()
            time.sleep(0.5)

            textBox = driver.find_element_by_xpath(
                '/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]/div')
            time.sleep(0.25)
            # textBox.send_keys(messageW)
            pyperclip.copy(messageW)

            Pasted = False

            while not Pasted:
                textBox.send_keys(Keys.CONTROL, "v")
                time.sleep(0.3)

                try:
                    sendMessage = driver.find_element_by_xpath(
                    ('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[2]/button'))
                    Pasted = True
                
                except Exception as e:
                    print("Trying to paste again...")
                    time.sleep(0.15)

            while True:
                try:
                    sendMessage.click()
                
                except Exception as e:
                    break
            
            print("Sent")

            

            '''
            # # sendMessage = driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[3]/button')
            # # sendMessage.click()
            # time.sleep(0.2)


            # try:
            #     sendMessage = driver.find_element_by_xpath(
            #         ('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[2]/button'))
            #     sendMessage.click()
            # except Exception as e:
            #     time.sleep(0.5)
            #     print("Trying Again ((((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))))))))")
            #     textBox.send_keys(Keys.CONTROL, "v")
            #     time.sleep(0.3)

            #     try:
            #         sendMessage = driver.find_element_by_xpath(
            #             ('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[2]/button'))
            #         sendMessage.click()

            #     except Exception as e:
            #         print(str(e), "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            #         textBox.send_keys(Keys.ENTER)
            # # time.sleep(0.15)
            '''
            time.sleep(0.4)
        except Exception as e:
            print("Error while sending info to", name)
            print(messageW)

            print()
            print(str(e))
            t1 = threading.Thread(target=ringRepeat, args=[5])
            t1.start()
            # ringRepeat(5)
            return



def sendMessages(List_Num, age):
    message = ""
    ID_Group = int(age)
    count = 1
    for (Vaccine_type, name, date, pin_code, capacity1, capacity2, URL, ID, age, cost) in List_Num:
        messageSingle = makeSingleMessage(Vaccine_type, name, date, pin_code, capacity1, capacity2, URL, ID, age, cost,
                                          count)
        message += messageSingle
        message += "\n \n"
        count += 1

        if not (ID_Group == 770 or 7702):
            print("Error in ID", ID_Group)

            ID = 770

    pyperclip.copy(message)
    WhatsApp_Send(ID_Group, message)


def makeSingleMessage(Vaccine_type, name, date, pin_code, capacity1, capacity2, URL, ID, age, cost, count):
    global groupDistricts

    if capacity2 > 4:
        message1 = "Open slots of *" + Vaccine_type + "* found at " + name + " on " + str(
            date)
    else:
        message1 = "Open slots of *" + Vaccine_type + "* found at " + name + " on " + str(
            date)

    message1 = str(count) + ") " + message1

    pinInfo = "Pin Code: *" + str(pin_code) + "*   |  Cost: " + str(cost)

    if capacity2 > 4:

        doseInfo = "Dose 1: " + str(capacity1) + "  |  _*Dose 2: " + str(capacity2) + "*_"
    else:
        doseInfo = "Dose 1: " + str(capacity1) + "  |  Dose 2: " + str(capacity2)

    # count = str(count) + ")"
    messagesList = [message1, doseInfo, pinInfo, URL]
    singleMessage = ''

    for m in messagesList:
        singleMessage += str(m)
        singleMessage += "\n"

    return singleMessage


def makeMessage(Vaccine_type, name, date, pin_code, capacity1, capacity2, URL, ID, age, cost):
    global groupDistricts

    delay1 = 1.2
    delay2 = 1.2
    delay3 = 1.5

    if age == 18:
        message = str(capacity1) + " doses of " + Vaccine_type + " _For 18+_ " + "found at " + name + " on " + str(date)
    else:
        message = str(capacity1) + " doses of " + Vaccine_type + " _For 45+_ " + "found at " + name + " on " + str(date)

    pinInfo = "Pin Code: *" + str(pin_code) + "*   |  Cost: " + str(cost)

    messages = [message, pinInfo, URL]

    # message = Vaccine_type + " Found at " + name + " on " + str(date)
    # doseInfo = "Dose 1: " + str(capacity1) + " Dose 2: " + str(capacity2)
    # pinInfo = "Pin Code: " + str(pin_code)

    # messages = [message, doseInfo, pinInfo, URL]
    print(message, ID, pin_code)

    try:
        time.strftime("%I: %M: %S")

    except Exception as e:
        print("Error printing Time")
        print(str(e))

    groups = groupDistricts[ID]

    for name in groups:
        try:
            chat = driver.find_element_by_xpath("//*[@title='" + name + "']")
            actions = ActionChains(driver)
            actions.move_to_element(chat).click()
            chat.click()
            time.sleep(0.1)

            textBox = driver.find_element_by_xpath(
                '/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]/div')
            for message in messages:
                textBox.send_keys(message + Keys.CONTROL + Keys.ENTER)

            # sendMessage = driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[3]/button')
            # sendMessage.click()
            textBox.send_keys(Keys.ENTER)
            # time.sleep(0.15)
        except Exception as e:
            print("Error while sending info to", name)
            for p in messages:
                print(p)

            print()
            print(str(e))
            t1 = threading.Thread(target=ringRepeat, args=[5])
            t1.start()
            # ringRepeat(5)
        time.sleep(0.15)



def ErrorLights(dely=0.9):
    for i in range(5):
        Light_Off()
        time.sleep(delay)
        if DIML:
            singePress(DIM)
        else:
            Light_On()
        time.sleep(delay)



def ringRepeat(num=5):
    try:
        global Already_On

        for i in range(num):
            winsound.PlaySound("point.wav", winsound.SND_ASYNC)
            time.sleep(0.6)
            winsound.PlaySound("hit.wav", winsound.SND_ASYNC)

        # time.sleep(200)
        Already_On = False
    except Exception as e:
        print(str(e))
        print("RING REPEAT ERROR")



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



def GetSlots(Days1, ID):
    global Already_On, foundSpots, foundSpots2, OldData, NewData, List_45, List_18, List_18_2, longDelay
    Found = False
    counts = 0
    URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=' + str(
        ID) + '&date=' + Days1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

    try:
        r = requests.get(URL, headers=headers)
    except ConnectionError:
        print("Connection Error")
        time.sleep(5)
        return Found, counts

    if str(r) == "<Response [429]>":
        t1 = threading.Thread(target=ringRepeat, args=[3])
        t1.start()
        print("ERROORRRRR", ID)
        print(str(r))
        try:

            print(r.headers)
            print(type(r.headers))
        except:
            pass
        time.sleep(5)
        return Found, counts

    if str(r) != "<Response [200]>":
        print("ERROORRRRR", ID)
        print(str(r))
        time.sleep(5)
        return Found, counts

    data = r.json()
    if "calendar" in URL:
        centers = data["centers"]
    elif "find" in URL:
        centers = data["sessions"]
    else:
        print("Could not find proper data")
        print(data)
        return

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
        cost = center["fee"]
        if str(cost) == "0":
            cost = "Free"

        if capacity1 > 4 and cost == "Free":
            # print(
            #     "Name: " + name + "     capacity1: " + str(capacity1) + "     Date: " + str(
            #         date) + "     Age Limit: " + str(min_age_limit) + "     Pincode: " + str(pin_code))
            # print("Time: " + str(time.strftime("%I: %M: %S")))

            if min_age_limit < 45:

                if (name + Vaccine_type + str(date)) not in foundSpots:  # and (name not in longDelay):
                    Found = True

                    List_18.append((Vaccine_type, name, date, pin_code,
                                    capacity1, capacity2, RegistrationURL, ID, 18, cost))

                    foundSpots[(name + Vaccine_type + str(date))] = capacity1
                    print()
                    print("Added " + (name + Vaccine_type + str(date)) + " " + str(capacity1))
                    print()

                    if len(List_18) == maxListLength:
                        print("Sending 18+ Vacancies1:", len(List_18))
                        sendMessages(List_18, ID)
                        List_18 = []
                    # makeMessage(Vaccine_type, name, date, pin_code,
                    #             capacity1, capacity2, RegistrationURL, ID, 18, cost)

                    if not Already_On:
                        Already_On = True

                elif foundSpots[(name + Vaccine_type + str(date))] + 10 < capacity1:

                    Found = True

                    List_18.append((Vaccine_type, name, date, pin_code,
                                    capacity1, capacity2, RegistrationURL, ID, 18, cost))

                    foundSpots[(name + Vaccine_type + str(date))] = capacity1
                    print()
                    print("Added " + name + Vaccine_type + str(date) + " " + str(capacity1))
                    print()

                    if len(List_18) == maxListLength:
                        print("Sending 18+ Vacancies2:", len(List_18))
                        sendMessages(List_18, ID)
                        List_18 = []
                    # makeMessage(Vaccine_type, name, date, pin_code,
                    #             capacity1, capacity2, RegistrationURL, ID, 18, cost)

                    if not Already_On:
                        Already_On = True

                elif foundSpots[name + Vaccine_type + str(date)] > capacity1:
                    print("Decreased capacity of", name + " " + Vaccine_type + "1", "from",
                          foundSpots[name + Vaccine_type + str(date)], "to", capacity1)
                    foundSpots[name + Vaccine_type + str(date)] = capacity1

        if capacity2 > 4:

            # print(
            #     "Name: " + name + "     Capacity: " + str(capacity) + "     Date: " + str(
            #         date) + "     Age Limit: " + str(min_age_limit) + "     Pincode: " + str(pin_code))
            # print("Time: " + str(time.strftime("%I: %M: %S")))

            if min_age_limit < 45:

                if name + Vaccine_type + str(date) not in foundSpots2:  # and (name not in longDelay):
                    Found = True

                    ID_2 = int(str(ID) + "2")
                    List_18_2.append((Vaccine_type, name, date, pin_code,
                                      capacity1, capacity2, RegistrationURL, ID, 18, cost))

                    foundSpots2[name + Vaccine_type + str(date)] = capacity2
                    print()
                    print("Added " + name + Vaccine_type + str(
                        date) + "SECOND DOSE_______________1________________" + " " + str(
                        capacity2))
                    print()

                    if len(List_18_2) == maxListLength:
                        print("Sending 18+ Vacancies:", len(List_18_2), "for 2nd Dose1")
                        sendMessages(List_18_2, 7702)
                        List_18_2 = []

                    if not Already_On:
                        Already_On = True




                elif foundSpots2[name + Vaccine_type + str(date)] + 10 < capacity2:
                    print()
                    print(name[0:10], capacity1, capacity2, foundSpots2[name + Vaccine_type + str(date)])
                    print()
                    print("New DATA:", capacity2, "Old DATA:", foundSpots2[name + Vaccine_type + str(date)])

                    Found = True

                    ID_2 = int(str(ID) + "2")
                    List_18.append((Vaccine_type, name, date, pin_code,
                                    capacity1, capacity2, RegistrationURL, ID, 18, cost))

                    foundSpots2[name + Vaccine_type + str(date)] = capacity2
                    print()
                    print("Added " + name + Vaccine_type + str(
                        date) + " SECOND DOSE_____________2_________________" + " " + str(capacity1))
                    print()

                    if len(List_18_2) == maxListLength:
                        print("Sending 18+ Vacancies:", len(List_18_2), "for 2nd Dose2")
                        sendMessages(List_18_2, 7702)
                        List_18_2 = []

                    if not Already_On:
                        Already_On = True

                elif foundSpots2[name + Vaccine_type + str(date)] > capacity2:
                    print("1Decreased capacity of", name + " " + Vaccine_type + "2", "from",
                          foundSpots2[name + Vaccine_type + str(date)], "to", capacity2)
                    foundSpots2[name + Vaccine_type + str(date)] = capacity2

            # elif min_age_limit == 45:
            #
            #
            #     if (name not in foundSpots) and (name not in longDelay):
            #         Found = True
            #
            #         List_45.append((Vaccine_type, name, date, pin_code,
            #                         capacity1, capacity2, RegistrationURL, 45, 45, cost))
            #
            #         if cost != "Free" and capacity1 > 250:
            #             longDelay[name] = time.time()
            #             print("Added " + name, "for 45+   [Long Delay]")
            #             print()
            #         else:
            #             foundSpots[name] = time.time()
            #             print("Added " + name, "for 45+")
            #             print()
            #
            #         if len(List_45) == maxListLength:
            #             print("Sending 45+ Vacancies:", len(List_45))
            #             sendMessages(List_45, 45)
            #             List_45 = []
            #
            #         # makeMessage(Vaccine_type, name, date, pin_code,
            #         #             capacity1, capacity2, RegistrationURL, 45, 45, cost)

            # print()
            # print()

        counts += 1

    if len(List_18) != 0:
        print("Sending 18+ Vacancies3:", len(List_18))
        sendMessages(List_18, 770)
        List_18 = []

    if len(List_18_2) != 0:
        print("Sending 18+ Vacancies:", len(List_18_2), "for 2nd Dose3")
        sendMessages(List_18_2, 7702)
        List_18_2 = []

    return Found, counts


# os.environ['TZ'] = 'Asia/Kolkata'
# time.tzset()


AHM = 770
GHN = 772
GHN2 = 153
SUR = 776

loops = 0
delay = 3.4

time.sleep(1)
print("Testing...")

v = "COVISHIELD"
n = "K D HOSPITAL"
d = "Today1"
p = 380000
c1 = 100
c2 = 0
ID = 0
makeMessage(v, n, d, p, c1, c2, RegistrationURL, ID, 18, "1500")

Days1 = "1-06-2021"
Days2 = "3-06-2021"
while True:
    loops += 1

    GotSomething = False

    try:

        today = datetime.now()
        today.replace(tzinfo=timezone.utc)

        # print(today.strftime("%H: %M: %S"))
        HR = int(today.strftime("%H"))
        if HR > 13:
            change = 1
        else:
            change = 0

        Days2 = (str(int(today.strftime("%d")) + change) +
                 (today.strftime("-%m-%y")))

        Days1 = (str(int(today.strftime("%d")) + change + 1) +
                 (today.strftime("-%m-%y")))

        if "31" in Days2:
            Days2 = "01-07-2021"
        if "31" in Days1:
            Days1 = "01-07-2021"

        found, count = GetSlots(Days2, AHM)
        time.sleep(delay)

        # found1, count1 = GetSlots(Days1, AHM)
        # time.sleep(delay)
        #
        # found, count = GetSlots(Days2, AHM)
        # time.sleep(delay)

        # found1, count1 = GetSlots(Days2, GHN)
        # time.sleep(delay)
        # found2, count2 = GetSlots(Days2, GHN2)
        # time.sleep(delay)
        # found3, count3 = GetSlots(Days2, SUR)
        # time.sleep(delay)

        try:
            count = count  # + count1 #+ count3 #count1 + count2 + count3
        except Exception as e:
            print("Sum of count error")
            print(str(e))

        if loops == 10:
            print(Days2, Days1, time.strftime("%I: %M: %S"))
            loops = 0
        GotSomething = True

    except Exception as e:

        print("ERROR OCCURRED")
        print(str(e))
        # ringRepeat(5)
        time.sleep(5)

    if GotSomething:
        p = 0
        # print(found, count, loops)
        '''
        if len(foundSpots) > 0:
            for name in list(foundSpots):

                if time.time() - foundSpots[name] > 1800:
                    print("Removed " + str(name))
                    del foundSpots[name]

        if len(longDelay) > 0:
            for name in list(longDelay):

                if time.time() - longDelay[name] > 7200:
                    print("Removed " + str(name) + " from Long Delay")
                    del longDelay[name]
        '''

        if not count:
            print("Zero Counts", time.strftime("%I: %M: %S"))
            p = 1
            pass

        if (type(found)) == str:
            p = 1
            # print("STRING")
            if "Samee" in found:
                print("Same Data received", str(time.strftime("%I: %M: %S")))

        if not found:
            p = 1
            print("No New Open Slots in " + str(count) +
                  " Spaces. Time: " + str(time.strftime("%I: %M: %S")))

        if found == "False":
            p = 1
            print("No Open Slots in " + str(count) +
                  " Spaces. Time: " + str(time.strftime("%I: %M: %S")))

        # print(time.strftime("%I: %M: %S"))
