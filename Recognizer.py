import os
from os.path import exists
import numpy
from datetime import datetime
#opencv
import cv2
#camera
from picamera import PiCamera

class Recognizer:  
    PICTURES_FACES_PATH = 'PicturesFaces/'
    HAAR_XML = 'haarcascade_frontalface_default.xml'
    
    MODEL_PATH = '/home/ysteunou/Documents/CasLiemieYsteunou/model.yml'
    MODEL_YML = 'model.yml'
  
    names = {}

    def __init__(self):
        #get folderName and indexes
        i = 0
        for subFolder in os.listdir(self.PICTURES_FACES_PATH):
            self.names[i] = subFolder
            i+=1
        del i

    def Mkdir(self, path:str)->bool:
        creationOk = False
        try:
            os.mkdir(path)
            creationOk = True
        except FileExistsError:
            pass
        except FileNotFoundError:
            pass
        finally:
            return creationOk
        
    def FaceRecognition(self, login:str)->bool:          
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(self.MODEL_YML)
        face_cascade = cv2.CascadeClassifier(self.HAAR_XML)
        font = cv2.FONT_HERSHEY_SIMPLEX

        faceCount = 0
        id = 0
        name = None

        capture = cv2.VideoCapture(0)
        (im_width, im_height) = (112, 92)
        #size = 4
        timeout = 0
        
        while faceCount < 30:
            ret, frame = capture.read()
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            faces = face_cascade.detectMultiScale(frame, 1.1, 4)       
            
            
            for (x, y, width, height) in faces:
                cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 3)
                id, confidence = recognizer.predict(gray[y:y + height, x:x + width])
                
                if(confidence < 90):
                    name = self.names[id]
                    if(name == login and len(faces)==1):
                        #print('%s %s' % (login, name))
                        faceCount += 1
                    elif len(faces)>1:
                        cv2.putText(frame, 'trop de visages', (0, 20), font, 0.5, (255, 255, 255), 2)
                else:
                    name = 'inconnu'                
                
                confidence = round(100 - confidence)  
                
                cv2.putText(frame, name, (x+5, y-5), font, 1, (255, 255, 255), 2)
                cv2.putText(frame, str(confidence), (x+5, y+height-5), font, 1, (255, 255, 0), 1)
            
            if(cv2.waitKey(1) & 0xFF == ord('x')):
                break
            
            if timeout >= 100:
                break
            timeout += 1
            
            
            cv2.imshow("capture", frame)
        capture.release()
        cv2.destroyAllWindows()
        return True if (faceCount >= 5) else False
        
    def TakePictures(self, directory:str, picturesNumber:int=30):
        path = self.PICTURES_FACES_PATH+directory
        
        face_cascade = cv2.CascadeClassifier(self.HAAR_XML)
        (im_width, im_height) = (112, 92)
        size = 4
        capture = cv2.VideoCapture(0)
        
        if exists(path):
            pass
        else:
            self.Mkdir(path)
            
        i = 0
        while i < picturesNumber:
            ret, frame = capture.read()
            frame = cv2.flip(frame, 1, 0)        
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            faces = face_cascade.detectMultiScale(frame, 1.1, 4)
            face = None
                
            if(len(faces) == 1):
                face = faces[0]
        
                (x, y, width, height) = face
                face = gray[y:y + height, x:x + width]
                faceResized = cv2.resize(face, (im_width, im_height))
                
                cv2.rectangle(frame, (x-10, y-10), (x + width+10, y + height+10), (0, 255, 0), 3)
                
                cv2.imwrite(path+"/picture%d.png" % (i), faceResized)
                i+=1
                print('Done %d' % (i))

                if cv2.waitKey(1) & 0xFF == ord('x'):
                    break

            cv2.imshow("capture", frame)
        capture.release()
        cv2.destroyAllWindows()
    
    def Training(self):
        pictures = []
        labels = []
        cpt = 0
        for subFolder in os.listdir(self.PICTURES_FACES_PATH):
            subFolderPath = os.path.join(self.PICTURES_FACES_PATH, subFolder)
            
            for filename in os.listdir(subFolderPath):
                picturePath = os.path.join(subFolderPath, filename)
                #print(picturePath)
                picture = cv2.imread(picturePath, 0)
                
                pictures.append(numpy.asarray(picture, dtype=numpy.uint8))
                labels.append(cpt)
            cpt += 1

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(pictures, numpy.array(labels))
        if exists(self.MODEL_PATH):
            os.remove(self.MODEL_PATH)
        recognizer.save(self.MODEL_PATH)
    
    
#reco = Recognizer()
#reco.TakePictures('test', 45)
#reco.Training()
#reco.FaceRecognition('jeanne')