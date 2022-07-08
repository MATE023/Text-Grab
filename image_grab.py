import os
import sys
import time
import mss
import mss.tools

from upload_image import upload_image
from upload_image_a import upload_file

from tkinter import *
import tkinter as tk
import pyperclip as pc
from PIL import Image, ImageGrab
import numpy as np


from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OcrLine, OcrWord

root = Tk()
root.attributes('-alpha',0.5)
root.geometry("1000x1000")
root.state('zoomed')

KEY = "************************"
ENDPOINT = "****************************"
conn_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = "words"
blob_name = "image.png"

client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

c = Canvas(root, width=1000, height=1000)
c.pack()

c.create_text(100, 10, fill="darkblue", font="Times 20 italic bold", text="TEXT GRAB")
c.update

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

def origin(eventorigin):
    global x0, y0 
    x0 = eventorigin.x
    y0 = eventorigin.y

    root.bind('<Double-Button-1>', callback0)
    
    
def callback0(e):
    global x0
    global y0
    x0 = e.x
    y0 = e.y
    root.bind('<Double-Button-1>', callbackE)
   

def callbackE(e):
    global xE
    global yE
    xE = e.x
    yE = e.y
    copy_text()
    

def createImage():
    with mss.mss() as sct:
        #       height       width
        box = {"top": y0+24, "left": x0+181, "width": abs(xE-x0), "height": abs(yE-y0)}
        #      + to push down  + to push right

        output = "image.png"
        
        image = sct.grab(box)
        
        mss.tools.to_png(image.rgb, image.size, output=output)
            
    upload_file("image.png")

def copy_text():
    copied_text = ""  
    c.create_rectangle(
        x0, y0, xE, yE,
        outline="#fb0",
        fill="#FFF")
           
    createImage()

    with open(os.path.dirname(os.path.abspath("image.png")) + "\image.png", "rb") as img_str:
        cl = client.recognize_printed_text_in_stream(
            image=img_str,
            language="en"
        )
    
    if(len(cl.regions) > 0):
        text = cl.regions[0].lines
    else:
        words = OcrWord(bounding_box = "", text="No text detected.")
        text = [OcrLine(bounding_box = "", words=[words])]
    
    for t in text:
        line_t = " ".join([word.text for word in t.words])
        copied_text += line_t
        print(line_t)
                
    
    pc.copy(copied_text)
    
    root.bind('<Double-Button-1>', origin)
    
root.bind('<Double-Button-1>', origin)


def changeText(newText):
    c.create_text(100, 10, fill="darkblue", font="Times 20 italic bold", text=newText)
    c.update
    
root.mainloop()
