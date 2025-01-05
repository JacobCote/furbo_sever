import PIL.Image
import requests
import time
import io
from pynput import keyboard
from utils import keyManager1, sendLife
import json
from threading import Thread
from collections import deque
import PIL
import cv2
import numpy as np
import base64
from utils import Arduino
from threading import Thread




def videoFeed(url,api_key,video_feed):
        
    
    
    last_time = 0 
    time.thread_time_ns
    last_frame =  np.zeros((1080, 1920, 3))
    last_time_get = time.time()
    
    
    while True:
        
        if len(video_feed) < 3 :
            print("SLEEPING FOR BUFFER")
            while len(video_feed) < 10 :
                print(len(video_feed))
                
                time.sleep(0.01)
            
        my_time = time.time()
           
            
        if my_time - last_time > 0.10  :
            print("buffer size = ", len(video_feed) )
            #print(my_time - last_time)
            
            last_time = time.time()
            
            if len(video_feed) == 0 :
                frame = last_frame
            else :
                frame = video_feed.popleft()
                #frame = np.zeros((1080, 1920, 3))
                last_frame = frame
            
            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) == ord('p'):
                break
        
        
       

            
        
        



def getData(url,api_key,video_feed):
    
    info = {
        "api_key" : api_key
    }
    last_time = 0
    while True:
        if time.time() - last_time > 1:
            last_time = time.time()
            response = requests.get(
                url=url,
                json=info
            )
        
        
    
    
        
            
            images = response.json().get("bundles",[])
        
            if not images:
                pass
                
            else : 
        
                #pix = np.array(img[0][0].getdata()).reshape(img.sizeimg[0][0], img[0][0].size[1], 3)
                for bundle in images:
                    for image in bundle :
                        
                        img = PIL.Image.open(io.BytesIO(base64.b64decode(image)))
                        img = np.asarray(img)
                        #bgr_img = cv2.imdecode(base64.b64decode(image),flags=cv2.IMREAD_COLOR)
                    
                    
                        
                        video_feed.append(img)
            
                        
                        
                        
                        
    
                
                    # Convertir l'image en format binaire
                    #image_bytes = io.BytesIO(bytes(image_data[0]['content']))
                    
                    # Charger l'image avec PIL
                    #image = PIL.Image.open(image_bytes)
                    #image
                    #video_feed.append(PIL.Image.open(image_bytes))


        
    

def on_press(key,url,api_key):
    
    
    try:
       
        INPUTKEY = key.char
        
        keyManager1(INPUTKEY,url,api_key)
        if INPUTKEY == "q":
            
            return False
    
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
  
def manageInput(url,api_key):
    with keyboard.Listener(on_press=lambda event : on_press(event, url,api_key)) as listener:
        
        listener.join()
    return
              
        

if __name__ == '__main__' :
    ## check for connection with server
    with open("API_KEY.json") as f :
        d = json.load(f)
        API_KEY = d['APIKEY']
        
    
    
    # URL to send the POST request to
    url = "http://127.0.0.1:5000/api"
    url = "https://jacobcote.pythonanywhere.com/api"
    
    

    # Data to be sent in the request body
    data = {
                "api_key": API_KEY,
                "life": 1
                }

    response = requests.post(url+"/life", json=data)
    if response.status_code == 200:
        print("CONNECTION ESTABLISHED")# Use `json=data` for JSON payloads
    else :
        print("CONNECTION FAILED")
        print("code : ",response.status_code)  # Prints the status code of the response
    
    
    
    global QUIT
    QUIT = False
    VIDEO_FEED = deque()
    
    #ports = getPorts(url=url+'/getPorts',api_key=API_KEY)
    #print(ports)
   
    response = requests.post(url+"/life",json=data)
    t3 = Thread(target=lambda: getData(url+"/getdata",API_KEY,video_feed=VIDEO_FEED))
    t1 = Thread(target=lambda : manageInput(url+"/resource",API_KEY))
    t2 = Thread(target=lambda: sendLife(url+"/life",API_KEY))
    t2.start()
    t3.start()
    
    arduino = Arduino(url=url,api_key=API_KEY)
    arduino.initDistance()
    
    
    

    
     
    t1.start()
    
    
    
   
    
    
    
    
    while len(VIDEO_FEED) < 15 : 
        time.sleep(0.2)
    
    ## setup cam 
    videoFeed(url+"/getdata",API_KEY,VIDEO_FEED)
    



    

# Release the capture and writer objects
    


   