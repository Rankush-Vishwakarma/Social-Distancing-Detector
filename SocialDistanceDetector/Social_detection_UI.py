# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 20:36:34 2022

@author: rvishwakar23
"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from social_distance_detector import Detector
from tkinter import messagebox
from loggingModule import makeLog
# initializing the detector module
detector = Detector()
log = makeLog()
filename = None
# defining the function for selecting the input video file
def select_file():
    try:
        global filename
        filetypes = (
            ('video files', '*.mp4'),
            ('All files', '*.MP4')
        )
    
        filename = fd.askopenfilename(
            title='Open video file',
            initialdir='/',
            filetypes=filetypes)
        log.info('File name choosen successfully')
    except Exception as e:
        log.error(e)
# defining temorary text
def temp_text(e):
    try:
        OutputFileName.delete(0,"end")
        log.info('Temprary text deleted successfully ')
    except Exception as e:
        log.debug(e)
   
# making detection
def Detect():
    if OutputFileName.get() == "Enter file name without extension":
        messagebox.showerror('Error','Error! No Output file Found.') 
        log.error('Error! No Output file Found.')
    if filename is None or 'C:' not in filename:
        messagebox.showerror('Error','Error! Video FileName not Found.')
        log.error('Error! Video FileName not Found.')
    else:
        detector.social_distance_detector(filename,OutputFileName.get())
        OutputFileName.delete(0, END)

# closing the UI
def close():
    try:
       master.destroy()
       log.info('UI closed successfully')
    except Exception as e:
        log.debug(e)
   
if __name__ == '__main__':
    master = tk.Tk()
    master.title('Social Distance Detector')
    master.resizable(False, False)
    master.geometry('400x250')
    
    tk.Label(master, 
             text="Output File").place(x = 60,
                                      y = 70) 
    tk.Label(master, 
             text="Input File").place(x = 70,
                                      y = 100) 
    
    OutputFileName = tk.Entry(master, width = 28)
    OutputFileName.insert(0,'Enter file name without extension')
    OutputFileName.bind("<FocusIn>",temp_text)
    open_button = ttk.Button(
        master,
        text='Open a File',
        command=select_file
    )
    OutputFileName.place(x = 150,y = 70) 
    open_button.place(x = 150,y = 100) 
    tk.Button(master, 
              text='Quit', 
              command=close).place(x=100,y=200)
    tk.Button(master, 
              text='Detect', command=Detect).place(x=200,y=200)
    
    tk.mainloop()