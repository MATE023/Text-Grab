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

root = Tk()
root.attributes('-alpha',0.5)
root.geometry("1000x1000")
root.state('zoomed')

#region = os.environ['ACCOUNT_REGION']
#key = os.environ['ACCOUNT_KEY']
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
    #c.delete("all")
    global x0, y0 
    x0 = eventorigin.x
    y0 = eventorigin.y
    c.bind("<Button 1>",getX)
    
#c.bind("<Button 1>",origin)
    
def getX(eventextentx):
    global xE
    xE = eventextentx.x
    if(xE > screen_width):
        xE = screen_width
    c.bind("<Button 1>",getY)
    
def getY(eventextenty):
    global yE
    yE = eventextenty.y
    if(yE > screen_height):
        yE = screen_height
    c.bind("<Button 1>",copy_text)

def copy_text(event):
    copied_text = ""  
    c.create_rectangle(
        x0, y0, xE, yE,
        outline="#fb0",
        fill="#FFF")
    print(x0, y0, xE, yE)
    
    with mss.mss() as sct:
        box = {"top": x0, "left": y0, "width": xE-x0, "height": yE-y0}
        output = "image.png"
        
        image = sct.grab(box)
        
        mss.tools.to_png(image.rgb, image.size, output=output)
    
    #------------------------------------------------------------------
    #image = ImageGrab.grab(bbox=(x0+180, y0+25, xE+180, yE+25))
    #i = np.asarray(image)
    #image = ImageGrab.grab(bbox=(x0, y0, xE, yE))
    #------------------------
    #image.save("image.png")
    #------------------------
    #Doesn't get here in tile extended outside image case
    #im = Image.fromarray(i)
    #im.tile = [i for i in im.tile if i[1][2] < 2181 and i[1][3]<1294]
    #im.save("im.png")
    #-------------------------------------------------------------------
    #TODO: Set image file name
    upload_file("image.png")
    
    
    
    with open(os.path.dirname(os.path.abspath("image.png")) + "\image.png", "rb") as img_str:
        cl = client.recognize_printed_text_in_stream(
            image=img_str,
            language="en"
        )
    
    text = cl.regions[0].lines
    for t in text:
        line_t = " ".join([word.text for word in t.words])
        copied_text += line_t
        print(line_t)

    pc.copy(copied_text)
    
    c.bind("<Button 1>", origin)
    
    
c.bind("<Button 1>", origin)

def changeText(newText):
    c.create_text(100, 10, fill="darkblue", font="Times 20 italic bold", text=newText)
    c.update
    
root.mainloop()
