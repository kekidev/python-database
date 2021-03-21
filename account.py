import hashlib
import sqlite3
import random
import string

class Account:
    def __init__(self):
        self.conn = sqlite3.connect("./databases/accounts.db")
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
            elif option == "d":
                self.delete_account()
            elif option == "q":
                break
            else:
                print("invalid option")

    def instruction(self):
        print("*"*50)
        print("c - create account")
        print("l - login")
        print("d - delete account")
        print("q - quit")
        print("*"*50)

    def create_account(self):
        sha256 = hashlib.sha256()
        md5 = hashlib.md5()
        email = input("Set email: ")
        password = input("Set password: ")

        # Encyprt password twice
        sha256.update(password.encode("utf-8"))
        md5.update(sha256.hexdigest().encode("utf-8"))

        # Create random salt
        salt = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

        # Add salt to encrypted password
        encrypted_password = md5.hexdigest() + salt


        print(f"Successfully encrypted password\nencrypted value: {encrypted_password}")
        self.c.execute(f"""INSERT INTO accounts (email, password) VALUES ('{email}','{encrypted_password}')""")
        self.conn.commit()

        print("Successfully created account")
        
    def login(self):
        sha256 = hashlib.sha256()
        md5 = hashlib.md5()

        email = input("Enter email: ")
        password = input("Enter password: ")
        
        # Encrypt password using sha256 algorithm
        sha256.update(password.encode("utf-8"))
        # Encyprt encrypted password using md5 algorithm 
        md5.update(sha256.hexdigest().encode("utf-8"))

        # Get salt 
        salt = self.get_salt(email)

        # if account dosent exists it returns False
        if salt == False:
            return 

        # Final encrypted password
        # Add salt to the Encrypted md5 password
        encrypted_password = md5.hexdigest() + salt

        # Check if email, password matches
        self.c.execute("SELECT * from accounts WHERE email=? and password= ?", (email, encrypted_password))

        found = self.c.fetchone()

        if found:
            print(found)
            print("Successfully logged in")
        else:
            print("Incorrect email or password")

    def get_salt(self, email):
        self.c.execute("SELECT * from accounts WHERE email=?", (email,))

        
        try:
            # Return last 5 characters which is salt
            return self.c.fetchone()[1][-5:]
        except TypeError:
            print("That account dosent exists")
            return False

    def delete_account(self):
        email = input("Enter email: ")
        password = input("Enter password: ")

        sha256 = hashlib.sha256()
        md5 = hashlib.md5()

        sha256.update(password.encode("utf-8"))
        md5.update(sha256.hexdigest().encode("utf-8"))

        salt = self.get_salt(email)

        if salt == False:
            return 

        encrypted_password = md5.hexdigest() + salt

        self.c.execute("DELETE FROM accounts WHERE email=? AND password=?", (email,encrypted_password))
        self.conn.commit()

Account().run()