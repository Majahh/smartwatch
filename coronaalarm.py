from m5stack import lcd #Basis M5StickC
from m5stack import M5Led
import imu #bibliotek til at bruge beværgelsessensoren
import fusion #en oversætter til de rå sensordata
import funktioner #nogle funktioner vi skal bruge
from m5stack import btnA
from m5stack import btnB
from flowlib import hat

spk = hat.get(hat.SPEAKER)
sensor = imu.IMU() #
myfilter = fusion.MahonyFilter()
lcd.orient(lcd.LANDSCAPE)
state = "start"
count = 0
hit = 0
lcd.clear(0x000000)
funktioner.appendData(0)

while True:
    if state == "start": #0
        lcd.text(10,10,"reset tryk B")
        lcd.text(10,40,"continue tryk A")
        if btnA.wasPressed():
            lcd.clear(0x000000)
            M5Led.on()
            state = "monitor" #1
        if btnB.wasPressed():
            funktioner.whipeData()
            lcd.clear(0x000000)
            lcd.text(10,10,"data er blevet slettet")
            lcd.text(10,40,"continue tryk A")
            state = "pause"
    if state == "monitor":
        #opdater sensordata
        myfilter.update(sensor.acceleration, sensor.gyro)
        pitch = int(myfilter.pitch)
        roll = int(myfilter.roll)
        count += 1
        #insæt grænser for pitch og roll
        if 3 < pitch < 29 and 67 < roll < 99:
            hit += 1
            if (hit %50 == 0):
                spk.sing(440, 1/2)
            print(hit)
        if count > 3000: #3000 er ca 30 sekunder.
            funktioner.appendData(hit)
            hit = 0
            count = 0
        if btnA.wasPressed():
            M5Led.off()
            funktioner.showTimeline(0xFF0000, 0xFFFF00)
            state = "pause" #2
    if state == "pause": #2
        if btnA.wasPressed():
            M5Led.on()
            lcd.clear(0x000000)
            state = "monitor" #1
