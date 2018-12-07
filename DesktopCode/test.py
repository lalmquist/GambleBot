import psutil

def isRunning(Program):
        found = 0
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['name'])
            except psutil.NoSuchProcess:
                pass
            if Program in pinfo['name']:
                found = 1
        if found == 1:
            return 1
        else:
            return 0

def CheckProgs():
        # list of programs to check
        # steam
        # blizzard
        # chrome
        if isRunning('chrome.exe'):
            return 1
        elif isRunning('Steam.exe'):
            return 2
        elif isRunning('Battle.net.exe'):
            return 3
        else:
            return 0
test = CheckProgs()
print(test)
