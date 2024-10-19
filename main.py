from Server import Server
from DiscordLinks import DiscordLinks

from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from sys import platform
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
    chromeOptions.add_experimental_option("detach", True)

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

    discordLinks = DiscordLinks(
        "discord.gg/2UXsPaHRHq",
        "https://discord.com/api/webhooks/1297254030535295026/NPjKlluTgQFjfIuhm1n8B-j8G-kQLuES7fchx2b-TLRMED7sCDjVsmUNwnh_i3bgCq69",
        "https://discord.com/api/webhooks/1294134671717957763/bEuXT5GqgiqP0HFkQHcFIwPDr6_elMhzF5nUCfWnWSZGI8hzHZ8fbSbEvVRdZ5ca0_1S",
        "https://discord.com/api/webhooks/1294345171764248586/D3D2XTB9HL7n7iFV5xlykuX5CAVfc_Kg8p1M9vVQ9P7vNXAxHDEc3-VwrTuw_Fr4LrqL"
    )

    server1 = Server(stadium=Stadiums.FUTSAL_X7, 
                     filepath="files/script.js", 
                     gameTime=10, 
                     goalLimit=4, 
                     dsLinks=discordLinks)

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