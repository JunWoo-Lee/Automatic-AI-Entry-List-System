from huskylib import HuskyLensLibrary #Huskylens lib
import json
import time
import serial #Pyserial lib for connect to Arduino
from stepper import stepper
from pyfingerprint.pyfingerprint import PyFingerprint
import wave
import pyaudio
import GPIO.RPi as GPIO
import pygame
human=["박건우","손태일","정하은","이준우"]

Husky = HuskyLensLibrary('SERIAL', '/dev/ttyUSB0', 3000000) #Connect to huskylens through USB Serial
f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000) #Connect to Fingerprint sensor
Arduino=serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.5) #Connect to Arduino
Arduino.flush()
Arduino.flushInput()
Arduino.flushOutput()
step1 = stepper(9,10,700)
loc = '/home/pi/Desktop/HUSKYLENS/Voice/'
GPIO.setup(11,GPIO.output) ##마스크
GPIO.setup(12,GPIO.output)
GPIO.setup(13,GPIO.output)
GPIO.setup(14,GPIO.output)

GPIO.output(11,False)
GPIO.output(12,False)
GPIO.output(13,False)
GPIO.output(14,False)

def read():
    if Arduino.readable():
        res = Arduino.readline()
        ress=res.decode()[:len(res)-2]
        return ress
    else:
        return False
def send(a):
    Arduino.write(a.encode('utf-8'))

def check(what):
    if what=="isfront": #Check user.
        send("i")
        time.sleep(0.5)
        for i in range(3):
            g = read()
            if g == False:
                time.sleep(1)
                continue
            else:
                return g
        print("Timeout occurred While get ",what)
        exit()
    elif what=='temp':
        send('t')
        time.sleep(0.5)
        for i in range(3):
            g = read()
            if g == False:
                time.sleep(1)
                continue
            else:
                return g
        print("Timeout occurred While get ",what)
        exit()
    elif what=='mask':
        t = [0,0,0,0]
        for i in range(5):
            v = Husky.requestAll()
            time.sleep(0.75)
            t[v[0].ID] = t[v[0].ID] + 1
        t[2] = t[2]+t[3]
        if t[0]<t[1]:
            if t[1]<t[2]:
                return 2
            else:
                return 1
        else:
            if t[0]<t[2]:
                return 2
            else:
                return 0

def red():
    GPIO.output(12,True)
    GPIO.output(13,False)
    GPIO.output(14,False)

def green():
    GPIO.output(12,False)
    GPIO.output(13,True)
    GPIO.output(14,False)

def blue():
    GPIO.output(12,False)
    GPIO.output(13,False)
    GPIO.output(14,True)

def off():
    GPIO.output(12,False)
    GPIO.output(13,False)
    GPIO.output(14,False)


def play(file):
    pygame.mixer.init()
    pygame.mixer.music.load(loc+file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def red_blink():
    red()
    time.sleep(0.3)
    off()
    time.sleep(0.3)
    red()
    time.sleep(0.3)
    off()
    time.sleep(0.3)
    red()
    time.sleep(0.3)

def green_blink():
    green()
    time.sleep(0.3)
    off()
    time.sleep(0.3)
    green()
    time.sleep(0.3)
    off()
    time.sleep(0.3)
    green()
    time.sleep(0.3)

def blue_blink():
    blue()
    time.sleep(0.3)
    off()
    time.sleep(0.3)
    blue()
    time.sleep(0.3)
    off()
    time.sleep(0.3)
    blue()
    time.sleep(0.3)

def givemask():
    GPIO.output(11,True)
    time.sleep(0.5)
    GPIO.output(11,False)
    return

def open_door():
    step1.forward(16.5)
    return
def close_door():
    step1.backward(16.5)
    return
def __main__():
    while True:
        time.sleep(1)
        blue()
        print("사람 있는지 확인")
        result = check("isfront")
        if result!="yes":
            print("사람없음")
            continue
        print("사람 있음")
        play('안녕하세요.wav')
        play('설명.wav')
        play('지문안내.wav')
        print("지문 인식 시작")
        q=False
        j=0
        k=0
        for i in range(3):
            while ( f.readImage() == False ):
                pass
            ## Converts read image to characteristics and stores it in charbuffer 1
            f.convertImage(0x01)
            result = f.searchTemplate()[0]
            if result == -1 and i!=2:
                play('지문등록안됨.wav')
            if result==-1 and i == 2:
                print('No match fingerprint found 3times!')
                play('지문등록안됨.wav')
                play('처음.wav')
                continue
            else:
                play('안녕하세요.wav')
                play(str(human[result])+".wav")
                print('found finger number: #'+str(result))
                j=int(result)
                q=True
                break
        if q==False:
            continue

        time.sleep(1)
        play('체온을_측정중이오니_잠시만_기달려주세요.wav')
        print("체온 측정 시작")
        result = check('temp')
        if float(result) > 37.5:
            print("체온높음")
            red()
            play('체온높음.wav')
            print("처음으로")
            play('처음.wav')
            continue
        print("체온정상")
        play('체온완료.wav')
        print("마스크 착용 확인")
        play('카메라.wav')
        q=0
        v=0
        while True:
            v=v+1
            q=check('mask')
            if q == 0:
                red_blink()
                play('인식X.wav')
            if q == 0 and v==2:
                red_blink()
                play('3회X_처음으로.wav')
                break
            if q==1:
                red_blink()
                play('마스크X_지급.wav')
                givemask()
            if q==1 and v==1:
                red_blink()
                play('마스크X.wav')
            if q==1 and v==2:
                red_blink()
                play('3회X_처음으로.wav')
                break
            if q==2:
                green_blink()
                break
        if q==1 and v==2:
            continue
        if q==0 and v==2:
            continue
        play('마스크O.wav')
        open_door()
        #문 여는 코드
        play('마지막.wav')
        time.sleep(10)
        red()
        close_door()


__main__()
