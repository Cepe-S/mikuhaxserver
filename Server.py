
from Script import Script
from DiscordLinks import DiscordLinks
from server_enums.Stadiums import Stadiums
import regex

class Server:
    def __init__(self, filepath: str,  stadium: Stadiums, gameTime: int, goalLimit: int, dsLinks: DiscordLinks):
        self.script = Script(filepath)
        self.stadium = stadium
        self.gameTime = gameTime
        self.goalLimit = goalLimit
        self.dsLinks = dsLinks

    def getToken(self) -> str:
        with open("files/token.txt", "r") as token:
            return token.read().strip()

    def getScript(self):
        data = {
            "{{TOKEN}}": f"token: \"{self.getToken()}\",",
            "{{STADIUM}}": f"var MapaPorDefecto = \"{self.stadium.value}\";",
            "{{GAMETIME}}": f"var TiempoDeJuego = {self.gameTime};",
            "{{GOAL_LIMIT}}": f"var LimiteDeGoles = {self.goalLimit};",
            "{{DS_RECORDS_LINK}}": f"const GrabacionesDiscord = \"{self.dsLinks.server}\";",
            "{{DS_RECORDS_HOOK}}": f"const WebhookGrabaciones = \"{self.dsLinks.records}\";",
            "{{DS_KICKBANS}}": f"const AnuncioKicksBans = \"{self.dsLinks.kickBans}\";",
            "{{DS_SERVER_OPEN}}": f"var AnuncioHostAbierto = \"{self.dsLinks.hostOpen}\";",
            "{{DS_LINK}}": f"const DiscordLink = \"{self.dsLinks.server}\";"
        }

        self.script.addData(data)
        
        return self.script.script