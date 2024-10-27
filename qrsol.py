import argparse
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import mss
import winsound
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

parser = argparse.ArgumentParser(description="Popis vašeho programu")

#parser.add_argument("--beep", type=bool, default=False, help="Beep mode => no autofill")
parser.add_argument("--beep", action="store_true", help="Beep mode => no autofill")
args = parser.parse_args()

users = [
    {"name": "Valentýna", "surname": "Bujnošková", "email": "valmetalistka@seznam.cz", "phone": "731849514"},
    {"name": "Jana", "surname": "Bujnošková", "email": "janabuj@seznam.cz", "phone": "736770619"},
    {"name": "Jakub", "surname": "Bartoš", "email": "jkbbrts@gmail.com", "phone": "773241834"},
    {"name": "Sebastián", "surname": "Walenta", "email": "sezbastian.walent@gmail.com", "phone": "604164664"}
]
def fillAndSend(user_data,url):
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.get(url)

    time.sleep(2)

    name_input = driver.find_element(By.NAME, 'NAME')
    surname_input = driver.find_element(By.NAME, 'SURNAME')
    email_input = driver.find_element(By.NAME, 'EMAIL')
    phone_input = driver.find_element(By.NAME, 'PHONE')

    name_input.send_keys(user_data['name'])
    surname_input.send_keys(user_data['surname'])
    email_input.send_keys(user_data['email'])
    phone_input.send_keys(user_data['phone'])

    submit_button = driver.find_elements(By.XPATH, "//button[@type='submit']")
    print(len(submit_button))
    driver.execute_script("arguments[0].scrollIntoView();", phone_input)
    time.sleep(1)
    submit_button[1].click()

    random_value = random.uniform(1.3, 2.2)
    time.sleep(random_value)

    driver.quit()

sct = mss.mss()
monitor = sct.monitors[1]  # Index 1 obvykle odpovídá hlavní obrazovce

while True:
    img = sct.grab(monitor)
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    zoom_factor = 0.5
    height, width = frame.shape[:2]
    new_height = int(height * zoom_factor)
    new_width = int(width * zoom_factor)
    
    zoomed_frame = cv2.resize(frame, (new_width, new_height))

    qr_codes = decode(zoomed_frame)

    for qr_code in qr_codes:
        qr_data = qr_code.data.decode('utf-8')
        print("QR Code Detected:", qr_data)

        if("tvrebel" in qr_data):
            if(args.beep):
                winsound.Beep(1000,1000)
                time.sleep(0.6)
            else:
                random.shuffle(users)
                for user in users:
                    fillAndSend(user,qr_data)
                print("Right:"+qr_data)
        else:
            print("False:"+qr_data)

    cv2.imshow('Screen QR Code Scanner', zoomed_frame)

    # Stisknutím 'q' zavřeš aplikaci
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()