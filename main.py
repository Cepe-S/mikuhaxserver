from Server import Server
from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from sys import platform
import regex
from server_enums.Stadiums import Stadiums
from time import sleep

isServerOpen = False

def createDriver():
    chromeOptions = ChromeOptions()
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument('--headless')

    if "linux" in platform:
        return webdriver.Chrome(service=ChromeService(executable_path="/usr/bin/chromedriver"), 
                                options=chromeOptions)
    
    return webdriver.Chrome(options=chromeOptions)

def runServer():

    driver = createDriver()
    driver.get("https://html5.haxball.com/headless")

    server1 = Server(stadium=Stadiums.FUTSAL_X7, filepath="files/script.js")
    # with open("servermodified.js", "w", encoding="utf-8") as file:
    #     file.write(server1.getScript())

    driver.execute_script(server1.getScript())
    
    sleep(5)
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@src, '30xIZB1N/__cache_static__/g/headless.html')]")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "roomlink")))
    pageSource = driver.page_source
    print(pageSource)
    while (1 != 0):
        sleep(9000000000)

while not isServerOpen:
    try:
        if (not isServerOpen):
            runServer()
            isServerOpen = True
    except JavascriptException as e:
        isServerOpen = False
        print(e)