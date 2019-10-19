import tkinter as tk
from Servo_caliberation import *


class servo_caliberation:
    def __init__(self):

        self.servo_name = "Test"
        self.servo_pin = 25
        self.angle = 0
        self.pwm_value = 0 
        self.delay_pwm = 0.1

        self.begin_caliberation()

    def begin_caliberation(self):

        self.root = tk.Tk()
        self.root.title("Servo Caliberation")

        #Servo name 
        tk.Label(self.root,text="Servo Name : ").grid(row = 0)
        self.e_servo_name = tk.Entry(self.root)
        self.e_servo_name.grid(row = 0, column = 1)
        self.e_servo_name.insert(0,"Test")
        self.l_servo_name = tk.Label(self.root,text="")
        self.l_servo_name.grid(row = 0,column = 2)

        #servo pin
        tk.Label(self.root,text="Servo Pin Number: ").grid(row = 1)
        self.e_servo_pin = tk.Entry(self.root)
        self.e_servo_pin.grid(row = 1, column = 1)
        self.e_servo_pin.insert(0,"25")
        #self.e_servo_pin.bind("<Return>",self.set_servo_pin)
        self.l_servo_pin = tk.Label(self.root,text="")
        self.l_servo_pin.grid(row = 1,column = 2)

        #start button to initiate the servo object
        self.start_button = tk.Button(self.root,text = "Start",command = self.create_servo_obj)
        self.start_button.grid(row = 2 ,column = 0 , columnspan = 2)
        self.l_start_button = tk.Label(self.root,text ='')
        self.l_start_button.grid(row = 2, column = 2)
  

        tk.Label(self.root,text="").grid(row = 3)

        #Set delay before the PWM 0 signal
        tk.Label(self.root,text="Delay before 0 PWM :").grid(row = 4)
        self.e_delay_pwm = tk.Entry(self.root,state = tk.DISABLED)
        self.e_delay_pwm.grid(row = 4, column = 1)
        self.l_delay_pwm = tk.Label(self.root,text="")
        self.l_delay_pwm.grid(row = 4,column = 2,rowspan = 2)

        #Duty Cycle of the PWM signal
        tk.Label(self.root,text="Duty Cycle of PWM :").grid(row = 5)
        self.e_pwm_value = tk.Entry(self.root,state = tk.DISABLED)
        self.e_pwm_value.grid(row = 5, column = 1)
        self.e_pwm_value.bind("<Return>",self.set_pwm_value)
        self.l_start_button = tk.Label(self.root,text ='')

        #set the Duty Cycle and the delay PWM 0 signal button
        self.set_pwm_button = tk.Button(self.root,text = "Set PWM",command = self.set_pwm_value,state = tk.DISABLED)
        self.set_pwm_button.grid(row = 6 ,column = 0 , columnspan = 2)

        tk.Label(self.root,text="").grid(row = 7)

        #0 position
        tk.Label(self.root,text="0\u00b0 position Duty Cycle : ").grid(row = 8)
        self.e_0_position = tk.Entry(self.root,state =tk.DISABLED)
        self.e_0_position.grid(row = 8, column = 1)
        self.l_0_position = tk.Label(self.root,text="")
        self.l_0_position.grid(row = 8,column = 2,rowspan =3)

        #180 position
        tk.Label(self.root,text="180\u00b0 position Duty Cycle : ").grid(row = 9)
        self.e_180_position = tk.Entry(self.root,state =tk.DISABLED)
        self.e_180_position.grid(row = 9, column = 1)

        #set servo parameters
        self.b_set_params_button = tk.Button(self.root,text = "Set Servo Parameters",command = self.set_servo_params,state =tk.DISABLED)
        self.b_set_params_button.grid(row = 10 ,column = 0 , columnspan = 2)
  

        tk.Label(self.root,text="").grid(row = 11)

        #Angle entry box
        tk.Label(self.root,text="Angle between 0\u00b0-180\u00b0 : ").grid(row = 12)
        self.e_angle = tk.Entry(self.root,state =tk.DISABLED)
        self.e_angle.grid(row = 12, column = 1)

        #set angle button
        self.b_set_angle_button = tk.Button(self.root,text = "Set Servo Angle",command = self.set_angle,state =tk.DISABLED)
        self.b_set_angle_button.grid(row = 13 ,column = 0 , columnspan = 2)
        self.l_set_angle = tk.Label(self.root,text="")
        self.l_set_angle.grid(row = 12,column = 2,rowspan =2)

        tk.Label(self.root,text="").grid(row = 14)

        #until cancelled this will be in a infite loop
        self.root.mainloop()

        #after cancelling,GPIO cleanup
        self.servo.gpio_cleanup()


    def create_servo_obj(self):
        
        self.servo_name = self.e_servo_name.get()
        self.l_servo_name.config(text = "\u2713")
    
        self.servo_pin = int(self.e_servo_pin.get())
        self.l_servo_pin.config(text = "\u2713")
        
        self.servo = servo_caliberate(self.servo_pin,self.servo_name) #uncomment----------------------------------
        print("\nServo object created")
        self.l_start_button.config(text = "Servo Object Created")
        self.e_servo_name.config(state =tk.DISABLED)
        self.e_servo_pin.config(state =tk.DISABLED)
        self.e_delay_pwm.config(state = tk.NORMAL)
        self.e_pwm_value.config(state = tk.NORMAL)
        self.set_pwm_button.config(state = tk.NORMAL)
        self.e_0_position.config(state = tk.NORMAL)
        self.e_180_position.config(state = tk.NORMAL)
        self.b_set_params_button.config(state = tk.NORMAL)
        self.e_angle.config(state = tk.NORMAL)
        self.e_delay_pwm.insert(0,"0.5")
        self.e_pwm_value.insert(0,"5.0")
        self.e_0_position.insert(0,"4")
        self.e_180_position.insert(0,"8")
        self.e_angle.insert(0,90)

    def set_pwm_value(self,event=None):
        print("Wrote pwm values")
        self.delay_pwm = float(self.e_delay_pwm.get())
        self.pwm_value = float(self.e_pwm_value.get())
        self.l_delay_pwm.config(text = "Current Duty cycle :\n%.2f"%(self.pwm_value))
        self.e_pwm_value.delete(0,'end')
        self.servo.turn_servo(self.pwm_value,self.delay_pwm) #uncomment -----------------------------------------

    def set_servo_params(self):
        print("Saving Servo Parameters")
        self._0_position = float(self.e_0_position.get())
        self._180_position = float(self.e_180_position.get())
        self.servo.generate_mapping_para(self._0_position,self._180_position) #uncomment -------------
        self.l_0_position.config(text = "The Mapping Function:\n y = %.2fx + %.2f"%(self.servo.gradient,self.servo.intersection))# -----uncomment
        self.b_set_angle_button.config(state = tk.NORMAL)

    def set_angle(self):
        print("Setting the Angle of the servo")
        temp = float(self.e_angle.get())
        if temp>180:
            self.angle = 180.0
        elif temp<0:
            self.angle = 0.0
        else:
            self.angle = temp
        self.delay_pwm = float(self.e_delay_pwm.get())        
        self.servo.turn_servo_degrees(self.angle,self.delay_pwm)# -------------------------uncomment
        self.l_set_angle.config(text = "The Angle set to : %.2f"%(self.angle))

GUI = servo_caliberation()






