import requests
import datetime
import winsound
import time
import threading
import socket
import json
from pynput.keyboard import Key, Controller

RegistrationURL = "https://selfregistration.cowin.gov.in/"
keyboard = Controller()

CONNECT = False
Already_On = False
TYPE = False

foundSpots = {}
to_remove = {}

if CONNECT:
    host = "192.168.86.27"
    port = 5000

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server


def typeMessage(message, URL):
    print(message)
    print(URL)
    if TYPE:
        message = str(message)
        keyboard.type(message)

        keyboard.press(Key.ctrl_l)
        keyboard.tap(Key.enter)
        keyboard.release(Key.ctrl_l)

        keyboard.type(URL)
        keyboard.tap(Key.enter)


'''
Slot Found at APOLLO HOSPITALS CITY CENTRE on 15-05-2021 and 1 seat(s) availablehttps://selfregistration.cowin.gov.in/
Slot Found at APOLLO HOSPITALS CITY CENTRE on 15-05-2021 and 1 seat(s) availablehttps://selfregistration.cowin.gov.in/



'''


def ringRepeat(num):
    global Already_On

    for i in range(5):
        winsound.PlaySound("point.wav", winsound.SND_ASYNC)
        time.sleep(0.6)
        winsound.PlaySound("hit.wav", winsound.SND_ASYNC)

    time.sleep(200)
    Already_On = False


def on_and_off(delay=1.5):
    global Already_On

    pos = "bright"
    client_socket.send(pos.encode())

    for i in range(3):
        pos = "Off"
        client_socket.send(pos.encode())
        time.sleep(delay)
        pos = "On"
        client_socket.send(pos.encode())
        time.sleep(delay)

    time.sleep(200)
    Already_On = False


def GetSlots():
    global Already_On, foundSpots
    Found = False

    today = datetime.datetime.now()
    Days1 = (str(int(today.strftime("%d")) - 0) + (today.strftime("-%m-%y")))

    URL = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=770&date={Days1}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

    r = requests.get(URL, headers=headers)

    if str(r) != "<Response [200]>":
        print("ERROORRRRR")
        print(str(r))
        time.sleep(5)
        return Found, Found

    data = r.json()
    centers = data["centers"]
    counts = 0

    for center in centers:

        name = center["name"]
        pin_code = center["pincode"]
        for session in center["sessions"]:
            date = session["date"]
            min_age_limit = session["min_age_limit"]
            capacity = session["available_capacity"]
            if capacity > 0:
                # print(counts, name, pin_code, date, min_age_limit, capacity)
                print(
                    f"Name: {name}    Capacity: {capacity}    Date: {date}    Age Limit: {min_age_limit}    Pincode: {pin_code}")
                Found = True

                if min_age_limit < 45:

                    if name not in foundSpots:
                        # print(f"Slot Found at {name} on {date} and {capacity} seat(s) available. Pincode: {pin_code}")
                        message2Send = f"Slot Found at {name} on {date} and {capacity} seat(s) available. Pincode: {pin_code}"
                        typeMessage(message2Send, RegistrationURL)
                        # print(RegistrationURL)
                        foundSpots[name] = time.time()
                        print(f"Added {name}")

                        t1 = threading.Thread(target=on_and_off, args=[1])
                        t2 = threading.Thread(target=ringRepeat, args=[1])

                        if not Already_On:
                            Already_On = True
                            t1.start()
                            t2.start()

                print()
                print()
            counts += 1
    return Found, counts


while True:
    found, count = GetSlots()
    if len(foundSpots) > 0:
        for name in list(foundSpots):
            if time.time() - foundSpots[name] > 300:
                print(f"Removed {name}")
                del foundSpots[name]
    if not count:
        time.sleep(15)
        continue
    if not found:
        print("No Open Slots in " + str(count) +
              "  Spaces. Time: " + str(time.strftime("%I: %M: %S")))
        time.sleep(3.34)
