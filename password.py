"""
    Object oriented programmed application
    used sqlite3
    you can customize only "path to db file"
    check code for more informations
"""


import sqlite3

class PasswordManagement:
    def __init__(self, path_to_db : str):
        self.conn = sqlite3.connect(path_to_db)
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS passwords (service TEXT, password TEXT)""")

    def run(self):
        while True:
            self.instruction()
            res = input(":")

            if res == "add":
                self.add()
            elif res == "remove":
                self.remove()
            elif res == "show":
                self.show()
            elif res == "clear":
                self.clear()
            elif res == "ls":
                self.ls()
            elif res == "q":    
                self.c.close()
                self.conn.close()
                break
            else:
                print("Not existing option")

    def instruction(self):
        print("*"*50)
        print("add - add new password")
        print("remove = remove password")
        print("show - show password")
        print("clear - clear console")
        print("ls = list all passwords")
        print("q - quit")
        print("*"*50)

    @staticmethod
    def e():
        print("big E")

    def add(self):
        service = input("Service: ")
        password = input("Password: ")  
        self.c.execute(f"INSERT INTO passwords (service, password) VALUES ('{service}','{password}')")
        self.conn.commit()

    def remove(self):
        service = input("Service: ")
        self.c.execute(f"DELETE FROM passwords WHERE service=?", (service,))
        self.conn.commit()

    def show(self):
        service = input("Service : ")
        self.c.execute('''SELECT * FROM passwords WHERE service=?''', (service,))
        print(self.c.fetchone()[1])

    def clear(self):
        print("\n"*10)

    def ls(self):
        self.c.execute("SELECT * FROM passwords")
        print(self.c.fetchall())

PasswordManagement("databases/passwords.db").run()