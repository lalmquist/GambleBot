import psutil

def main():
        connect()

def Bootreturn():
        boot = (psutil.boot_time()/100000000)
        bootstr = str(boot)
        return bootstr

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

        # 1 - Red
        # 2 - Blue
        # 3 - Green
        # 4 - White
        
        if isRunning('7DaysToDie.exe'):
            return '1'
        elif isRunning('ForzaHorizon4.exe'):
            return '2'
        elif isRunning('chrome.exe'):
            return '2'
        elif isRunning('Steam.exe'):
            return '3'
        elif isRunning('Battle.net.exe'):
            return '4'
        else:
            return '0'
        
def connect():
        import time
        import socket
        Booting = 1
        MESSAGE = ''
        PreviousRunning = '999'
        RunningProgram = '999'

        TCP_IP = '192.168.1.100'
        TCP_PORT = 5008
        BUFFER_SIZE = 1024
        while True:
                try:        
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((TCP_IP, TCP_PORT))
                    if Booting == 1:
                        MESSAGE = Bootreturn()
                        s.sendall(MESSAGE.encode('utf-8'))
                        data = s.recv(BUFFER_SIZE)
                        print(data)
                        Booting = 0
                    while Booting == 0:
                        RunningProgram = CheckProgs()
                        MESSAGE = RunningProgram
                        if RunningProgram != PreviousRunning:
                            s.sendall(MESSAGE.encode('utf-8'))
                            data = s.recv(BUFFER_SIZE)
                            print(data)
                            PreviousRunning = RunningProgram
                            if data == "disc":
                                s.close()
                    MESSAGE = "disconnect"
                    s.sendall(MESSAGE.encode('utf-8'))
                except:
                    print("Failed Connection")
if __name__ == '__main__':
    main()
