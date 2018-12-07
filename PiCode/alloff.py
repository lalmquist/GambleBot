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
def OFF(color):
	GPIO.output(color, False)
OFF(red)
OFF(yellow)
OFF(white)
OFF(green)
OFF(blue)




