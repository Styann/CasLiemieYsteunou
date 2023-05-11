from os.path import exists
from os import mkdir
from datetime import datetime
#opencv
import cv2
#camera
from picamera import PiCamera


PICTURES_FACES_PATH = '/home/ysteunou/Documents/CasLiemieYsteunou/PicturesFaces/'
HAAR_XML = 'haarcascade_frontalface_default.xml'

def CheckDir(directory:str)->bool:
    return True if exists(directory) else False

def Mkdir(path:str)->str:
    creationOk = False
    try:
        mkdir(path)
        creationOk = True
    except FileExistsError:
        pass
    except FileNotFoundError:
        pass
    finally:
        return creationOk
        
def TakePictures(directory:str):
    face_cascade = cv2.CascadeClassifier(HAAR_XML)
    (im_width, im_height) = (112, 92)
    size = 4
    capture = cv2.VideoCapture(0)
    
    if exists(directory):
        pass
    else:
        Mkdir(directory)
    
    while True:
        ret, frame = capture.read()
        frame = cv2.flip(frame, 1)
                
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(frame, 1.1, 4)
        face = None
            
        if(len(faces) > 0):
            face = faces[0]
    
            (x, y, width, height) = face
            face = gray[y:y + height, x:x + width]
            faceResized = cv2.resize(face, (im_width, im_height))
            
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 3)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite(directory+"/picture%s.png" % (datetime.now().strftime("%m%d%Y %H%M%S")), face)
                print('Done')
            elif cv2.waitKey(1) & 0xFF == ord('x'):
                break

        

        cv2.imshow("capture", frame)


    capture.release()
    cv2.destroyAllWindows()
    

TakePictures(PICTURES_FACES_PATH+'test')