import sys
import time

from upload_image import upload_image
from upload_image_a import upload_file

from tkinter import *
import tkinter as tk
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
    c.bind("<Button 1>",copy_text)

def copy_text(event):
    text = ""  
    c.create_rectangle(
        x0, y0, xE, yE,
        outline="#fb0",
        fill="#FFF")
    print(x0, y0, xE, yE)
    
    image = ImageGrab.grab(bbox=(x0+180, y0+25, xE+180, yE+25)) 

    image.save("image.png")
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
        print(line_t)
    #----------------------------------------------------------------------------
    #imageURL = "https://github.com/Azure-Samples/cognitive-services-python-sdk-samples/raw/master/samples/vision/images/make_things_happen.jpg"
    #numberOfCharsInOperationId = 36
    
    #readT = client.read(imageURL, raw = True)
    #opLocation = readT.headers["Operation-Location"]
    #id_ = opLocation.split("/")[-1]

    #while True:
    #    readR = client.get_read_result(id_)
    #    if readR.status not in ['notStarted', 'running']:
    #        break
    #    time.sleep(1)
        
    #if readR.status == OperationStatusCodes.succeeded:
    #    for tResult in readR.analyze_result.read_results:
    #        for line in tResult.lines:
    #            print(line.text)
    #            text += line.text
    #-----------------------------------------------------------------------------
    
    pc.copy(line_t)
    
def changeText(newText):
    c.create_text(100, 10, fill="darkblue", font="Times 20 italic bold", text=newText)
    c.update
    
root.mainloop()