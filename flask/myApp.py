from flask import Flask, request, jsonify
import json
import time
from collections import deque
from threading import Lock
import base64
import io
from myServer import MyServer

server = MyServer()

with open('API_KEY.json') as json_data:
    d = json.load(json_data)
    
    API_KEY = d['APIKEY']
    json_data.close()
    

VIDEO_FEED = deque()

app = Flask(__name__)

global lastLife

lastLife = 0

def checkKEY(key):
   
    if key == API_KEY:
        return True
    return False

def add_to_buffer(image):
    print("BUFFER SIZE", len(server.BUFFER))
    with server.BUFFER_LOCK:
        server.BUFFER.append(image)
        if len(server.BUFFER) > server.BUFFER_SIZE:
            server.BUFFER.pop(0)  # Supprime l'image la plus ancienne si le buffer est plein



@app.route('/',methods=['GET'])
def test():
    
        return jsonify({"bundles": "test"}), 200
       
        


@app.route('/api/getdata',methods=['GET'])
def getData():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Process the data (for demonstration, we echo it back)
    key1 = data.get("api_key")
    
    
    
    if checkKEY(key1):
       with server.BUFFER_LOCK:
        if not server.BUFFER:
            return jsonify({"message": "The buffer is empty", "bundles": []}), 200

        
        bundles = [[base64.b64encode(file.read()).decode('utf-8') for file in bundle] for bundle in server.BUFFER]
        server.BUFFER.clear()
        return jsonify({"bundles": bundles}), 200
       
        

@app.route('/api/getcommand',methods=['GET'])
def getCommand():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Process the data (for demonstration, we echo it back)
    key1 = data.get("api_key")
    
    
    
    if checkKEY(key1):
       with server.BUFFER_LOCK:
       
    
            commands = ''.join(str(x) for x in server.COMMAND_BUFFER)
            
            
            response =  jsonify({"commands": commands}), 200
            server.COMMAND_BUFFER.clear()
       
            return response
           
    
    else : 
        return jsonify({"commands": "bad api key"}), 400
       
    
        
    


@app.route('/api/sendData',methods=['POST'])
def sendData():
    # Retrieve API key from the request
    api_key = request.form.get("api_key")

    # Check if API key is valid
    if not checkKEY(api_key):
        return jsonify({"error": "BAD API_KEY"}), 400

    if not request.files:
        return jsonify({"error": "No files provided"}), 400

    # Initialize the bundle list
    bundle = []

    # Process the files in the request
    for key in request.files.keys():
        buffer = io.BytesIO()
        file = request.files[key]
        file.save(buffer)
        buffer.seek(0)
    
        bundle.append(buffer)

        # If the bundle reaches the defined size, add it to the buffer
        if len(bundle) == server.BUNDLE_SIZE:
            with server.BUFFER_LOCK:
                print("BUFFER_SIZE : ", len(server.BUFFER))
                server.BUFFER.append(bundle)
                if len(server.BUFFER) > server.BUFFER_SIZE:
                    server.BUFFER.popleft()  # Remove the oldest bundle if buffer is full
            bundle = []  # Reset the bundle for the next set of files

    # If there are remaining files in the bundle, add them to the buffer
    if bundle:
        with server.BUFFER_LOCK:
            server.BUFFER.append(bundle)
            if len(server.BUFFER) > server.BUFFER_SIZE:
                server.BUFFER.popleft()

    return jsonify({"message": "Files stored in buffer as bundles successfully!"}), 200




@app.route('/api/pingLife',methods=['POST'])
def pingLife():
    print("LAST LIFE ", time.time() - lastLife)
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Process the data (for demonstration, we echo it back)
    key1 = data.get("api_key")
    if checkKEY(key1):
        if  time.time() - lastLife < 10:
            server.ALIVE = True
            
            response = {
                "message": "A",
                
            }
            return jsonify(response), 200
        else : 
            server.ALIVE = False
            server.PORT = ""
            response = {
                "message": "B",
                
            }
            VIDEO_FEED.clear()
            return jsonify(response), 400
    else:
        return jsonify({"error": f"BAD API_KEY "}), 400
        


@app.route('/api/life',methods=['POST'])
def life():
   
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Process the data (for demonstration, we echo it back)
    key1 = data.get("api_key")
    key2 = data.get("life")
    
    
    if checkKEY(key1):
        global lastLife
        lastLife = time.time()
        server.BUFFER.clear()
        
        
        response = {
            "message": "Data received successfully!",
            "received": {
                "API_KEY": key1,
                "life": key2
            }
        }
        return jsonify(response), 200
    else :
         return jsonify({"error": f"BAD API_KEY for keypress {key2}"}), 400

@app.route('/api/resource', methods=['POST'])
def handle_post_request():
    # Retrieve JSON data from the request
    data = request.get_json()

    # Ensure data was received
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Process the data (for demonstration, we echo it back)
    key1 = data.get("api_key")
    key2 = data.get("keyPress")
    
    print('DATA:', data)
    
    if checkKEY(key1):
        lastLife = time.time()
        server.COMMAND_BUFFER.append(key2)
        #print('commands ', COMMAND_BUFFER)
        
        response = {
            "message": "Data received successfully!",
            "received": {
                "API_KEY": key1,
                "keyPress": key2
            }
        }
        return jsonify(response), 200
    else :
         return jsonify({"error": f"BAD API_KEY for keypress {key2}"}), 400
     
     
@app.route('/api/postPorts', methods=['POST'])
def postPorts():
    # Retrieve JSON data from the request
    data = request.get_json()

    # Ensure data was received
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Process the data (for demonstration, we echo it back)
    key1 = data.get("api_key")
    key2 = data.get("ports")
    
    print('DATA:', data)
    
    if checkKEY(key1):

       
        server.PORTS = key2
        #print('commands ', COMMAND_BUFFER)
        
        response = {
            "message": "Data received successfully!",
            
        }
        return jsonify(response), 200
    else :
         return jsonify({"error": f"BAD API_KEY "}), 400
     

@app.route('/api/getPorts', methods=['POST'])
def getPorts():
    # Retrieve JSON data from the request
    data = request.get_json()

    # Ensure data was received
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Process the data (for demonstration, we echo it back)
    key1 = data.get("api_key")

    
    print('DATA:', data)
    
    if checkKEY(key1):

       
        #print('commands ', COMMAND_BUFFER)
        
        response = {
          
                "ports": server.PORTS,
        }
        return jsonify(response), 200
    else :
         return jsonify({"error": f"BAD API_KEY"}), 400
     
     
     
     
     
@app.route('/api/choosePort', methods=['POST',"GET"])
def choosePorts():
    # Retrieve JSON data from the request
    data = request.get_json()

    # Ensure data was received
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Process the data (for demonstration, we echo it back)
    key1 = data.get("api_key")

    
    print('DATA:', data)
    
    if checkKEY(key1):
        
        if request.method == "GET":
             response = {
          
                "port": server.PORT,
        }
             
        if request.method == "POST":
            server.PORT = data.get("port")
            response = {
          
                "port": server.PORT,
        }
            
        
       
        return jsonify(response), 200
    else :
         return jsonify({"error": f"BAD API_KEY"}), 400
        