
from Script import Script
from server_enums.Stadiums import Stadiums
import regex

class Server:
    def __init__(self, filepath: str,  stadium: Stadiums):
        self.script = Script(filepath)
        self.stadium = stadium

    def getToken(self) -> str:
        with open("files/token.txt", "r") as token:
            return token.read().strip()

    def getScript(self):
        data = {
            "{{TOKEN}}": f"token: \"{self.getToken()}\",",
            "{{STADIUM}}": f"var MapaPorDefecto = \"{self.stadium.value}\";"
        }

        self.script.addData(data)
        
        return self.script.script