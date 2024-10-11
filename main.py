from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from Server import Server
import regex

isServerOpen = False

def runServer():
    driver = webdriver.Chrome()
    driver.get("https://html5.haxball.com/headless")
    # sleep(10)
    # driver.refresh()
    
    server1 = Server("cancha")
    driver.execute_script(server1.GetScript())
    sleep(5)
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@src, '30xIZB1N/__cache_static__/g/headless.html')]")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "roomlink")))
    pageSource = driver.page_source
    print(pageSource)
    sleep(900)

while not isServerOpen:
    try:
        if (not isServerOpen):
            runServer()
            isServerOpen = True
    except JavascriptException as e:
        isServerOpen = False
        print(e)

sleep(1000000)
