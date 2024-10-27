import cv2
import numpy as np
from pyzbar.pyzbar import decode
import mss
import winsound
import time
import winsound
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

users = [
    {"name": "Valentýna", "surname": "Bujnošková", "email": "valmetalistka@seznam.cz", "phone": "731849514"},
    {"name": "Jana", "surname": "Bujnošková", "email": "janabuj@seznam.cz", "phone": "736770619"},
    {"name": "Jakub", "surname": "Bartoš", "email": "jkbbrts@gmail.com", "phone": "773241834"},
    {"name": "Sebastián", "surname": "Walenta", "email": "sezbastian.walent@gmail.com", "phone": "604164664"}
]
# Funkce pro vyplnění a odeslání formuláře
def fillAndSend(user_data):
    driver = webdriver.Chrome()

    url = 'https://tvrebel.cz/soutezim-s-arch-enemy/'  # Změň na URL stránky s formulářem
    driver.get(url)

    # Časová prodleva, aby se stránka načetla
    random_value = random.uniform(1.3, 2.2)
    time.sleep(random_value)

    # Najdi elementy na stránce podle atributu 'name'
    name_input = driver.find_element(By.NAME, 'NAME')
    surname_input = driver.find_element(By.NAME, 'SURNAME')
    email_input = driver.find_element(By.NAME, 'EMAIL')
    phone_input = driver.find_element(By.NAME, 'PHONE')

    # Vyplnění formuláře
    name_input.send_keys(user_data['name'])
    surname_input.send_keys(user_data['surname'])
    email_input.send_keys(user_data['email'])
    phone_input.send_keys(user_data['phone'])

    # Najdi tlačítko odeslání a klikni na něj
    submit_button = driver.find_elements(By.XPATH, "//button[@type='submit']")
    print(len(submit_button))
    driver.execute_script("arguments[0].scrollIntoView();", phone_input)
    time.sleep(1)
    submit_button[1].click()

    # Počkej na odeslání formuláře
    random_value1 = random.uniform(1.3, 2.2)
    time.sleep(random_value1)

    # Zavři prohlížeč
    driver.quit()

# Inicializace snímače obrazovky
sct = mss.mss()

# Oblast pro snímání obrazovky (např. celá obrazovka)
monitor = sct.monitors[1]  # Index 1 obvykle odpovídá hlavní obrazovce

while True:
    # Snímek obrazovky
    img = sct.grab(monitor)
    
    # Převod na numpy array
    frame = np.array(img)

    # Převod do BGR formátu (mss vrací obrázek v BGRA)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # Zvětšení snímku (zoom)
    zoom_factor = 0.5
    height, width = frame.shape[:2]
    new_height = int(height * zoom_factor)
    new_width = int(width * zoom_factor)
    
    # Změna velikosti obrazu
    zoomed_frame = cv2.resize(frame, (new_width, new_height))

    # Dekóduj QR kód ze snímku
    qr_codes = decode(zoomed_frame)

    # Projdi všechny nalezené QR kódy v obrázku
    for qr_code in qr_codes:
        # Dekódovaný text z QR kódu
        qr_data = qr_code.data.decode('utf-8')
        print("QR Code Detected:", qr_data)

        # Vyplň a odešli formulář, pokud byl QR kód nalezen
        if("tvrebel" in qr_data):
            #random.shuffle(users)
            #for user in users:
                #fillAndSend(user)
            winsound.Beep(1000,1000)
            time.sleep(0.6)
            print("Right:"+qr_data)
        else:
            print("False:"+qr_data)

    # Zobraz snímek obrazovky
    cv2.imshow('Screen QR Code Scanner', zoomed_frame)

    # Stisknutím 'q' zavřeš aplikaci
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Uvolnění prostředků
cv2.destroyAllWindows()