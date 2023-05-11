import requests
from tkinter import *
import json

#badge
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from FormFacialRecognition import FormFacialRecognition 

class FormBadgeLogin:
    
    def __init__(self):
        GPIO.setwarnings(False)
        
        
    def ApiBadge(self, login:str)->bool:
        reader = SimpleMFRC522()
        badgeId = None
        
        try:
            print("Presenter le badge")
            id, text = reader.read()
            badgeId = id
        finally:
            print("test")
            GPIO.cleanup()
            print(badgeId)
            url = "https://www.btssio-carcouet.fr/ppe4/public/badge/%s/%s" % (login, badgeId)
            request = requests.get(url)
            return True if request.json()["status"] == 'true' else False


    def CheckIntInput(self, value):
        try:
            int(value)
        except:
            value = 30
        finally:
            return value if(value > 0) else 1

    def test(self, window:Tk, login:str):
        print('test')
        FormFacialRecognition.FacialRecognition(window, login)


    def EventBadgeLogin(self, window:Tk, login:str)->None:
        #if ApiBadge(login):
        if True:
            enter = Button(window, text="Lancer la reconnaissance facial", command=lambda:self.test(window, login)).grid(row=1, column=0)
            
            picturesNumberInput = Entry(window, textvariable=login).grid(row=2, column=0)
            picturesNumber = IntVar(window, value=30)
            takePhoto = Button(window, text="Prendre des photos", command=lambda:EventTakePictures(window, login, self.CheckIntInput(picturesNumber))).grid(row=2, column=1)         
        else:
            errorMessage = "Le badge n'est pas valide"
                

    def FormBadgeLogin(self, login:str)->None:
        window = Tk()
        window.geometry("300x250")
      
        #leave = Button(window, text="Annuler", command=lambda:window.destroy()).grid(row=1)
        Label(window, text="Présenter le badge sur le lecteur").grid(row=0)
        window.after(1000, lambda:self.EventBadgeLogin(window, login))
        
        window.mainloop()
