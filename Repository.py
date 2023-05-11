import sqlite3

class Repository:
    DB_PATH = "casLiemieYsteunou.db"
    db = None
    
    def __init__(self):
        self.db = sqlite3.connect(self.DB_PATH)
        
    def Close(self):
        self.db.close()
    
    def InsertLogAcces(self, data:tuple)->bool:
        isNoError = True
        try:
            cur = self.db.cursor()
            cur.execute("INSERT INTO log_acces(num_phase, login, num_badge, commentary, successful) values(?, ?, ?, ?, ?);", data)
            self.db.commit()
        except sqlite3.Error:
            isNoError = False
        finally:
            return isNoError

    def FindAllLogAcces(self)->list:
        try:
            cur = self.db.cursor()
            result = cur.execute("SELECT * FROM log_acces;")
            return result.fetchall()
        except sqlite3.Error:
            return []

    def FindLogAccesByLogin(self, login:str)->list:
        try:
            cursor = self.db.cursor()
            result = cursor.execute("SELECT * FROM log_acces WHERE log_acces.login like ?;", (login,))
            return result.fetchall()
        except sqlite3.Error:
            return []


"""repo= Repository()
#print(repo.InsertLogAcces((1, 'D.TURNER', None, '', False)))
#print(repo.InsertLogAcces((1, 'K.LINGARD', None, '', True)))

for i in repo.FindAllLogAcces():
    print(i)
  

print('\n')

for i in repo.FindLogAccesByLogin('D.TURNER'):
    print(i)
  


repo.Close()"""