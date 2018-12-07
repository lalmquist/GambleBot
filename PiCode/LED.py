import RPi.GPIO as GPIO
import time
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


# loops
y = 0
# sleep time
x = 0.25

def LED(color):
	GPIO.output(color,True)
        time.sleep(x)
        GPIO.output(color,False)


while y < 10:

	LED(red)
	LED(yellow)
	LED(white)
	LED(green)
	LED(blue)
	LED(blue)
	LED(green)
	LED(white)
	LED(yellow)
	LED(red)

	y = y 
