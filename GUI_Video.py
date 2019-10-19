import time
import tkinter as tk
import os
import shutil
import picamera
import RPi.GPIO as GPIO
from Servo_caliberation import *
from PIL import Image
from datetime import datetime


class Video:
    def __init__(
        self
    ):

        self.folder_name    = "Collection_video"
        self.reserve_space  = 1024 #MB (dont start if free space is less than this)
        self.resolution_cam = (480,360)
        self.expos_compens  = 0
        self.file_suffix    = "" # Change this to R_,G_,Y_,N_ using buttons
        self.quit_value     = False
        self.preview_image  = None
        try:
            with open("/home/pi/Desktop/device_info/device_id.txt",'r') as f:
                self.device_id = f.read()
        except:
            self.device_id = "U"
        # Servo pins
        self.base_servo_pin   = 25 # BCM pins
        self.camera_servo_pin = 17 # BCM pins

        # Setting up servo Objects
        self.base_servo   = servo_caliberate(self.base_servo_pin,"Base")
        self.camera_servo = servo_caliberate(self.camera_servo_pin,"Camera")

        # Loading last recorded servo orientation
        self.load_orientation()

        # Creating camera object
        self.camera = picamera.PiCamera()
        self.camera.vflip = True                         # Vertically Flipping the camera image
        self.camera.hflip = True

        self.set_GUI()

        self.top.mainloop()


    def set_GUI(
        self
    ):
        """Setting up GUI"""
        self.top = tk.Tk()
        self.top.title("Video collection interface")

        self.get_label(
                self.top,
                text = "Folder name",
                width = None, # in characters
                height = 1, # in lines
                font = None,
                stick = tk.W,
                row = 0,
                column = 0,
                return_lbl = False
            )

        self.e_path = self.get_entry(
                self.top,
                default_txt = self.folder_name,
                enable = True,
                width = 30,
                row = 0,
                column = 1)
        
        self.get_label(
            self.top,
            text = "",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 2,
            column = 0,
            return_lbl = False
        )

        self.get_label(
                self.top,
                text = "Resolution",
                width = None, # in characters
                height = 1, # in lines
                font = None,
                stick = tk.W,
                row = 2,
                column = 0,
                return_lbl = False
            )

        self.r_radio_button_variable = tk.IntVar(self.top,3)

        self.r_images_time = self.get_radio_button(
            self.top,
            control_variable =self.r_radio_button_variable ,
            returned_value = 0,
            text = "1080p",
            enable = True,
            default_state = True,
            #width = 30,
            row = 3,
            column = 0,
            align = tk.W,
            command = self.quality_change)#self.block_entry)

        self.r_images_interval = self.get_radio_button(
            self.top,
            control_variable =self.r_radio_button_variable ,
            returned_value = 1,
            text = "720p",
            enable = True,
            default_state = False,
            #width = 30,
            row = 4,
            column = 0,
            align = tk.W,
            command = self.quality_change)#self.block_entry)

        self.r_time_interval = self.get_radio_button(
            self.top,
            control_variable =self.r_radio_button_variable ,
            returned_value = 2,
            text = "480p",
            enable = True,
            default_state = False,
            #width = 30,
            row = 5,
            column = 0,
            align = tk.W,
            command = self.quality_change)#self.block_entry)

        self.r_time_interval = self.get_radio_button(
                self.top,
                control_variable =self.r_radio_button_variable ,
                returned_value = 3,
                text = "360p",
                enable = True,
                default_state = False,
                #width = 30,
                row = 6,
                column = 0,
                align = tk.W,
                command = self.quality_change)#self.block_entry)

        self.r_radio_button_variable.set(3)

        self.get_label(
            self.top,
            text = "",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 7,
            column = 0,
            return_lbl = False
        )

        self.get_label(
            self.top,
            text = "Day or Night",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 2,
            column = 1,
            return_lbl = False
        )

        self.r_Day_Night_variable = tk.StringVar(self.top,"Day")

        self.r_Day = self.get_radio_button(
            self.top,
            control_variable =self.r_Day_Night_variable ,
            returned_value = "Day",
            text = "Day",
            enable = True,
            default_state = True,
            #width = 30,
            row = 3,
            column = 1,
            align = tk.W,
            command = self.day_change)

        self.r_Night = self.get_radio_button(
            self.top,
            control_variable =self.r_Day_Night_variable ,
            returned_value = "Night",
            text = "Night",
            enable = True,
            default_state = False,
            #width = 30,
            row = 4,
            column = 1,
            align = tk.W,
            command = self.day_change)


        self.b_start = self.get_button(
            root = self.top,
            button_text = "Start",
            row = 2,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.start_recording#self.start_collecting
        )

        self.b_stop = self.get_button(
            root = self.top,
            button_text = "Stop",
            row = 3,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.stop_recording#self.start_collecting
        )
        self.b_red = self.get_button(
            root = self.top,
            button_text = "Red",
            row = 5,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.red#self.start_collecting
        )

        self.b_red.config(bg='red', activebackground = 'red')

        self.b_yellow = self.get_button(
            root = self.top,
            button_text = "Yellow",
            row = 6,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.yellow#self.start_collecting
        )

        self.b_yellow.config(bg='yellow', activebackground = 'yellow')

        self.b_green = self.get_button(
            root = self.top,
            button_text = "Green",
            row = 7,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.green#self.start_collecting
        )

        self.b_green.config(bg='green', activebackground = 'green')

        self.b_no_clr = self.get_button(
            root = self.top,
            button_text = "No color",
            row = 8,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.normal#self.start_collecting
        )

        self.get_label(
            self.top,
            text = "",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 9,
            column = 2,
            return_lbl = False
        )

        self.b_start = self.get_button(
            root = self.top,
            button_text = "Preview",
            row = 10,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.preview#self.start_collecting
        )

        self.b_load_orientation = self.get_button(
            root = self.top,
            button_text = "Load orientation",
            row = 11,
            column = 2,
            enable = True,
            width = 12,
            height =1,
            command = self.load_orientation#self.start_collecting
        )


        self.get_label(
            self.top,
            text = "",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 18,
            column = 0,
            return_lbl = False
        )


        self.l_image = self.get_label(
            self.top,
            text = None,
            width = None, # in characters
            height = None, # in lines
            font = None,
            stick = None,
            row = 120,
            column = 3,#0,
            return_lbl = True,
            ctr_var = None
        )

        self.get_label(
            self.top,
            text = "Progress :",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 7,
            column = 0,
            return_lbl = False
        )

        self.progress_var = tk.StringVar(self.top)
        
        self.get_label(
            self.top,
            text = "",
            width = None,#30, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 7,
            column = 1,
            return_lbl = False,
            ctr_var = self.progress_var
        )

        self.get_label(
            self.top,
            text = "",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 8,
            column = 0,
            return_lbl = False
        )

        self.get_label(
            self.top,
            text = "Free Space :",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 9,
            column = 0,
            return_lbl = False
        )

        self.free_space_var = tk.StringVar(self.top)
        
        self.get_label(
            self.top,
            text = "",
            width = None,#20, # in characters
            height = 2, # in lines
            font = None,
            stick = tk.W,
            row = 9,
            column = 1,
            return_lbl = False,
            ctr_var = self.free_space_var
        )

        


    def get_label(
        self,
        root,
        text = None,
        width = 10, # in characters
        height = 1, # in lines
        font = ('Times', '24', 'bold italic'),
        row = 0,
        column = 0,
        stick = None, #tk.W
        return_lbl = False,
        ctr_var = None
    ):
        temp_label = tk.Label(root,text = text,font = font,width = width,height = height)
        temp_label.grid(row = row,column = column,sticky = stick)
        if ctr_var != None : 
            temp_label.config(textvariable = ctr_var)
        if return_lbl:
            return temp_label

    def get_button(
        self,
        root,
        button_text = None,
        row = 0,
        column = 0,
        enable = True,
        width = 1,
        height =1,
        command = None
    ):
        temp_button = tk.Button(root,text = button_text,command = command,height = height,width = width)
        temp_button.grid(row = row,column = column)
        if enable == True:
            temp_button.config(state = tk.NORMAL)
        else:
            temp_button.config(state = tk.DISABLED)
        return temp_button


    def get_entry(
        self,
        root,
        default_txt = None,
        enable = True,
        width = 20,
        row = 0,
        column = 0
    ):
        temp_entry = tk.Entry(root)
        temp_entry.grid(row = row,column = column)
        temp_entry.insert(0, default_txt)
        if enable:
            temp_entry.config(state = tk.NORMAL)
        else:
            temp_entry.config(state = tk.DISABLED)
        return temp_entry

    def get_radio_button(
        self,
        root,
        control_variable,
        returned_value,
        text = None,
        enable = True,
        default_state = False,
        width = None,
        row = 0,
        column = 0,
        align = None,
        command = None
    ):

        temp_radio_button = tk.Radiobutton(root,text = text,width = width, variable = control_variable, value = returned_value,command = command)
        temp_radio_button.grid(row = row, column = column,sticky = align)
        if default_state:
            temp_radio_button.select()
        else: 
            temp_radio_button.deselect()
            
        if enable:
            temp_radio_button.config(state = tk.NORMAL)
        else:
            temp_radio_button.config(state = tk.DISABLED)
        return temp_radio_button

    def day_change(
        self
    ):
        """Changes the Parameters according to day or night"""
        if self.r_Day_Night_variable.get() == 'Day':
            self.expos_compens = 0
        else:
            self.expos_compens = 25
        print("Changed to {} mode : Exposure compensation = {}".format(self.r_Day_Night_variable.get(),self.expos_compens))

    def quality_change(
        self
    ):
        """Changes the Parameters according to quality"""
        qualities = [(1920,1080),(1280,720),(858,480),(480,360)]
        self.resolution_cam = qualities[self.r_radio_button_variable.get()]
        print("Changed quality to {}".format(qualities[self.r_radio_button_variable.get()]))

    def red(
        self
    ):
        self.file_suffix = "_R"
        print("Red light suffix placed")
        self.start_recording()
    
    def yellow(
        self
    ):
        self.file_suffix = "_Y"
        print("Yellow light suffix placed")
        self.start_recording()
    
    def green(
        self
    ):
        self.file_suffix = "_G"
        print("Green light suffix placed")
        self.start_recording()
    
    def normal(
        self
    ):
        self.file_suffix = ""
        print("No light suffix placed")
        self.start_recording()

    def start_recording(
        self
    ):
        """Starts recording. If currently recording"""
        if self.get_disk_space():
            self.stop_recording()
            return None
        try:
            self.camera._check_recording_stopped()
            print("\nStarting to record....\n")
            self.folder_name = self.e_path.get()
            self.camera.resolution = self.resolution_cam
            self.camera.exposure_compensation = self.expos_compens
            self.update_label(                          # Updating progress bar
                    self.top,
                    label_var =self.progress_var,
                    text = "Capturing video....",
                    delay = 2
                )
        except:
            self.camera.stop_recording()
            print("\nStopped ongoing recording.\nStarting a new recording.\n")
        # if(~(os.path.isdir(self.folder_name))):
        try:
            os.mkdir(self.folder_name)
        except:
            print("Folder exists")
        # self.camera.annotate_text_size = 17
        # self.camera.annotate_background = picamera.Color('black')
        # self.camera.annotate_text = datetime.now().strftime('%d %m %Y %H:%M:%S')
        self.camera.start_recording(self.folder_name+"/"+datetime.now().strftime("%Y:%m:%d_%H:%M:%S_")+"D"+self.device_id+self.file_suffix+".h264")
        # print(self.folder_name+"/"+self.file_suffix+"D"+self.device_id+datetime.now().strftime("_%Y:%m:%d_%H:%M:%S")+".h264")

    def preview(
        self
    ):
        """Starts recording. If currently recording"""
        self.camera.resolution = (480,360)
        self.camera.exposure_compensation = self.expos_compens
        self.camera.capture("preview.png")
        self.image = tk.PhotoImage(file = "preview.png")
        self.image = self.image.subsample(2,2)
        self.l_image.config(image=self.image)
        self.top.update()
        time.sleep(2)
        
    def stop_recording(
        self
    ):
        """Stops the recording process"""
        try:
            self.camera._check_recording_stopped()
            print("\nNo ongoing recording to stop.\n")
        except:
            self.camera.stop_recording()
            print("\nStopped ongoing recording.\n")

        self.update_label(                          # Updating progress bar
                    self.top,
                    label_var =self.progress_var,
                    text = "Stopped capturing",
                    delay = 2
                )

    def update_label(
        self,
        root,
        label_var,
        text = "",
        delay = 2 #seconds
    ):
        """Updates the text on the label with the given text"""
        label_var.set(text)
        root.update()
        time.sleep(delay)

    def get_disk_space(
        self
    ):
        space = shutil.disk_usage(os.getcwd())
        free_space = (space.free)/(1024**2) #in MB
        self.update_label(
                self.top,
                self.free_space_var,
                text = "{} MB.\n".format(round(free_space,2)),
                delay = 2 #seconds
        )
        if(free_space < self.reserve_space):
            print("Free space remaining is {} MB.".format(free_space))
            self.update_label(
                self.top,
                self.progress_var,
                text = "Space not enough. Free space : {} MB.\n".format(round(free_space,2)),
                delay = 2 #seconds
            )
            return True # No hard disk space
        else:
            return False

    

    def load_orientation(
        self
    ):
        
        if(os.path.isfile("parameters/servo_orientation.txt")):
            with open("parameters/servo_orientation.txt",'r') as foo:
                base_val = int(foo.readline().split()[1])
                camera_val = int(foo.readline().split()[1])
                self.base_servo.turn_servo_degrees(base_val,delay_pwm0 = 0.7)
                self.base_servo.turn_servo_degrees(base_val)
                self.camera_servo.turn_servo_degrees(camera_val,delay_pwm0 = 0.7)
                self.camera_servo.turn_servo_degrees(camera_val)
                print("\nLoaded orientation as:\nBase %i degrees\nCamera %i degrees"%(base_val,camera_val))
        else:
            print("\nFound no previous orientation.")

try:
    GUI = Video()
except KeyboardInterrupt:
    GUI.base_servo.pwm.stop()
    GUI.camera_servo.pwm.stop()
    GPIO.cleanup()
    GUI.camera.close()
    print("GPIO cleanup done : KeyBoardInterrupt")
finally:
    GUI.base_servo.pwm.stop()
    GUI.camera_servo.pwm.stop()
    GPIO.cleanup()
    GUI.camera.close()
    print("GPIO cleanup done")