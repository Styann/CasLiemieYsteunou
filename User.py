class User:
    login = None
    password = None
    numBadge = None
    numPhase = None
    commentary = None

    def __init__(self) -> None:
        self.login = 'non identifié'
        self.password = ''
        self.commentary = ''

    #get
    def getLogin(self)->str:
        return self.login

    def getPassword(self)->str:
        return self.password

    def getNumBadge(self)->int:
        return self.numBadge

    def getNumPhase(self)->int:
        return self.numPhase

    #set
    def setLogin(self, login:str)->None:
        self.login = login

    def setPassword(self, password:str)->None:
        self.password = password

    def setNumBadge(self, numBagde:int)->None:
        self.numBadge = numBagde

    def setNumPhase(self, numPhase:int)->None:
        self.numPhase = numPhase

    def setCommentary(self, commentary:str)->None:
        self.commentary = commentary
    

    def createLogAcces(self, successful:bool)->tuple:
        return (self.numPhase, self.login, self.numBadge, self.commentary, successful)