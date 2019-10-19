import RPi.GPIO as GPIO
import time
import os



class servo_caliberate:
    def __init__(
        self,   
        servo_pin,              #pwm pin assigned for the servo (use BCM numbering)
        servo_name = "Servo_name"   #name given to the servo (string)
        ): 

        self.servo_name = servo_name
        self.servo_param_path = os.getcwd() + "/parameters/" + servo_name + "_param.txt"

        self.servo_pin = servo_pin
        self.pwm = None
        self.setup_servo() #This will setup the GPIO

        if os.path.isfile(self.servo_param_path): #Trying to load the servo angle-pwm mapping parameters
            with open(self.servo_param_path,'r') as foo:
                self.gradient = float(foo.readline().split()[1])
                self.intersection = float(foo.readline().split()[1])
                print("Previous Servo Parameters Loaded !!\n%s will use the mapping equation : y = %.3fx + %.2f\n"%(self.servo_name,self.gradient,self.intersection))
        else:
            #mappin parameters - to map the angle given to the pwm value
            self.gradient = 0
            self.intersection = 0
            print("No servo parameters were found. Please caliberate")

        
    def setup_servo(self):
        #Set the pin numbers according to the BCM pin mapping
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin,GPIO.OUT)
        self.pwm = GPIO.PWM(self.servo_pin,50)  #frequency 50Hz
        self.pwm.start(0)   

    def gpio_cleanup(self): #Use this when you define only 1 servo
        self.pwm.stop()
        GPIO.cleanup()
        print("Exiting. Cleaning up GPIO.")

    def turn_servo(
        self,
        duty_cycle, #for caliberation purposes only. Give duty cycle ~2 - ~11
        delay_pwm0 = 0.1 # the delay before the pwm signal is removed
        ):
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(delay_pwm0)
        self.pwm.ChangeDutyCycle(0)
        time.sleep(0.05)

    def generate_mapping_para(self,position_0,position_180): #creating the parameter values and storing them in a file
        self.gradient = (position_180-position_0)/180.0
        self.intersection = position_0
        with open(self.servo_param_path,'w') as foo:
            foo.write("gradient %s\n"%(self.gradient))
            foo.write("intersection %s"%(self.intersection))
        print("Mapping Equation for %s : y = %.3fx + %.2f"%(self.servo_name,self.gradient,self.intersection))

    def servo_centralize(self):
        self.turn_servo_degrees(90) #centralize the servos
        print("Centralized servo (%s)"%(self.servo_name))

    def turn_servo_degrees(
        self,
        angle, #0-180 degrees
        delay_pwm0 = 0.1 #delay before pwm signal goes 0
        ): 

        pwm_value = self.gradient*angle + self.intersection
        self.turn_servo(pwm_value,delay_pwm0)

    
