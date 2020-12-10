import RPi.GPIO as GPIO
import time
from time import sleep
##############
# Author: Chong
# Driver for my 3-axis platform
##############

class StepMotorAdapterTask():
    lastPoint = (0,0);
    thisPoint = (0,0);
    
    def __init__(self):
        #33: pwm
        #16: first step motor direction: High to motor & Low to end
        #18: second step motor direction: High to motor & Low to end
        #22: third step motor direction: High to motor & Low to end
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(33,GPIO.OUT)
        GPIO.setup(16,GPIO.OUT)
        GPIO.setup(18,GPIO.OUT)
        GPIO.setup(22,GPIO.OUT)
        #11: first step motor enable: High to disable & Low to enable
        #13: second step motor enable: High to disable & Low to enable
        #15: third step motor enable: High to disable & Low to enable
        GPIO.setup(11,GPIO.OUT)
        GPIO.setup(13,GPIO.OUT)
        GPIO.setup(15,GPIO.OUT)
        # disable all motor at begining
        GPIO.output(11,GPIO.HIGH)
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(15,GPIO.HIGH)
    
    #########################
    # Functioon moveTo(): Move on x and y simutaneously.
    #
    # param x: move x pixels in x axis
    # param y: move y pixels in y axis
    # param isDrawing: True/Fasle, set pen to up/down position
    ###############################################
    def moveTo(self, x:int , y:int, isDrawing:bool):
        self.thisPoint = (x,y)
        mx = self.thisPoint[0]-self.lastPoint[0]
        my = self.thisPoint[1]-self.lastPoint[1]
        print(mx,":",my)
        #self.moveZ(isDrawing)
        #move x
        GPIO.output(11,GPIO.LOW)
        GPIO.output(13,GPIO.LOW)
        if mx >=0 :
            GPIO.output(16,GPIO.LOW)
        else:
            mx=-mx
            GPIO.output(16,GPIO.HIGH)
        #move y
        if my >=0 :
            GPIO.output(18,GPIO.LOW)
        else:
            my=-my
            GPIO.output(18,GPIO.HIGH)
        #start
        if mx>my:
            step = mx
        else:
            step = my
        for i in range(0,step*5):
            GPIO.output(33,GPIO.LOW)
            time.sleep(0.0005)
            GPIO.output(33,GPIO.HIGH)
            time.sleep(0.0005)

            if mx>my and i>=(my*10):
                GPIO.output(13,GPIO.HIGH)
            if mx<my and i>=(mx*10):
                GPIO.output(11,GPIO.HIGH)
            
        GPIO.output(11,GPIO.HIGH)
        GPIO.output(13,GPIO.HIGH)
        #save this point
        self.lastPoint = self.thisPoint
    
    #########################
    # Functioon moveZ: Move on z axis
    #
    # param isDrawing: True/Fasle, set pen to up/down position
    ###############################################
    def moveZ(self,isDrawing:bool): #true up
        GPIO.output(15,GPIO.LOW)
        if isDrawing :
            GPIO.output(22,GPIO.HIGH)
            self.generatePWM(500)
        else:
            GPIO.output(22,GPIO.LOW)
            self.generatePWM(500)
        GPIO.output(15,GPIO.HIGH)
        
    #########################
    # Functioon generatePWM(): Generate PWM wave for step motor.
    #
    # param step: cycles of PWM wave
    # 1 pixel = 10 step (0.25mm)    
    # total 320*320, 1 step 0.2(0.01*2*10)
    #####################################################
    def generatePWM(self, step:int):
        for i in range(0,step*2):
            GPIO.output(33,GPIO.LOW)
            time.sleep(0.0005)
            GPIO.output(33,GPIO.HIGH)
            time.sleep(0.0005)

    def test(self):
        #self.moveTo(-100,0,True)
        self.moveZ(True)
        #sleep(50)
        #GPIO.cleanup()

if __name__ == "__main__":
    task = StepMotorAdapterTask()
    task.test()
