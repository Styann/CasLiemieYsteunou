import requests
import json
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class NameTag:
    
    def __init__(self):
        GPIO.setwarnings(False)

    def ApiLogin(self, login:str, password:str)->dict:
        url = "https://www.btssio-carcouet.fr/ppe4/public/connect2/%s/%s/infirmiere" % (login, password)
        request = requests.get(url)
        return request.json()
        
    def ApiBadge(self, login:str)->bool:
        reader = SimpleMFRC522()
        badgeId = None
        
        try:
            print("Presenter le badge")
            id, text = reader.read()    
            badgeId = id
        finally:
            GPIO.cleanup()
            url = "https://www.btssio-carcouet.fr/ppe4/public/badge/%s/%s" % (login, badgeId)
            request = requests.get(url)
            return True if request.json()["status"] == 'true' else False
