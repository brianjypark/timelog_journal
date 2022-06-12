import sqlite3

conn = sqlite3.connect('activity.db')
c = conn.cursor()

def closeConn():
    c.close()
    conn.close()

def createTable():
    c.execute('''CREATE TABLE activity (
        start_time text,
        end_time text,
        category text,
        note text
    )''')
    conn.commit()

def dropTable():
    c.execute('''DROP TABLE activity''')
    createTable()
    conn.commit()

def addActivity(start, end, category, note):
    c = conn.cursor()
    c.execute("INSERT INTO activity (start_time, end_time, category, note) VALUES (?,?,?,?)", (start, end, category, note))
    conn.commit()

def editActivity():
    pass

def deleteActivity(del_idx):
    c.execute("DELETE FROM activity WHERE rowid=?", (del_idx,))
    conn.commit()
    print("Deleted activity")

def getCount():
    c.execute("SELECT COUNT(*) FROM activity")
    count = c.fetchone()
    return count[0]

def fetchActivity():
    c = conn.cursor()
    c.execute('''SELECT rowid, * FROM activity ''')
    items = c.fetchall()
    for log in items:
        print(str(log[0]) + '\t ' + log[1] + '\t ' + log[2] + '\t ' + log[3] + '\t ' + log[4])
        #print(log)

def calcDuration():
    pass


