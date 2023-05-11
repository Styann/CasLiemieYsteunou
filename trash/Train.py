import cv2
import os
import numpy

PICTURES_FACES_PATH = '/home/ysteunou/Pictures/PicturesFaces/'
HAAR_XML = 'haarcascade_frontalface_default.xml'
MODEL_PATH = '/home/ysteunou/Documents/CasLiemieYsteunou/'

pictures = []
labels = []
cpt = 0
for subFolder in os.listdir(PICTURES_FACES_PATH):
    subFolderPath = os.path.join(PICTURES_FACES_PATH, subFolder)
    
    for filename in os.listdir(subFolderPath):
        picturePath = os.path.join(subFolderPath, filename)
        print(picturePath)
        picture = cv2.imread(picturePath, 0)
        
        pictures.append(numpy.asarray(picture, dtype=numpy.uint8))
        labels.append(cpt)
    cpt += 1

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(pictures, numpy.array(labels))
recognizer.save(MODEL_PATH+'model.yml')
        

