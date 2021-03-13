import sqlite3
import webbrowser

conn = sqlite3.connect("databases/favs.db")

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS favorites (title TEXT, url TEXT)""")

def add():
    shortcut = str(input("shorcut: "))
    url = str(input("url: "))
    c.execute(f"""INSERT INTO favorites (title, url) VALUES ('{shortcut}', '{url}')""")
    conn.commit()

def clear():
    for i in range(30):
        print("\n"*10)


def remove():
    shortcut = input("shortcut: ")
    c.execute(f"DELETE FROM favorites WHERE title = ?", (shortcut,))
    conn.commit()   

def visit(url : str):
    print(f"visiting {url}")
    webbrowser.open(url)

def get_fav(title):
    c.execute('''SELECT * FROM favorites WHERE title=?''', (title,))
    return c.fetchone()

def get_favs():
    c.execute('''SELECT * FROM favorites''')

    results = c.fetchall()
    return results


def v():
    shortcut = input("What is shortcut?: ")
    record = get_fav(shortcut)
    try:
        webbrowser.open(record[1])
    except TypeError:
        print(f"Shortcut '{shortcut}' does not exists!")

def instruction():
    print("*"*30)
    print("v - visit a favorite website")
    print("ls - list all websites")
    print("add - add new website")
    print("rm - remove website")
    print("clear - clear console")
    print("q - quit")
    print("*"*30)


while True:
    instruction()
    
    res = input(":")

    if res == "v":
        v()
    elif res == "ls":
        print(get_favs())
    elif res == "add":
        add()
    elif res == "rm":
        remove()
    elif res == "clear":
        clear()
    elif res == "q":
        break


conn.close()
c.close()