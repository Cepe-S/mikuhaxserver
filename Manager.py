from WebDriver import WebDriver as wd
from ServerDoctor import ServerDoctor as Doctor
from UI import UI
from Server import Server
from server_enums.OutputType import OutputType as outType

from time import sleep
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import inspect

class Manager:
    def __init__(self, driver: wd, server: Server, ui: UI):
        self.driver = driver
        self.server = server
        self.ui = ui
        self.scheduler = AsyncIOScheduler()
        self.server_running = False
        self.server_task = None
        self.doctor = None
        self.keepRunning = True

    async def runServer(self):
        try:
            if not self.isTokenValid(self.server.token):
                return

            self.ui.toConsole("Initializing server", outType.PROGRAM, True)

            page = "https://html5.haxball.com/headless"
            await asyncio.to_thread(self.driver.getPage, page)
            self.ui.toConsole(f"Page {page} connected.", outType.PROGRAM, True)
            
            await asyncio.to_thread(self.driver.runScript, self.server.getScript())
            self.ui.toConsole("Script ejecuted", outType.PROGRAM, True)

            serverLink = await asyncio.to_thread(self.server.getServerLink, self.driver)
            self.ui.toConsole(f"Link found: {serverLink}", outType.PROGRAM, True)

            self.doctor = Doctor(serverLink)
            self.scheduler.add_job(self.checkServerStatus, 'interval', seconds=5*60, args=[self.doctor])
            self.scheduler.add_job(self.driver.getConsoleLogs, 'interval', seconds=2, args=[True])

            self.scheduler.start()
            self.ui.toConsole("Doctor and logger executed", outType.PROGRAM, True)

            while self.keepRunning:
                await asyncio.sleep(1)

        except Exception as e:
            self.ui.toConsole(f"Error en runServer: {str(e)}", outType.PROGRAM, True)

    def checkServerStatus(self, doctor: Doctor):
        if not doctor.isServerRunning():
            self.restartServer()

    def startServer(self):
        self.keepRunning = True
        self.server_task = asyncio.create_task(self.runServer())

    def stopServer(self):
        if self.server_task:
            self.ui.toConsole("Cerrando servidor", outType.PROGRAM, True)
            self.server_task.cancel()
            self.keepRunning = False
            sleep(5)
            self.ui.toConsole("Servidor cerrado", outType.PROGRAM, True)

    def restartServer(self):
        self.stopServer()
        self.startServer()

    def getServerStatus(self):
        if not self.doctor: self.ui.toConsole("The doctor is sleeping...", outType.ERROR, True)

        isServerRunning = self.doctor.isServerRunning()
        if isServerRunning: self.ui.toConsole("The server is open", outType.PROGRAM, True)
        if not isServerRunning: self.ui.toConsole("The server is closed", outType.ERROR, True)

    def isTokenValid(self, token: str):

        self.ui.toConsole("Validating token", outType.PROGRAM, True)
        with open("files/token_validator.js", "r") as file:
            validatorScript = file.read().replace("{{token}}", token)

        driver = wd()

        driver.getPage("https://html5.haxball.com/headless")

        driver.runScript(validatorScript)

        for _ in range(10):
            consoleLogs = driver.getConsoleLogs(False)
            for entry in consoleLogs:
                response = entry["message"]

                if "Token is invalid" in response:
                    self.ui.toConsole("The token is invalid, please update the token with [updatetoken]", outType.ERROR, True)
                    driver.wd.close()
                    return False
                
                if "Valid token" in response:
                    self.ui.toConsole("Token validated", outType.PROGRAM, True)
                    driver.wd.close()
                    return True
                
            sleep(3)

        self.ui.toConsole("No response from token validator", outType.ERROR, True)

    def updateToken(self, token):
        if not len(token) == 39 and token[4] == '.':
            self.ui.toConsole("Wrong token format", outType.ERROR, True)
            return
        
        if not self.isTokenValid(token):
            self.ui.toConsole("Token invalid", outType.ERROR, True)
            return
        
        with open("files/token.txt", "w") as file:
            file.write(token)
        self.server.token = token
        self.ui.toConsole("Token updated", outType.PROGRAM, True)

    def processInput(self, message: str):
        parts = message.split(' ')  
        command = parts[0]  
        args = parts[1:]
        
        commands = {
            "startserver": self.startServer,
            "stopserver": self.stopServer,
            "restartserver": self.restartServer,
            "checkserver": self.getServerStatus,
            "updatetoken": self.updateToken
        }
        func = commands.get(command)

        if func:
            # obtiene el número de argumentos que necesita la función
            sig = inspect.signature(func)
            required_args = len([param for param in sig.parameters.values() if param.default == inspect.Parameter.empty])

            if len(args) == required_args:
                func(*args)
            else:
                self.ui.toConsole(f"El comando '{command}' espera {required_args} argumento(s), pero se recibieron {len(args)}.", outType.ERROR, True)
        else:
            self.ui.toConsole(f"Comando '{command}' no reconocido", outType.ERROR, True)