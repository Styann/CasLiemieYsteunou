#utility
import requests
from tkinter import *
import json
import time
from datetime import datetime
import sys

#badge
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
GPIO.setwarnings(False)

from Recognizer import Recognizer
from Repository import Repository
from MicroBit import MicroBit
from User import User
  
led = MicroBit()
user = User()
repository = Repository()

def AppExit(user:User, numPhase:int):
    if(numPhase):
        user.setNumPhase(numPhase)
    user.setCommentary('à fermer l\'application')
    raise SystemExit

def ApiLogin(user:User)->dict:
    url = "https://www.btssio-carcouet.fr/ppe4/public/connect2/%s/%s/infirmiere" % (user.getLogin(), user.getPassword())
    request = requests.get(url)
    return request.json()
    
def ApiBadge(user:User)->bool:
    reader = SimpleMFRC522()
    
    try:
        print("Presenter le badge")
        id, text = reader.read()
        user.setNumBadge(int(id))
    finally:
        GPIO.cleanup()
        url = "https://www.btssio-carcouet.fr/ppe4/public/badge/%s/%s" % (user.getLogin(), user.getNumBadge())
        request = requests.get(url)
        return True if request.json()["status"] == 'true' else False

def EventTakePictures(window:Tk, directory:str, picturesNumber:int):
    window.destroy()
    reco = Recognizer()
    reco.TakePictures(directory, picturesNumber)
    reco.Training()
    del reco

def FormEnd()->None:
    window = Tk()
    window.title('accès au coffre')
    window.geometry('400x250')
    Label(window, text='Le coffre fort est ouvert').grid(row=2)
    leave = Button(window, text='Quitter', command=lambda:AppExit(user, 99)).grid(row=1)
       

def FacialRecognition(window:Tk)->None:
    user.setNumPhase(3)

    window.destroy()
    reco = Recognizer()
    if reco.FaceRecognition(user.getLogin()):
        led.Thread(led.AnimationInterval, (led.CHECK,))
        user.setCommentary('visage reconnu avec succès')
        repository.InsertLogAcces(user.createLogAcces(True))
        FormEnd()
    else:
        user.setCommentary('visage non reconnu')
        raise SystemExit
        
def CheckIntVarInput(var:IntVar)->int:
    try:
        var = var.get()
        int(var)
        return var if(var > 0) else 1
    except:
        return 30
     
    
def EventBadgeLogin(window:Tk)->None:
    user.setNumPhase(2)

    #if ApiBadge(user):
    if True:
        led.Thread(led.AnimationInterval, (led.CHECK,))
        user.setCommentary('badge reconnu avec succès')
        repository.InsertLogAcces(user.createLogAcces(True))
        login = user.getLogin()
        enter = Button(window, text="Lancer la reconnaissance facial", command=lambda:FacialRecognition(window)).grid(row=1, column=1)
        
        picturesNumber = IntVar(window, value=30)
        picturesNumberInput = Entry(window, textvariable=picturesNumber).grid(row=3, column=0)
        
        takePhoto = Button(window, text="Prendre des photos (30 par défaut)", command=lambda:EventTakePictures(window, login, CheckIntVarInput(picturesNumber))).grid(row=3, column=1)
    else:
        user.setCommentary('badge invalide')
        raise SystemExit
    

def FormBadgeLogin()->None:
    window = Tk()
    window.title('lecture de badge')
    window.geometry("500x250")
  
    Label(window, text="Présenter le badge sur le lecteur").grid(row=0, column=0)
    leave = Button(window, text="Quitter", command=lambda:AppExit(user, 2)).grid(row=1, column=0)
    window.after(1000, lambda:EventBadgeLogin(window))
    
    window.mainloop()
    
  

def EventLogin(window:Tk, login:str, password:str)->None:
    user.setLogin(login)
    user.setPassword(password)
    user.setNumPhase(1)

    userJson = ApiLogin(user)
    userIsConnected = True if len(userJson)==13 else False

    if userIsConnected:
        window.destroy()
        led.Thread(led.AnimationInterval, (led.CHECK,))
        user.setCommentary('identifiants valides')
        repository.InsertLogAcces(user.createLogAcces(True))
        FormBadgeLogin()
    else:
        user.setCommentary('identifiants invalides')
        raise SystemExit

def FormLogin()->None:
    window = Tk()
    window.title('connexion')
    window.geometry("300x250")

    Label(window, text="Login : ").grid(row=0, pady=(20, 0), padx=(20, 0))
    Label(window, text="password : ").grid(row=2, pady=(0, 0), padx=(20, 0))

    login = StringVar(window, value="")
    password = StringVar(window, value="")
    loginInput = Entry(window, textvariable=login).grid(row=0, column=1, pady=(20, 0), padx=(20, 0))
    passwordInput = Entry(window, textvariable=password, show="●").grid(row=2, column=1, pady=(0, 0), padx=(20, 0))    

    leave = Button(window, text="Quitter", command=lambda:AppExit(user, 1)).grid(row=3, column=0, pady=(20, 0), padx=(20, 0))
    enter = Button(window, text="Ok", command=lambda:EventLogin(window, login.get(), password.get())).grid(row=3, column=1, pady=(20, 0), padx=(20, 0))

    window.mainloop()

    

try:
    FormLogin()
except SystemExit:
    led.Thread(led.AnimationInterval, (led.CROSS,))
    if(user.getNumPhase() < 4):
        repository.InsertLogAcces(user.createLogAcces(False))
finally:
    repository.Close()
    sys.exit()