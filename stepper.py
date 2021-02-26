#Copyright KeonWoo PARK 2020, All right reserved.
#2020-11-12 Stepper morter control Library for Raspberry pi.
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

class stepper:
    def __init__(self,step,dir,speed):
        self.step_port=int(step)
        self.dir_port=int(dir)
        self.speed=int(speed)
        GPIO.setup(self.step_port,GPIO.output)
        GPIO.setup(self.dir_port,GPIO.output)
        GPIO.output(self.step_port,False)
        GPIO.output(self.dir_port,False)
    
    def setspeed(self,speed):
        self.speed=speed
    
    def forward(self,round):
        GPIO.output(self.dir_port,False)
        for i in range(200*round):
            GPIO.output(self.step_port,True)
            time.sleep(self.speed/1000000)
            GPIO.output(self.step_port,False)
            time.sleep(self.speed/1000000)
    
    def backward(self,round):
        GPIO.output(self.dir_port,True)
        for i in range(200*round):
            GPIO.output(self.step_port,True)
            time.sleep(self.speed/1000000)
            GPIO.output(self.step_port,False)
            time.sleep(self.speed/1000000)
    