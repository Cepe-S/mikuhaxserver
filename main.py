from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from Server import Server
import regex

isServerOpen = False

def runServer():
      
    with open("browser_path.txt", "r") as f:
        chrome_path = f.read().strip()  

    chrome_service = ChromeService(executable_path=chrome_path)
    
    driver = webdriver.Chrome(service=chrome_service)
    driver.get("https://html5.haxball.com/headless")



    server1 = Server("cancha")
    driver.execute_script(server1.GetScript())
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
