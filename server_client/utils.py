import requests
import time
from serial import Serial
from serial.tools.list_ports import comports

def keyManager(key,serialInst):
    keys = {'a','d'}
    if key in keys:
        serialInst.write((key+'\n').encode("utf-8"))
        
def keyManager1(key,url,api_key):
    keys = {'a','d'}
    if key in keys:
        print("key pressed : ", key)
        data = {
        "api_key": api_key,
        "keyPress": key
        }
        response = requests.post(url, json=data)
        if response.status_code == 200 :
            print(key, " send")

        
    else: 
        print("BAD KEYPRESS")
        
def sendLife(url,api_key):
    while True :
        if round(time.time()) % 10 == 0 :
            data = {
                "api_key": api_key,
                "life": 1
                }
            response = requests.post(url,json=data)
            if response.status_code == 200:
                print("life signal sent")
            else : 
                print('life sent, bad connection')
                print("code", response.status_code)
        time.sleep(1)
            

class Arduino():
    def __init__(self,url, api_key):
        self.url = url
        self.api_key = api_key
        self.ports = []
        self.port = None
        self.serial = Serial()
        self.isInit = False
        self.IsConnected = False
        
    def initDistance(self):
        
        data = {
                "api_key": self.api_key,
                }
    
        response = requests.post(url=self.url+"/getPorts",json=data)
        print(response.json())
        self.ports = response.json()["ports"]
        
        
        for i, port in enumerate(self.ports):
            print(f"{i} :  {port}")
        
        useport = int(input("Choose a port: "))
        self.port  = self.ports[useport].split(' ')[0]
        data = {
            "api_key": self.api_key,
            "port" : self.port
            
        }
        response = requests.post(url=self.url+"/choosePort",json=data)
        print('Choose port status : ',response.status_code)
        
        self.isInit = True
        
        
    def initLocal(self):
        ports = comports()
        portList = [str(i) for i in ports]
        print("AVAILABLE PORTS : ", portList)
        self.ports = portList
        data = {
                "api_key": self.api_key,
                "ports": self.ports
                }
    
        response = requests.post(url=self.url+"/postPorts",json=data)
        print(response.status_code)
        
        
    def initPort(self):
        data = {
            "api_key": self.api_key,
            "port" : self.port
            
        }
        response = requests.get(url=self.url+"/choosePort",json=data)
        print('Choose port status : ',response.status_code)
        self.serial.baudrate = 9600
         #print(use)
        use = response.json()["port"]
        print("CHOSEN PORT : ", use)
        
        while use == '' :
            use = requests.get(url=self.url+"/choosePort",json=data).json()["port"]
            print("CHOSEN PORT : ", use)
            time.sleep(2)
        
        self.serial.port = use
        if not self.serial.is_open:
            self.serial.open()
        
        self.IsConnected
    def manageCommand(self,commands):
        #print("COMMANDS: ", commands)
        #self.serial.write((commands+'\n').encode("utf-8"))
        
        
        for command in commands :
            if command == "a":
                self.serial.write((command+'\n').encode("utf-8"))
            elif command == "d" :
                self.serial.write((command+'\n').encode("utf-8"))
            else:
                print("!!Not a good command!!") 
        commands = ""
        
        
        
        
        
       
    
    

                
def getPorts(url,api_key):
    data = {
                "api_key": api_key,
                }
    
    response = requests.post(url=url,json=data)
    print(response)
    return response.json()["ports"]
    
    

                
        
        
            
    
    
    