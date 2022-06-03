import sys
import time

from upload_image import upload_image

from tkinter import *
import tkinter as tk
#import pyscreenshot as ImageGrab
import pyperclip as pc
from PIL import Image, ImageGrab

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

root = Tk()
root.attributes('-alpha',0.5)
root.geometry("1000x1000")


import os
#region = os.environ['ACCOUNT_REGION']
#key = os.environ['ACCOUNT_KEY']
KEY = "443006f6e047441a9185afd881359c2e"
ENDPOINT = "https://textgrab.cognitiveservices.azure.com/"

client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

c = Canvas(root, width=1000, height=1000)
c.pack()

c.create_text(100, 10, fill="darkblue", font="Times 20 italic bold", text="TEXT GRAB")
c.update

def origin(eventorigin):
    global x0, y0
    x0 = eventorigin.x
    y0 = eventorigin.y
    c.bind("<Button 1>",getX)
    
c.bind("<Button 1>",origin)
    
def getX(eventextentx):
    global xE
    xE = eventextentx.x
    c.bind("<Button 1>",getY)
    
def getY(eventextenty):
    global yE
    yE = eventextenty.y
    c.bind("<Button 1>",printcoords)

def printcoords(event):
    #xmpx = xE - x0
    #ympx = yE - y0
    
    text = ""
    
    
    c.create_rectangle(
        x0, y0, xE, yE,
        outline="#fb0",
        fill="#FFF")
    print(x0, y0, xE, yE)
    
    image = ImageGrab.grab(bbox=(x0+180, y0+24, xE+180, yE+24))
    print(x0, y0, xE, yE)
    image.save("image.png")
    #TODO: Set image file name
    upload_image("image.png")
    
    #imageURL = "https://github.com/Azure-Samples/cognitive-services-python-sdk-samples/raw/master/samples/vision/images/make_things_happen.jpg"
    #imageURL = "https://kiosk-dot-codelabs-site.appspot.com/codelabs/mobile-vision-ocr/img/c5134dae01ad22a5.png"    
    imageURL = "https://github.com/mateooos/image/blob/main/imagefolder/image.png?raw=true"
    #imageURL = "https://github.com/mateooos/image/blob/main/imagefolder/image.png?raw=true"
    
    numberOfCharsInOperationId = 36
    
    readT = client.read(imageURL, raw = True)
    opLocation = readT.headers["Operation-Location"]
    id_ = opLocation.split("/")[-1]

    while True:
        readR = client.get_read_result(id_)
        if readR.status not in ['notStarted', 'running']:
            break
        time.sleep(1)
        
    if readR.status == OperationStatusCodes.succeeded:
        for tResult in readR.analyze_result.read_results:
            for line in tResult.lines:
                print(line.text)
                text += line.text
                
    pc.copy(text)
    #changeText(readR)
    
    #print("Origin: ", x0, y0)
    #print("Finish: ", xE, yE)
    #print(xmpx, ympx)
    #print(readR)
    
def changeText(newText):
    c.create_text(100, 10, fill="darkblue", font="Times 20 italic bold", text=newText)
    c.update
    
root.mainloop()