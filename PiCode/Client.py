import time
import socket
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

#Define colors to IO points
red = 18
yellow = 23
white = 17
green = 22
blue = 27

def LED(color):
	GPIO.output(color,True)
        time.sleep(x)
        GPIO.output(color,False)

TCP_IP = '192.168.1.100'
TCP_PORT = 5008
BUFFER_SIZE = 1024
MESSAGE = "Combat"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while data != "disc":
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)
	i = i + 1
	print i
	print "received data:" , data
	if data == "disc":
		s.close()

MESSAGE = "disconnect"
s.send(MESSAGE)
