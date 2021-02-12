import os
from moviepy.editor import *
import  numpy as np
from PIL import  Image, ImageEnhance
from matplotlib import cm
from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.lang import  Builder
from kivy.uix.gridlayout import GridLayout
import tkinter as tk
from tkinter import filedialog
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.clock import Clock

Window.size = (900, 800)
Window._set_top(30)

Builder.load_file("EditVideoProgram.kv")
pos_x = 0
pos_y = 0
size_width = 1080
size_height = 1080
contrast  = 1.0
brightness = 1.0
sharpness = 1.0
videoSpeed = 1.0
increaseRed = 0
increaseBlue = 0
increaseGreen = 0
scaleWidth = 1.0
scaleHeight = 1.0


class PathButton(Button):
    @staticmethod
    def get_path():
        root = tk.Tk()
        root.withdraw()

        return( filedialog.askopenfilename() )
    
    @staticmethod
    def get_save_path():
        root = tk.Tk()
        root.withdraw() 

        return( filedialog.askdirectory() )

class MyLayout(GridLayout):
    def renderVideo(self, source_path, destinationPath):
        if self.ids.video_pos_x.text == "" or self.ids.video_pos_y.text == "" or self.ids.video_size_width.text == "" or self.ids.video_size_height.text== "" or self.ids.video_size_scale_width.text == "" or self.ids.video_size_scale_height.text == "" or self.ids.video_speed.text == "" or self.ids.video_output_name.text == "" or self.ids.label.text == "" or self.ids.saveLabel.text == "":
                popup = Popup(title='Error!', content=Label(text='Please fill full information!'),size_hint=(None, None), size=(400, 400))
                popup.open()
        else:
            popup = Popup(title='Waitting!', content=Label(text='Loading....!'),size_hint=(None, None), size=(400, 400))
            popup.open() 
            clip = VideoFileClip(source_path)
        # clip = clip.margin(top=120, bottom=120,color=(220, 20, 60))
            clip = clip.set_position((float(self.ids.video_pos_x.text), float(self.ids.video_pos_y.text))) 
            clip = clip.resize( (float(self.ids.video_size_width.text),float(self.ids.video_size_height.text)) )
            clip = clip.resize( width = clip.w * float(self.ids.video_size_scale_width.text) , height = clip.h * float(self.ids.video_size_scale_height.text)  )
            # sang hon, hoac doi mau clip
            # clip = clip.fx( vfx.colorx, 1.0)
            global contrast
            contrast = float(self.ids.video_contrast.text)
            global brightness 
            brightness = float(self.ids.video_brightness.text)
            global sharpness 
            sharpness = float(self.ids.video_sharpness.text)
            global increaseRed
            increaseRed = float(self.ids.video_color_red.text)
            global increaseGreen
            increaseGreen = float(self.ids.video_color_green.text)
            global increaseBlue
            increaseBlue = float(self.ids.video_color_blue.text)

            clip = clip.fl_image( handleImage )
            videoSpeed = float(self.ids.video_speed.text)
            clip = clip.fx( vfx.speedx, videoSpeed) 
            clip.write_videofile(destinationPath)
            popup.dismiss()
            popup = Popup(title='Success!', content=Label(text='Reder video success!'),size_hint=(None, None), size=(400, 400))
            popup.open()      

class MyApp(App):
    def build(self):
        layout = MyLayout()
        layout.height = 1000
        self.title = 'Edit video program'
        return layout

def handleImage(image):
    pillowImage =  Image.fromarray(image.astype('uint8'), 'RGB')
    enhancerConstact = ImageEnhance.Contrast(pillowImage)
    enhancerBrightness  = ImageEnhance.Brightness(pillowImage)
    enhancerSharpness = ImageEnhance.Sharpness(pillowImage)
    # edit constact
    result = enhancerConstact.enhance(contrast)

    #eidt brightness
    result = enhancerBrightness.enhance(brightness)  

    #edit sharpness
    result = enhancerSharpness.enhance(sharpness)

    #edit color
    if increaseRed != 0 or increaseBlue != 0 or increaseGreen != 0:
        pixels = result.load()
    # return (np.array(result))[:,:,[0,1,1]]
        for i in range(result.size[0]):        #for each column
            for j in range(result.size[1]):
                r, g, b = result.getpixel((i, j))
                newr = r + int(increaseRed)
                if newr > 255:
                    newr = 255
                newg = g + int(increaseGreen)
                if newg > 255:
                    newg = 255
                newb = b + int(increaseBlue)
                if newb > 255:
                    newb = 255    #For each row
                pixels[i,j] = (newr, newg, newb)
    return (np.array(result))

MyApp().run()