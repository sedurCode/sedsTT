#!/usr/bin/env python
#Copyright (c) 2017 Adafruit Industries Author: Tony DiCola & James DeVito
import time, sys, os, glob, subprocess
from luma.core.sprite_system import framerate_regulator
from time import sleep
#import Adafruit_GPIO.SPI as SPI
#import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
brite=50
#----------------------------LUMA SETUP-----------------------------------------
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
botserial = i2c(port=1, address=0x3c)
#botserial = i2c(port=1, address=0x3D)

# substitute ssd1331(...) or sh1106(...) below if using that device
#disp = sh1106(botserial)
disp = ssd1306(botserial)
topserial = i2c(port=1, address=0x3C)
#disptop = sh1106(topserial)
disptop = ssd1306(topserial)
#----------------------------------------------

# Raspberry Pi pin configuration:
RST = None # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
#then = time.time()
#print then
line1 = str()
#------------------------------- PI INPUTS ---------------------------------
# pull up GPIO23-25 (tact switches)
up =0
down = 0
select = 0
a = 1
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#-----------------------------------------------------------------------
def filedisp(filename, filepath):
    global files
    path = os.getcwd()
    disp.clear()
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    padding = -2
    top = padding
    bottom = height-padding
    x = 0
    font = ImageFont.load_default()
    font1 = ImageFont.truetype(path+"/Roboto-Bold.ttf",12)
    font2 = ImageFont.truetype(path+"/Roboto-Light.ttf",13)
    font3 = ImageFont.truetype(path+"/Roboto-Bold.ttf",45)
    font4 = ImageFont.truetype(path+"/Roboto-Light.ttf",10)
    font5 = ImageFont.truetype(path+"/Roboto-Regular.ttf",14)
    #draw.rectangle((0,0,127,35), outline=brite, fill=brite)
    #draw.rectangle((1,top+3,117,34), outline=0, fill=brite)
    #draw.rectangle((126,top+3,119,34), outline=0, fill=0)
    #draw.rectangle((126,top+3,119,8), outline=0, fill=brite)
    draw.rectangle((0,0,127,bottom-12), outline=brite, fill=brite)
    draw.rectangle((1,top+3,117,bottom-12), outline=0, fill=brite)
    draw.rectangle((126,top+3,119,bottom-12), outline=0, fill=0)
    draw.rectangle((126,top+3,119,bottom-8), outline=0, fill=brite)
#    draw.rectangle((126,top+12,119,18), outline=0, fill=brite)
#    draw.rectangle((126,top+30,119,34), outline=0, fill=brite)
#    draw.text((12, top+12), filepath , font=font5, fill=0)
    draw.text((12, top+12), filepath , font=font5, fill=0)
#    draw.text((5, top+10), filename , font=font2, fill=0)
#    draw.text((14, top+45), "Buttons 1 & 2 to scroll", font=font4, fill=brite)
#    draw.text((14, top+55), "LED button to load", font=font4, fill=brite)
#    disp.image(image)
    with regulator:
        disp.display(image)

#-------------------------------------------------------------------
regulator = framerate_regulator(fps=40)  # Unlimited
#path = '/home/pi/terminal_tedium/software/' #tt dir
#path = '/home/pi/terminal_tedium/software/' #tt dir
path = os.getcwd()
pathlength = len(path)
searchpath = path+'/**/TT-*.pd'
files = glob.glob(searchpath)
listsize = len(files)
if not files: # test to see if the list returns anything
    print("No files found")
print(searchpath)
#print("List element 0 is: ", files[0])
x = 0
done = 0
print("START",x, files[x])
# display first file name
filenm = files[x][files[x].find('TT-'):99]
filepath = files[x][0:files[x].find('TT-')]
subpath = files[x][pathlength:files[x].find('TT-')]
#---------- put TT title on top display ------------------------
disptop.clear()
width = disptop.width
height = disptop.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()
font1 = ImageFont.truetype(path+"/Roboto-Light.ttf",11)
font2 = ImageFont.truetype(path+"/Roboto-Bold.ttf",14)
font3 = ImageFont.truetype(path+"/Roboto-Bold.ttf",48)
draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.rectangle((0,63,127,0), outline=brite, fill=0)
draw.text((34, 4), "TT", font=font3, fill=brite)
draw.text((25, 2), "terminal tedium", font=font1, fill=brite)
draw.text((39, 50), "MXMXMX", font=font1, fill=brite)
#topdisp.image(image)
disptop.display(image)
time.sleep(2.0)
disptop.clear()
disp.clear()
filedisp(subpath,filenm)

while not done == 1:
    up = not GPIO.input(23) # these things are inverted, so I inverted them again
    down = not GPIO.input(25)
    select = not GPIO.input(24)
#        print up,down,select
#        if msvcrt.kbhit():              # Key pressed?
    if up == 1 or down == 1 or select == 1:
#            a = ord(msvcrt.getch())     # get first byte of keyscan code
#            if a == 0 or a == 224:      # is it a function key?
#                msvcrt.getch()          # discard second byte of key scan code
#                return 0                # return 0
        if up == 1:
            x += 1
            x = x % (listsize)
            print ("+ ",x,files[x])
            sleep(.2)
            up = 0
            filenm = files[x][files[x].find('TT-'):99]
            filepath = files[x][0:files[x].find('TT-')]
            subpath = files[x][pathlength:files[x].find('TT-')]
#            print subpath
            filedisp(subpath,filenm)
        elif down == 1:
            x -= 1
            x = abs(x)
            print ("- ",x,files[x])
            sleep(.2)
            down = 0
            filenm = files[x][files[x].find('TT-'):99]
            filepath = files[x][0:files[x].find('TT-')]
            subpath = files[x][pathlength:files[x].find('TT-')]
            filedisp(subpath,filenm)
        elif select == 1:
            print("selected",x, files[x])
            sleep(.2)
            select = 0
            filenm = files[x][files[x].find('TT-'):99]
            filepath = files[x][0:files[x].find('TT-')]
            subpath = files[x][pathlength:files[x].find('TT-')]
            filedisp(subpath,filenm)
            oledfilepath = filepath+'tt-OLED.py'
#            exestring = '/home/pi/pd-0.46-7/bin/pd ' + '-nogui '+ '-rt '+ files[x]+ ' 2>&1 '+ '| python '+ oledfilepath
            exestring = '/home/pi/pd-0.47-1/bin/pd -nogui -rt -midiindev 2 '+ files[x]+ ' 2>&1 | python '+ oledfilepath
            os.system(exestring)
            break
#        print filepath, filenm
#sudo rm list2.txt && echo 'rec.wav' >> list2.txt && ls >> list2.txt

#create a list of .wav files that are located in subdirectory /loops/
#exestring = "sudo rm /loops/list2.txt && echo 'rec.wav' >> /loops/list2.txt && ls /loops/ >> list2.txt"
#os.system(exestring)
#
