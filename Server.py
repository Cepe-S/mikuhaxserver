class Server:

    def __init__(self, cancha):
        self.cancha = cancha

    def GetScript(self):
        with open("script1.js", "r", encoding="utf-8") as script:
            return script.read()