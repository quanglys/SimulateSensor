# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import random
import time
import _thread

strParentPath = ""

def readConfig():
    f = open(strParentPath + '/SimulateSensor/config/config.cfg', 'r')
    global ipMos
    global strMosIn
    global strMosOut
    global timePeriod
    timePeriod = []
    ipMos = f.readline().replace('\n', '')
    strMosIn = f.readline().replace('\n', '')
    strMosOut = f.readline().replace('\n', '')
    global numberSensor
    numberSensor = int(f.readline())
    for i in range(0, numberSensor):
        temp = int(f.readline())
        timePeriod.append(temp)
    f.close()


# Number    MyTemperature  "Temperature [%.1f °C]"         {mqtt="<[mos:/temp:state:default], >[mos:/out:state:*:default]"}
def writeItemFile():
    try:
        f = open(strParentPath + '/openhab/items/demo.items', 'w')
        for i in range(0, numberSensor):
            f.write('Number Sensor' + str(i) + ' "Value [%.1f]" {mqtt="<[mqttIn:' + strMosIn + str(
                i) + ':state:default], >[mqttOut:'+ strMosOut + str(i) + ':state:*:default]"}' + '\n')
    except IOError:
        print ('Can not open file item\n')
    else:
        f.close()


# sitemap demo label="Demo House"
# {
# 	Text item=MyTemperature
# }
def writeSitemapFile():
    try:
        f = open(strParentPath + '/openhab/sitemaps/demo.sitemap', 'w')
        f.write('sitemap demo label="Demo House"\n{' + '\n')
        for i in range(0, numberSensor):
            f.write('Text item=Sensor' + str(i) + '\n')
        f.writelines('}')
    except IOError:
        print ('Can not open file sitemap\n')
    else:
        f.close()


def sendData(i):
    while bStop:
        mqttc.publish(strMosIn + str(i), random.randint(-100, 100))
        time.sleep(timePeriod[i] * MILISECOND)


MILISECOND = 0.001
readConfig()
mqttc = mqtt.Client('python_pub')
mqttc.connect(ipMos, 1883)
bStop = 1
writeItemFile()
writeSitemapFile()
try:
    # sendData(0)
    for i in range(0, numberSensor):
        _thread.start_new_thread(sendData, (i,))
except:
    print ('Can not create thread\n')

while bStop:
    time.sleep(1)

