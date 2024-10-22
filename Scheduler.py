from WebDriver import WebDriver as wd
from Server import Server
from ServerDoctor import ServerDoctor as Doctor

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

class Scheduler:
    def __init__(self, driver: wd, server: Server):
        self.driver = driver
        self.server = server
        self.scheduler = AsyncIOScheduler()
        self.server_running = False
        self.server_task = None

    async def runServer(self):
        self.driver.getPage("https://html5.haxball.com/headless")
        self.driver.runScript(self.server.getScript())
        print("Script ejecutado")

        serverLink = self.server.getServerLink(self.driver)
        print(f"Link encontrado, {serverLink}")
        
        doctor = Doctor(serverLink)
        self.scheduler.add_job(self.checkServerStatus, 'interval', seconds=5*60, args=[doctor])
        self.scheduler.add_job(self.driver.getConsoleLogs, 'interval', seconds=2)

        self.scheduler.start()
        print("Doctor y logger ejecutados")

        while True:
            await asyncio.sleep(1)

    def checkServerStatus(self, doctor: Doctor):
        if not doctor.isServerRunning():
            self.restartServer()

    def startServer(self):
        self.server_task = asyncio.create_task(self.runServer())
        print("===========Servidor iniciado===========")

    def stopServer(self):
        if self.server_task:
            self.server_task.cancel()
            print("===========Servidor detenido===========")

    def restartServer(self):
        self.stopServer()
        self.server_task = asyncio.create_task(self.runServer())