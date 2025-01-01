from flask import Flask, request, jsonify
import json
import time
from collections import deque
from threading import Lock
import base64
import io

BUFFER = deque()
COMMAND_BUFFER = []
BUFFER_LOCK = Lock()
BUFFER_SIZE = 10
BUNDLE_SIZE = 5
PORTS = []


class MyServer():
    def __init__(self):
        self.BUFFER = deque()
        self.COMMAND_BUFFER = []
        self.BUFFER_LOCK = Lock()
        self.BUFFER_SIZE = 10
        self.BUNDLE_SIZE = 5
        self.PORTS = []
        self.PORT = ""
    
    