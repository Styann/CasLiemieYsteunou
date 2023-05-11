from bitio.src.microbit import display, Image, sleep
import time
import threading
import trace

class MicroBit:
    
    BLANK = "00000:00000:00000:00000:00000"
    CROSS = "90009:09090:00900:09090:90009"
    CHECK = "00000:00009:00090:90900:09000"
    ARROW_BOTTOM = "00900:00900:90909:09990:00900"
    
    thread = None
    threadrun = True

    def __init__(self):
        display.clear()
        
    def __del__(self):
        display.clear()
    
    def AnimationInterval(self, shape:str, interval:float = 500, repeat:int = 10):        
        for i in range(repeat):
            if self.threadrun:           
                display.show(Image(shape))
                sleep(interval)
                display.clear()
                sleep(interval)
        display.clear()
        print('end thread')
      

    
    def Thread(self, function:callable, params:tuple):
        
        if self.CountSameThread('led') < 2:     
            if self.IsThreadExists('led'):
                self.threadrun = False
                self.thread.join()      
            
            if self.threadrun == False:
                self.threadrun = True
                
            self.thread = threading.Thread(name='led', target=function, args=params)
            self.thread.start() 
      
    def CountSameThread(self, name:str)->bool:
        count = 0
        for thread in threading.enumerate():
            if thread.name == 'led':
                count += 1
        return count
        
    def IsThreadExists(self, name:str)->bool:
        isExists = False
        for thread in threading.enumerate():
            if thread.name == name:
                isExists = True
                break
        return isExists
        
        
    """def GetDisplay(self, shape:str):
        display.show(Image(shape))

    def Clear(self):
        display.clear()"""
    
