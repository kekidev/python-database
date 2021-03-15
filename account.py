"""
    Get user's input and encrypt using sha256 algorithm and store it in database
    Get user's input and encrypt with same algorithm and check if 
    email & encrypted password are same then it says logged in
"""

import hashlib
import sqlite3

class Account:
    def __init__(self):
        self.conn = sqlite3.connect("./database/accounts.db")
        self.c = self.conn.cursor()

        self.c.execute("""CREATE TABLE IF NOT EXISTS accounts (email text, password text)""")

    def run(self):
        while True:
            self.instruction()
            option = input(":")

            if option == "c":
                self.create_account()
            elif option == "l":
                self.login()
            elif option == "q":
                break
            else:
                print("invalid option")

    def instruction(self):
        print("*"*50)
        print("c - create account")
        print("l - login")
        print("q - quit")
        print("*"*50)

    def create_account(self):
        m = hashlib.sha256()
        email = input("Set email: ")
        password = input("Set password: ")
        m.update(password.encode("utf-8"))
        print(f"Successfully encrypted password\nencrypted value: {m.hexdigest()}")
        self.c.execute(f"""INSERT INTO accounts (email, password) VALUES ('{email}','{m.hexdigest()}')""")
        self.conn.commit()

        print("Successfully created account")
        
    def login(self):
        m = hashlib.sha256()

        email = input("Enter email: ")
        password = input("Enter password: ")
        
        m.update(password.encode("utf-8"))

        self.c.execute("SELECT * from accounts WHERE email=? and password= ?", (email, m.hexdigest()))

        found = self.c.fetchone()

        if found:
            print(found)
            print("Successfully logged in")
        else:
            print("Incorrect email or password")

Account().run()