import time
TempProbe = "28-051760d567ff"

def read(i):
    location = '/sys/bus/w1/devices/'+i+'/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celcius = temperature / 1000
    farenheit = (celcius * 1.8) + 32
    return farenheit

while 1:
    print(read(TempProbe))
    #time.sleep(5)
