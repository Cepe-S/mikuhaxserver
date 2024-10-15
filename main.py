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
from Logs import Logs
import datetime

isServerOpen = False
logger = Logs(datetime.datetime.now())

def createDriver() -> webdriver.Chrome:
    chromeOptions = ChromeOptions()
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument('--headless')
    chromeOptions.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    if "linux" in platform:
        return webdriver.Chrome(service=ChromeService(executable_path="/usr/bin/chromedriver"), 
                                options=chromeOptions)
    
    return webdriver.Chrome(options=chromeOptions)

def getConsoleLogs(driver: webdriver):
    logs = driver.get_log("browser")
    for entry in logs:
        log = f"{entry['level']}: {entry['message']}"
        print(log)
        logger.addLog(log)

def runServer():
    driver = createDriver()
    driver.get("https://html5.haxball.com/headless")

    server1 = Server(stadium=Stadiums.FUTSAL_X7, filepath="files/script.js")

    driver.execute_script(server1.getScript())
    sleep(5)
    pageSource = driver.page_source
    print(pageSource)

    while True:
        getConsoleLogs(driver)
        sleep(2)

while not isServerOpen:
    try:
        if (not isServerOpen):
            runServer()
            isServerOpen = True
    except JavascriptException as e:
        isServerOpen = False
        print(e)