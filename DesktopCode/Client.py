import psutil

def main():
        connect()

def CPUreturn():
        cpu = psutil.cpu_percent(interval = 0.5)
        cpustr = str(cpu)
        return cpustr
def Bootreturn():
        boot = (psutil.boot_time()/100000000)
        bootstr = str(boot)
        return bootstr
        
def connect():
        import time
        import socket
        Booting = 1
        MESSAGE = ''

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
                        MESSAGE = CPUreturn()
                        time.sleep(1)
                        s.sendall(MESSAGE.encode('utf-8'))
                        data = s.recv(BUFFER_SIZE)
                        print(data)
                        if data == "disc":
                                s.close()

                    MESSAGE = "disconnect"
                    s.sendall(MESSAGE.encode('utf-8'))
                except:
                    print("Failed Connection")
if __name__ == '__main__':
    main()
