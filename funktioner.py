from m5stack import lcd
import re

def showTimeline(farve1,farve2):
        lcd.clear(farve1)
        fil = open('data.csv', 'r')
        lines = fil.readlines()
        fil.close()

        last_lines = lines[-160:]
        print(last_lines)
        for i in range(len(last_lines)):
            value = 0
            line = last_lines[i][:-1]
            regex = r"\d+"
            if re.match(regex,line):
                value = int(int(line)/38) #skalere med 38, så det kan tegnes på 80 pixels
                print(value)
                lcd.line(i, 80, i, 80-value, color=farve2)
            if (i%32 == 0):
                lcd.line(i,80,i,0, color=0xFFFFFF)

def appendData(data):
    fil = open('data.csv', 'a')
    fil.write(str(data)+"\n")
    fil.close()

def whipeData():
    fil = open('data.csv', 'w')
    fil.write("new\n")
    fil.close()
