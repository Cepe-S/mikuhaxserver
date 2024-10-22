from Server import Server
from DiscordLinks import DiscordLinks
from WebDriver import WebDriver as wd
from Scheduler import Scheduler
from server_enums.Stadiums import Stadiums

import asyncio

discordLinks = DiscordLinks(
    "discord.gg/2UXsPaHRHq",
    "https://discord.com/api/webhooks/1297254030535295026/NPjKlluTgQFjfIuhm1n8B-j8G-kQLuES7fchx2b-TLRMED7sCDjVsmUNwnh_i3bgCq69",
    "https://discord.com/api/webhooks/1294134671717957763/bEuXT5GqgiqP0HFkQHcFIwPDr6_elMhzF5nUCfWnWSZGI8hzHZ8fbSbEvVRdZ5ca0_1S",
    "https://discord.com/api/webhooks/1294345171764248586/D3D2XTB9HL7n7iFV5xlykuX5CAVfc_Kg8p1M9vVQ9P7vNXAxHDEc3-VwrTuw_Fr4LrqL"
)

mainserver = Server(hostName="🟦🟦🟦 miku server juegan todos 🟦🟦🟦",
                stadium=Stadiums.FUTSAL_X7, 
                filepath="files/script.js", 
                gameTime=10, 
                goalLimit=4, 
                dsLinks=discordLinks)

testserver = Server(hostName="miku testing :3",
                stadium=Stadiums.FUTSAL_X7, 
                filepath="files/script.js", 
                gameTime=10, 
                goalLimit=4, 
                dsLinks=DiscordLinks("", "", "", ""))


# TODO: Control para usar el chat desde la consola


async def main():
    driver = wd(["--no-sandbox", "--disable-dev-shm-usage", "--headless"], "/usr/bin/chromedriver")
    server = testserver
    scheduler = Scheduler(driver, server)
    scheduler.startServer()

if __name__ == "__main__":
    asyncio.run(main())