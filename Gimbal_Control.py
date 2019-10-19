import time
import RPi.GPIO as GPIO
import tkinter as tk
from Servo_caliberation import *

base_servo_pin = 25 #BCM Pins
camera_servo_pin = 17 #BCM Pins

base_servo = servo_caliberate(base_servo_pin,"Base")
camera_servo = servo_caliberate(camera_servo_pin,"Camera")

def base_control(dummy):
    pwm_value = base_slider.get()
    base_servo.turn_servo_degrees(pwm_value)

def camera_control(dummy):
    pwm_value = camera_slider.get()
    camera_servo.turn_servo_degrees(pwm_value)

def store_orientation():
    with open("parameters/servo_orientation.txt",'w') as foo:
        base_val = base_slider.get()
        camera_val = camera_slider.get()
        foo.write("Base %i\n"%(base_val))
        foo.write("camera %i"%(camera_val))
        print("\nStored new orientation as:\nBase %i degrees\nCamera %i degrees"%(base_val,camera_val))

def load_orientation():
    if(os.path.isfile("parameters/servo_orientation.txt")):
        with open("parameters/servo_orientation.txt",'r') as foo:
            base_val = int(foo.readline().split()[1])
            camera_val = int(foo.readline().split()[1])
            base_servo.turn_servo_degrees(base_val,delay_pwm0 = 0.7)
            camera_servo.turn_servo_degrees(camera_val,delay_pwm0 = 0.7)
            base_slider.set(base_val)
            camera_slider.set(camera_val)
            print("\nLoaded orientation as:\nBase %i degrees\nCamera %i degrees"%(base_val,camera_val))
    else:
        print("\nFound no previous orientation.")

    


try:
    top = tk.Tk()
    top.title("Servo Control")
    w = tk.Label(top,text = "Slide to control the Servos",font = ("Times","20","bold underline"))
    w.pack(side = "top")

    base_slider = tk.Scale(top,from_ = 0, to =180, label ="Base Control",command = base_control,length = 300,width = 30,sliderlength = 60,font = ("Times","15"))
    base_slider.pack(side ="left")
    camera_slider = tk.Scale(top,from_ = 0, to =180, label ="Camera Control",command = camera_control,length = 300,width = 30,sliderlength = 60,font = ("Times","15"))
    camera_slider.pack(side ="left")

    load_orientation_button = tk.Button(top,text = "Load Orientation",command = load_orientation,font =("Times","15"))
    load_orientation_button.pack(side = "bottom")

    empty_label = tk.Label(top,text = "")
    empty_label.pack(side = "bottom")

    store_orientation_button = tk.Button(top,text = "Store Orientation",command = store_orientation,font =("Times","15"))
    store_orientation_button.pack(side = "bottom")
    
    #Setting the servos to a general orientation
    base_servo.turn_servo_degrees(90,delay_pwm0 = 0.7)
    camera_servo.turn_servo_degrees(55,delay_pwm0 = 0.7)
    base_slider.set(90)
    camera_slider.set(55) 

    #listening to events
    top.mainloop()
    
    print("\nEnding Gimbal Control. Cleaning up GPIO")
    camera_servo.pwm.stop()
    base_servo.pwm.stop()
    GPIO.cleanup()
    
except KeyboardInterrupt:
    print("\nInterupted by user :GPIO cleanup initiated")
    camera_servo.pwm.stop()
    base_servo.pwm.stop()
    GPIO.cleanup()

except:
    print("\nUnknown error.Cleaning up GPIO")
    camera_servo.pwm.stop()
    base_servo.pwm.stop()
    GPIO.cleanup()

