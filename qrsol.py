import cv2
import numpy as np
from pyzbar.pyzbar import decode
import mss
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Funkce pro vyplnění a odeslání formuláře
def fillAndSend(qr_data):
    # Cesta k chromedriveru (změň na svou vlastní cestu)
    driver_path = '/path/to/chromedriver'

    # Inicializace prohlížeče Chrome
    driver = webdriver.Chrome()

    # Načti webovou stránku
    url = 'https://tvrebel.cz/soutezim-s-arch-enemy/'  # Změň na URL stránky s formulářem
    driver.get(url)

    # Časová prodleva, aby se stránka načetla
    time.sleep(2)

    # Najdi elementy na stránce podle atributu 'name'
    name_input = driver.find_element(By.NAME, 'NAME')
    surname_input = driver.find_element(By.NAME, 'SURNAME')
    email_input = driver.find_element(By.NAME, 'EMAIL')
    phone_input = driver.find_element(By.NAME, 'PHONE')

    # Vyplnění formuláře
    name_input.send_keys('Sebastián')
    surname_input.send_keys('Walenta')
    email_input.send_keys('sebastian.walent@gmail.com')
    phone_input.send_keys('604164664')

    # Najdi tlačítko odeslání a klikni na něj
    submit_button = driver.find_elements(By.XPATH, "//button[@type='submit']")
    print(len(submit_button))
    driver.execute_script("arguments[0].scrollIntoView();", phone_input)
    time.sleep(1)
    submit_button[1].click()

    # Počkej na odeslání formuláře
    time.sleep(10)

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
            fillAndSend(qr_data)
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
