#!/usr/bin/python3
import pathlib
import tkinter.ttk as ttk
import pygubu
import os
import tkinter as tk
from PIL import Image, ImageTk
import pyglet
import webbrowser

from helpers.serial import F8000A_Serial
from helpers.display import F8000A_Display

import threading

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = os.path.join(PROJECT_PATH, "ui/", "main.ui")
PROJECT_ICO = os.path.join(PROJECT_PATH, "../res/icon.png")

pyglet.font.add_file(os.path.join(PROJECT_PATH, "../fonts/DSEG_v046/DSEG7-Classic/DSEG7Classic-Regular.ttf"))

class FL8000A:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        self.mainwindow.geometry("{}x{}".format(1024, 384))
        builder.connect_callbacks(self)      
        
        self.serPort = None
        self.serSpeed = None
        builder.import_variables(self, ['serPort', 'serSpeed'])
        
        # Setup style
        self.mainwindow.tk.call('source', os.path.join(os.getcwd(), 'frontend/res/forest-ttk/forest-dark.tcl'))
        self.style = ttk.Style(self.mainwindow)
        self.style.theme_use('forest-dark')  
        
        # Set icon
        ico = Image.open(PROJECT_ICO)
        photo = ImageTk.PhotoImage(ico)
        self.mainwindow.wm_iconphoto(False, photo)

        # Set canvas
        self.display = F8000A_Display(builder.get_object("displaycanvas"))
        
        self.serial = F8000A_Serial()
        self.serialRefresh()

    def on_quit(self, event=None):
        if self.serial.connected:
            self.serial.disconnect()    
        self.mainwindow.quit()  # Close main

    def run(self):
        self.mainwindow.mainloop()
        
    def openLink(self, widget_id):
        if widget_id == "btnArnweb":
            webbrowser.open("https://arnweb.nl")
        elif widget_id == "btnGithub":
            webbrowser.open("https://github.com/the-real-mcarn/Fluke8000A_Datalogger")
        else:
            print("Unknown link: {}".format(widget_id))
    
    def serialCtl(self, widget_id):
        btn = self.builder.get_object(widget_id)
        self.serial.speed = self.serSpeed.get()
        self.serial.port = self.serPort.get()
        
        if self.serial.connected:
            self.serial.disconnect()
            btn.configure(text="Connect")
        else:
            self.serial.connect()
            self.serialThread = threading.Thread(target=self.serial.read, args=(self.update,)).start()
            btn.configure(text="Disconnect")
    
    def serialRefresh(self):
        self.builder.get_object("serPorts").configure(values=self.serial.listPorts())
    
    def setFunc(self, widget_id):
        w = widget_id.split('_')
        
        if w[1] == "acv": self.display.setPolarity(False)
        elif w[1] == "acma": self.display.setPolarity(False)
        elif w[1] == "dcv": self.display.setPolarity(True)
        elif w[1] == "dcma": self.display.setPolarity(True)
        elif w[1] == "kohm": self.display.setPolarity(False)
        elif w[1] == "mohm": self.display.setPolarity(False)

    def setRange(self, widget_id):
        w = widget_id.split('_')
        
        if w[1] == "0_2": self.display.setDecimalPos(3)
        elif w[1] == "2": self.display.setDecimalPos(1)
        elif w[1] == "20": self.display.setDecimalPos(2)
        elif w[1] == "200": self.display.setDecimalPos(3)
        elif w[1] == "2000": self.display.setDecimalPos(0)

    def setPower(self, widget_id):
        print(widget_id)
        self.display.setDecimalPos(1)
        self.display.update([0, 0, 0, 0], 0, 0)
        pass
    
    def update(self, data):
        digits = data['digits']
        polarity = data['polarity']
        overload = data['overload']
        self.display.update(digits, polarity, overload)

if __name__ == "__main__":
    app = FL8000A()
    app.run()

