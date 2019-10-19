import time
import tkinter as tk
import threading
import os
import shutil
import picamera
import RPi.GPIO as GPIO #uncomment in the start_collection script too 821,25,26,567
from Servo_caliberation import *
from PIL import Image#, ImageTk
from datetime import datetime

class Data_Collect_GUI:
    def __init__(
        self
    ):
        self.folder_name = "Collection"
        self.num_images = 1800
        self.total_time = 1800 #seconds
        self.interval = 1 #second
        self.progress_display_frequency = 5 # the progress bar will update per this many images
        self.images_per_folder = 500 # maximum capacity of a sub folder. A new folder will be created after this
        self.resolution_cam = (720,480)
        self.expos_compens = 0
        self.file_suffix = "" # Change this to _R , _Y, _G using the buttons
        self.quit_value = False # set true to stop the collection through a button
        self.preview_image = None

        # Servo pins
        self.base_servo_pin = 25 #BCM Pins
        self.camera_servo_pin = 17 #BCM Pins

        # Setting up Servo Objects
        self.base_servo = servo_caliberate(self.base_servo_pin,"Base")
        self.camera_servo = servo_caliberate(self.camera_servo_pin,"Camera")

        # Loading the last recorded servo orientation
        self.load_orientation()

        self.set_GUI()


        self.top.mainloop()






    def set_GUI(
        self
    ):
        """Setting up the GUI"""
        self.top = tk.Tk()
        self.top.title("Data Collection Interface")
        
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
            default_txt = "Collected_data",
            enable = True,
            width = 30,
            row = 0,
            column = 1)

        self.get_label(
            self.top,
            text = "Number of Images",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 1,
            column = 0,
            return_lbl = False
        )

        self.e_num_images = self.get_entry(
            self.top,
            default_txt = "1800",
            enable = True,
            width = 30,
            row = 1,
            column = 1)

        self.get_label(
            self.top,
            text = "Total Time",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 2,
            column = 0,
            return_lbl = False
        )

        self.e_tot_time = self.get_entry(
            self.top,
            default_txt = "15",
            enable = True,
            width = 30,
            row = 2,
            column = 1)

        self.get_label(
            self.top,
            text = "Minutes",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 2,
            column = 2,
            return_lbl = False
        )

        self.get_label(
            self.top,
            text = "Time between photos",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 3,
            column = 0,
            return_lbl = False
        )

        self.e_interval = self.get_entry(
            self.top,
            default_txt = "0.001",
            enable = False,
            width = 30,
            row = 3,
            column = 1)

        self.get_label(
            self.top,
            text = "Seconds",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 3,
            column = 2,
            return_lbl = False
        )

        self.get_label(
            self.top,
            text = "Images Per Folder",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 4,
            column = 0,
            return_lbl = False
        )

        self.e_images_per_folder = self.get_entry(
            self.top,
            default_txt = "500",
            enable = True,
            width = 30,
            row = 4,
            column = 1)

        self.get_label(
            self.top,
            text = "Progress Display Frequency",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 5,
            column = 0,
            return_lbl = False
        )

        self.e_prog_display_freq = self.get_entry(
            self.top,
            default_txt = "5",
            enable = True,
            width = 30,
            row = 5,
            column = 1)

        self.get_label(
            self.top,
            text = "Preview Display Frequency",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 6,
            column = 0,
            return_lbl = False
        )

        self.e_prew_display_freq = self.get_entry(
            self.top,
            default_txt = "10",
            enable = True,
            width = 30,
            row = 6,
            column = 1)

        self.get_label(
            self.top,
            text = "",
            width = None, # in characters
            height = 2, # in lines
            font = None,
            stick = tk.W,
            row = 7,
            column = 2,
            return_lbl = False
        )
        """
        self.get_label(
            self.top,
            text = "",
            width = None, # in characters
            height = 2, # in lines
            font = None,
            stick = tk.W,
            row = 8,
            column = 2,
            return_lbl = False
        )"""

        self.r_radio_button_variable = tk.IntVar(self.top,1)

        self.r_images_time = self.get_radio_button(
            self.top,
            control_variable =self.r_radio_button_variable ,
            returned_value = 1,
            text = "Images + Total time",
            enable = True,
            default_state = True,
            #width = 30,
            row = 9,
            column = 0,
            align = tk.W,
            command = self.block_entry)

        self.r_images_interval = self.get_radio_button(
            self.top,
            control_variable =self.r_radio_button_variable ,
            returned_value = 2,
            text = "Images + Time interval",
            enable = True,
            default_state = False,
            #width = 30,
            row = 10,
            column = 0,
            align = tk.W,
            command = self.block_entry)

        self.r_time_interval = self.get_radio_button(
            self.top,
            control_variable =self.r_radio_button_variable ,
            returned_value = 3,
            text = "Total time + Time interval",
            enable = True,
            default_state = False,
            #width = 30,
            row = 11,
            column = 0,
            align = tk.W,
            command = self.block_entry)

        self.get_label(
            self.top,
            text = "",
            width = None, # in characters
            height = 2, # in lines
            font = None,
            stick = tk.W,
            row = 12,
            column = 0,
            return_lbl = False
        )

        self.get_label(
            self.top,
            text = "",
            width = None, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 14,
            column = 0,
            return_lbl = False
        )

        self.r_quality_variable = tk.StringVar(self.top,"Low")

        self.r_HQuality = self.get_radio_button(
            self.top,
            control_variable =self.r_quality_variable ,
            returned_value = "High",
            text = "High Quality",
            enable = True,
            default_state = False,
            #width = 30,
            row = 16,
            column = 0,
            align = tk.W,
            command = self.quality_change)

        self.r_LQuality = self.get_radio_button(
            self.top,
            control_variable =self.r_quality_variable ,
            returned_value = "Low",
            text = "Low Quality",
            enable = True,
            default_state = True,
            #width = 30,
            row = 15,
            column = 0,
            align = tk.W,
            command = self.quality_change)

        self.r_Day_Night_variable = tk.StringVar(self.top,"Day")

        self.r_Day = self.get_radio_button(
            self.top,
            control_variable =self.r_Day_Night_variable ,
            returned_value = "Day",
            text = "Day",
            enable = True,
            default_state = True,
            #width = 30,
            row = 15,
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
            row = 16,
            column = 1,
            align = tk.W,
            command = self.day_change)

        self.c_auto_zip_variable = tk.IntVar(self.top,0)

        self.c_auto_zip = tk.Checkbutton(
                                            self.top,
                                            text = "Auto Zip",
                                            variable = self.c_auto_zip_variable)
        self.c_auto_zip.grid(row = 17,column = 0, sticky = tk.W)
        self.c_auto_zip.deselect()

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
            row = 114,
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
            row = 113,
            column = 0,
            return_lbl = False
        )

        self.progress_var = tk.StringVar(self.top)
        
        self.get_label(
            self.top,
            text = "",
            width = 40, # in characters
            height = 2, # in lines
            font = None,
            stick = tk.W,
            row = 113,
            column = 1,
            return_lbl = False,
            ctr_var = self.progress_var
        )
        """
        self.lab = self.get_label(
            self.top,
            text = "",
            width = 40, # in characters
            height = 1, # in lines
            font = None,
            stick = tk.W,
            row = 10,
            column = 1,
            return_lbl = True,
            #ctr_var = self.progress_var
        )"""

        self.b_start = self.get_button(
            root = self.top,
            button_text = "Start",
            row = 5,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.start_collecting
        )

        self.b_pause = self.get_button(
            root = self.top,
            button_text = "Zip Folder",
            row = 6,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.zip_folder
        )

        self.b_stop = self.get_button(
            root = self.top,
            button_text = "Stop",
            row = 7,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.stop_collecting
        )

        self.b_red = self.get_button(
            root = self.top,
            button_text = "Red",
            row = 10,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.red
        )
        self.b_red.config(bg='red',activebackground = 'red')

        self.b_yellow = self.get_button(
            root = self.top,
            button_text = "Yellow",
            row = 11,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.yellow
        )
        self.b_yellow.config(bg='yellow', activebackground = 'yellow')

        self.b_green = self.get_button(
            root = self.top,
            button_text = "Green",
            row = 12,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.green
        )
        self.b_green.config(bg='green', activebackground = 'green')

        self.b_normal = self.get_button(
            root = self.top,
            button_text = "No light",
            row = 13,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.normal
        )

        self.b_load_orientation = self.get_button(
            root = self.top,
            button_text = "Load Orientation",
            row = 15,
            column = 2,
            enable = True,
            width = 10,
            height =1,
            command = self.load_orientation
        )

        

        """
        self.get_label(
            self.top,
            text = "tesing",
            width = 10, # in characters
            height = 2, # in lines
            font = ('Times', '12', 'normal'),
            row = 0,
            column = 0,
            return_lbl = False
        )
        
        self.button1 = self.get_button(
            root = self.top,
            button_text = "test",
            row = 1,
            column = 3,
            enable = True,
            width = 10,
            height =1,
            command = self.pt
        )

        self.entry = self.get_entry(
            self.top,
            default_txt = "Test",
            enable = True,
            width = 30,
            row = 3,
            column = 0)

        self.contrl = tk.IntVar(self.top)
        self.radio = self.get_radio_button(
            self.top,
            control_variable =self.contrl ,
            returned_value = 5,
            text = "radio",
            enable = True,
            default_state = False,
            #width = 30,
            row = 0,
            column = 0,
            align = tk.W,
            command = self.pt)

        self.radio2 = self.get_radio_button(
            self.top,
            control_variable =self.contrl ,
            returned_value = 6,
            text = "radio2",
            enable = True,
            default_state = False,
            width = None,
            row = 1,
            column = 0,
            align = tk.W,
            command = self.pt)"""






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


    




    def start_collecting(
        self
    ):
        
        self.block_entry()
        self.folder_name = self.e_path.get()
        self.interval = float(self.e_interval.get())
        self.total_time = float(self.e_tot_time.get())*60
        self.num_images = int(self.e_num_images.get())
        self.images_per_folder = int(self.e_images_per_folder.get())
        self.progress_display_frequency = int(self.e_prog_display_freq.get())
        self.quit_value = False
        if self.get_disk_space(self.num_images):
            return None

        if os.path.isdir(self.folder_name):
            shutil.rmtree(self.folder_name,"ignore_errors")
            print("Deleting the Existing Directory...")
            self.update_label(
                self.top,
                label_var =self.progress_var,
                text = "Deleting the Existing Directory...",
                delay = 2 #seconds
            )
        os.mkdir(self.folder_name)
        print("Creating a New Directory : " + os.getcwd() +"/" +self.folder_name )
        self.update_label(
                self.top,
                label_var =self.progress_var,
                text = 'Creating Directory \"{}\"'.format(self.folder_name)
            )

        self.update_label(
                self.top,
                label_var =self.progress_var,
                text = "Capturing Images",
                delay = 2
            )

        print("\nCapturing Images...\n")
        #os.mkdir(self.folder_name+"/0") # Creating initial sub folder
        """
        for pic_number in range(1,self.num_images+1):
            if pic_number%self.images_per_folder==0:
                os.mkdir(self.folder_name+f"/{pic_number//self.images_per_folder}")
            with open(self.folder_name+f"/{pic_number//self.images_per_folder}/" + f"{pic_number}.txt",'w') as foo:
                foo.write('s')
            time.sleep(self.interval)
            if(pic_number%self.progress_display_frequency == 0):
                self.update_label(
                    self.top,
                    label_var =self.progress_var,
                    text = f"{pic_number}/{self.num_images} Images Captured",
                    delay = 0
                )
                print("Captured %i/%i Images..."%(pic_number,self.num_images),end = '\r',flush = True)
        else:
            print("\n")
        """
        
        with picamera.PiCamera() as camera:
            #camera.framerate = 80
            camera.vflip = True                         # Vertically Flipping the camera image
            camera.hflip = True
            camera.resolution = self.resolution_cam     # Setting the resolution of the camera
            camera.exposure_compensation = self.expos_compens # Setting exposure compensation
            self.update_label(                          # Updating progress bar
                    self.top,
                    label_var =self.progress_var,
                    text = "Capturing Images",
                    delay = 2
                )
            print("\nCapturing Images...\n")
            
            for pic_number in range(1,self.num_images+1):
                # Creating sub directories
                if (pic_number-1)%self.images_per_folder==0:
                    os.mkdir(self.folder_name+"/{}".format((pic_number-1)//self.images_per_folder))

                # Capturing and Saving the images into the corresponding sub directory
                camera.annotate_text_size = 17
                camera.annotate_background = picamera.Color('black')
                camera.annotate_text = datetime.now().strftime('%d %m %Y %H:%M:%S')
                camera.capture(self.folder_name+"/{}/{}{}.png".format((pic_number-1)//self.images_per_folder,pic_number,self.file_suffix),format = 'png')
                # Delaying the next image capture
                time.sleep(self.interval)

                # Updating the progress bar
                if(pic_number%self.progress_display_frequency == 0):
                    self.update_label(
                        self.top,
                        label_var =self.progress_var,
                        text = "{}/{} Images Captured".format(pic_number,self.num_images),
                        delay = 0
                    )
                    print("Captured %i/%i Images..."%(pic_number,self.num_images),end = '\r',flush = True)

                if((pic_number-1)%int(self.e_prew_display_freq.get()) == 0):
                    image_path =  self.folder_name+"/{}/{}{}.png".format((pic_number-1)//self.images_per_folder,pic_number,self.file_suffix)
                    thrd = threading.Thread(target = self.load_image,args = ((self.top,self.l_image,image_path)))
                    thrd.start()
                    #self.threaded_load_image(self.top,self.l_image,(self.folder_name+"/{}/{}{}.png".format((pic_number-1)//self.images_per_folder,pic_number,self.file_suffix)))
                
                # listening to stop button
                if self.quit_value:
                    print("Collecting interrupted by user\n")
                    self.update_label(
                        self.top,
                        label_var =self.progress_var,
                        text = 'Stopped data collection',
                        delay =2
                    )
                    self.quit_value = False
                    break
            else:
                print("\n")
        self.normal()
        if(self.c_auto_zip_variable.get() == 1):
            self.zip_folder()
        





    def threaded_start_collecting(
        self
    ):
        print("started threaded capture")
        thrd = threading.Thread(target= self.start_collecting)
        thrd.start()
        



    def zip_folder(
        self
    ):
        self.update_label(
                self.top,
                label_var =self.progress_var,
                text = 'Creating a Zip File \"{}.zip\"'.format(self.folder_name),
                delay =2
            )
        print("Creating Zip File {}.zip".format(self.folder_name))
        shutil.make_archive(self.folder_name, 'zip', self.folder_name)
        self.update_label(
                self.top,
                label_var =self.progress_var,
                text = 'Created a Zip File \"{}.zip\"'.format(self.folder_name),
                delay =2
            )
        
        print("Zip File Created")






    def stop_collecting(
        self
    ):
        self.quit_value = True
        print("stop button pressed")
        #self.top.quit()






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
        if self.r_quality_variable.get() == "Low":
            self.resolution_cam = (720,480)
            self.e_prog_display_freq.delete(0,tk.END)
            if int(self.e_num_images.get())>15: self.e_prog_display_freq.insert(0,'5')
            else: self.e_prog_display_freq.insert(0,'1')
        else:
            self.resolution_cam = (3280,2464)
            self.e_prog_display_freq.delete(0,tk.END)
            self.e_prog_display_freq.insert(0,'1')
        self.block_entry()
        print("Changed the image Quality to {}. Resolution = {}".format(self.r_quality_variable.get(),self.resolution_cam))
        




    def red(
        self
    ):
        self.file_suffix = "_R"
        print("Red light suffix placed")
    




    def yellow(
        self
    ):
        self.file_suffix = "_Y"
        print("Yellow light suffix placed")
    




    def green(
        self
    ):
        self.file_suffix = "_G"
        print("Green light suffix placed")
    




    def normal(
        self
    ):
        self.file_suffix = ""
        print("No light suffix placed")






    def block_entry(
        self
    ):
        """Blocks the dependent text field depending on the radio buttons selected"""
        self.e_num_images.config(state = tk.NORMAL)
        self.e_tot_time.config(state = tk.NORMAL)
        self.e_interval.config(state = tk.NORMAL)

        if self.r_quality_variable.get() == "High":
            self.e_interval.delete(0,tk.END)
            self.e_interval.insert(0,str(0.001))
            self.e_interval.config(state = tk.DISABLED)

            self.e_tot_time.delete(0,tk.END)
            self.e_tot_time.insert(0,str(int(self.e_num_images.get())*10/60.0))
            self.e_tot_time.config(state = tk.DISABLED)

        else:
            if self.r_radio_button_variable.get() == 1:
                self.e_interval.delete(0,tk.END)
                self.e_interval.insert(0,str(float(self.e_tot_time.get())*60/int(self.e_num_images.get())))
                self.e_num_images.config(state = tk.NORMAL)
                self.e_tot_time.config(state = tk.NORMAL)
                self.e_interval.config(state = tk.DISABLED)
                
            elif self.r_radio_button_variable.get() == 2:
                self.e_tot_time.delete(0,tk.END)
                self.e_tot_time.insert(0,str(int(self.e_num_images.get())*float(self.e_interval.get())/60))
                self.e_num_images.config(state = tk.NORMAL)
                self.e_tot_time.config(state = tk.DISABLED)
                self.e_interval.config(state = tk.NORMAL)
            elif self.r_radio_button_variable.get() == 3:
                self.e_num_images.delete(0,tk.END)
                self.e_num_images.insert(0,str(int(float(self.e_tot_time.get())*60/float(self.e_interval.get()))))
                self.e_num_images.config(state = tk.DISABLED)
                self.e_tot_time.config(state = tk.NORMAL)
                self.e_interval.config(state = tk.NORMAL)
            else:
                self.e_num_images.config(state = tk.NORMAL)
                self.e_tot_time.config(state = tk.NORMAL)
                self.e_interval.config(state = tk.NORMAL)



    
    
    
    def threaded_load_image(
        self,
        root,
        label,
        image_path
    ):
        thrd = threading.Thread(target = self.load_image,args = ((root,label,image_path)))
        thrd.start()




    def load_image(
        self,
        root,
        label,
        image_path
    ):               
        image = tk.PhotoImage(file = image_path)
        if self.r_quality_variable.get() == "Low":
            self.preview_image = image.subsample(2,2)
        else:
            self.preview_image = image.subsample(10,10)
        label.config(image=self.preview_image)
        root.update()





    def get_disk_space(
        self,
        num_images
    ):
        space = shutil.disk_usage(os.getcwd())
        free_space = (space.free)/(1024**2) #in MB
        if self.r_quality_variable.get() == "High":
            allowed_images = (int(free_space/11)-100 )//2
        else:
            allowed_images = (int(free_space/0.5)-100 )//2
        if(num_images>allowed_images):
            print("Only {} images can be captured with {} quality".format(allowed_images,self.r_quality_variable.get()))
            self.update_label(
                self.top,
                self.progress_var,
                text = "Stopped. Free space : {} MB.\nMax images in {} quality: {}.".format(round(free_space,2),self.r_quality_variable.get(),allowed_images),
                delay = 2 #seconds
            )
            return True # No hard disk space
        else:
            return False
            
    








    def load_orientation(self):
        
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
    GUI = Data_Collect_GUI()
    #print("clean GPIO remember")
except KeyboardInterrupt:
    GUI.base_servo.pwm.stop()
    GUI.camera_servo.pwm.stop()
    GPIO.cleanup()
    print("GPIO cleanup done : KeyBoardInterrupt")
finally:
    GUI.base_servo.pwm.stop()
    GUI.camera_servo.pwm.stop()
    GPIO.cleanup()
    print("GPIO cleanup done")

