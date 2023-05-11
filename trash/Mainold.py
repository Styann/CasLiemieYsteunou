#utility
import requests
from tkinter import *
import json
import time
from datetime import datetime

#badge
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
GPIO.setwarnings(False)

from Recognizer import Recognizer
from Repository import Repository


def ApiLogin(login:str, password:str)->dict:
    url = "https://www.btssio-carcouet.fr/ppe4/public/connect2/%s/%s/infirmiere" % (login, password)
    request = requests.get(url)
    return request.json()
    
def ApiBadge(login:str)->bool:
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


def FacialRecognition(login:str)->None:
    reco = Recognizer()
    if reco.FaceRecognition(login):
        print('authorized')
    else:
        print('unauthorized')

    
def EventBadgeLogin(window:Tk, login:str)->None:
    #if ApiBadge(login):
    if True:
        window.destroy()
        FacialRecognition(login)
    else:
        errorMessage = "Le badge n'est pas valide"
            

def FormBadgeLogin(login:str)->None:
    window = Tk()
    window.geometry("300x250")
  
    #leave = Button(window, text="Annuler", command=lambda:window.destroy()).grid(row=1)
    Label(window, text="Présenter le badge sur le lecteur").grid(row=0)
    window.after(1000, lambda:EventBadgeLogin(window, login))
    
    window.mainloop()
    
  

def EventLogin(window:Tk, login:str, password:str)->None:
    user = ApiLogin(login, password);
    userIsConnected = True if len(user)==13 else False
    errorMessage = ""

    if userIsConnected:
        window.destroy()
        FormBadgeLogin(login)
    else:
        errorMessage = "Les identifiants sont invalides"
    print(errorMessage)


def FormLogin()->None:
    window = Tk()
    window.geometry("300x250")

    Label(window, text="Login : ").grid(row=0)
    Label(window, text="password : ").grid(row=1)

    login = StringVar(window, value="jeanne")
    password = StringVar(window, value="jeanne")
    loginInput = Entry(window, textvariable=login).grid(row=0, column=1)
    passwordInput = Entry(window, textvariable=password, show="●").grid(row=1, column=1)    

    enter = Button(window, text="Ok", command=lambda:EventLogin(window, login.get(), password.get())).grid(row=3, column=0)
    leave = Button(window, text="Quitter", command=lambda:window.destroy()).grid(row=3, column=1)

    window.mainloop()

    


FormLogin()