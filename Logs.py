import datetime

class Logs:
    def __init__(self, date: datetime):
        self.date = date

    def getFilename(self) -> str:
        return self.date.strftime("%Y-%m-%d_%H-%M-%S.log")

    def addLog(self, message: str):
        filename = self.getFilename()
        filepath = "logs/" + filename
        toLog = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ": " + message + "\n"
        with open(filepath, "a", encoding='utf-8') as logfile:
            logfile.write(toLog)