import PIL
import io
import PIL.Image
import cv2
import time
import numpy as np
from collections import deque
import requests
from threading import Thread
import json
from utils import Arduino

VIDEO_FEED = deque()
PINGLIFE_URL = "http://127.0.0.1:5000/api/pingLife"


def fetchCommand(api_key,url):
    info = {
        "api_key" : api_key
    }
    response = requests.get(
        url=url,
        json=info
    )
    
    return response.json()["commands"]
    
    
    

def sendToServer(api_key,images,url):
   

    data = {
         "api_key" : api_key,

    }

    files = {f'image_{i}': (f'image_{i}.jpg', io.BytesIO(images[i]), 'image/jpeg') for i in range(len(images))}
    
    response = requests.post(
        url=url,
        files=files,
        data=data
    )
    
    
def captureImage(image):
    buffer = io.BytesIO()
    img = PIL.Image.fromarray(image)
    img.save(buffer,"JPEG",quality=70)
    buffer.seek(0)
    return buffer.getvalue()

def pingLife(api_key,url):
    data = {
        "api_key" : api_key
    }
    r = requests.post(url+"/pingLife",json=data)
    
    return r.status_code == 200
    

    
def camera(api_key,url,commands):
    global RECORD
    RECORD = True
    
    # Open the default camera
    try :
        cam = cv2.VideoCapture(1)
    except :
        cam = cv2.VideoCapture(0)
        

    # Get the default frame width and height
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))



    # Define the codec and create VideoWriter object
    
    

    n_image = 0 
    lastPing = time.time()
    up = pingLife(api_key,url)
    buffer_images = []
    last_time = time.time()
    arduino = Arduino(url=url,api_key=api_key)
    arduino.initLocal()
    was_up = False
    
    
    while RECORD:
        mytime = time.time()
        if  mytime - lastPing > 2 :
            up = pingLife(api_key,url)
            if up and not was_up: 
                print(up,was_up)
                arduino.IsConnected = True
                arduino.initPort()
                was_up = True
                
            elif not up : 
                was_up = False
                arduino.IsConnected = False
                arduino.port = ""
            lastPing = time.time()
            
     
       
        
        
        
        if mytime - last_time > 0.035 :
            
            last_time = time.time()
            ret, frame = cam.read()
            frame = np.array(frame,dtype=np.uint8)
        
            jpeg = captureImage(frame)
            buffer_images.append(jpeg)
            n_image +=1
        

            if n_image == 5  :
                
                n_image = 0
                if up :
                    #if arduino.IsConnected:
                        #arduino.initPort()
                    command = fetchCommand(api_key, url+"/getcommand")
                    if command != '' :
                        commands += command
                        arduino.manageCommand(commands)
                        commands = ""
                
                    sendToServer(images=buffer_images,url=url+"/sendData",api_key=api_key)
                    pass
                else :
                    arduino.IsConnected = False
                    arduino.port = ""
                    
                buffer_images = []
                

    
    cam.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    ACTIVE = True
    url = 'http://127.0.0.1:5000/api'
    with open('API_KEY.json') as f:
        d = json.load(f)
        api_key = d['APIKEY']
   
        
    
    commands= ''

    # Data to be sent in the request body
    #t1 = Thread(target=lambda : manageArduino(ACTIVE,commands,url=url+"/postPorts",api_key=api_key))
    #t1.start()
    #t2 = Thread(target=lambda: camera(api_key,url+"/sendData",commands=commands))
    #t2.start()
    
    camera(api_key,url,commands=commands)
    
    
    