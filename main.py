import asyncio

from ServerDoctor import ServerDoctor as Doctor
from Server import Server
from DiscordLinks import DiscordLinks
from WebDriver import WebDriver as wd
from server_enums.Stadiums import Stadiums
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from time import sleep
from Logs import Logs
import datetime

isServerOpen = False
logger = Logs(datetime.datetime.now())

def restartServer():
    True #

async def checkServerStatus(doctor: Doctor):
    if not doctor.isServerRunning():
        restartServer()
        return
    


def getLogs(driver: wd):
    driver.getConsoleLogs()

async def runServer():
    driver = wd(["--no-sandbox", "--disable-dev-shm-usage", "--headless"], "/usr/bin/chromedriver")

    discordLinks = DiscordLinks(
        "discord.gg/2UXsPaHRHq",
        "https://discord.com/api/webhooks/1297254030535295026/NPjKlluTgQFjfIuhm1n8B-j8G-kQLuES7fchx2b-TLRMED7sCDjVsmUNwnh_i3bgCq69",
        "https://discord.com/api/webhooks/1294134671717957763/bEuXT5GqgiqP0HFkQHcFIwPDr6_elMhzF5nUCfWnWSZGI8hzHZ8fbSbEvVRdZ5ca0_1S",
        "https://discord.com/api/webhooks/1294345171764248586/D3D2XTB9HL7n7iFV5xlykuX5CAVfc_Kg8p1M9vVQ9P7vNXAxHDEc3-VwrTuw_Fr4LrqL"
    )

    server = Server(stadium=Stadiums.FUTSAL_X7, 
                     filepath="files/script.js", 
                     gameTime=10, 
                     goalLimit=4, 
                     dsLinks=discordLinks)

    driver.getPage("https://html5.haxball.com/headless")
    driver.runScript(server.getScript())

    scheduler = AsyncIOScheduler()

    scheduler.add_job(getLogs, 'interval', seconds=2, args=[driver])

    serverLink = server.getServerLink(driver)
    doctor = Doctor(serverLink)
    scheduler.add_job(checkServerStatus, 'interval', seconds=5*60, args=[doctor])

    print(serverLink)


if __name__ == "__main__":
    asyncio.run(runServer())