import requests
from tkinter import *
import json

from Recognizer import Recognizer


class FormFacialRecognition():
      
    def __init__(self):
        pass
                        
    def EventTakePictures(self, window:Tk, directory:str, picturesNumber:int):
        window.destroy()
        reco = Recognizer()
        reco.TakePictures(directory, picturesNumber)
        del reco


    def FacialRecognition(self, window:Tk, login:str)->None:
        window.destroy()
        reco = Recognizer()
        if reco.FaceRecognition(login):
            print('authorized')
        else:
            print('unauthorized')
            
