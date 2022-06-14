import sqlite3
from datetime import datetime, date, timedelta

conn = sqlite3.connect('activity.db', detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES)
c = conn.cursor()

def closeConn():
    c.close()
    conn.close()

def createTable():
    c.execute('''CREATE TABLE activity (
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        category text,
        note text
    )''')
    conn.commit()

def dropTable():
    c.execute('''DROP TABLE activity''')
    conn.commit()
    createTable()

def createDuration():
    c.execute('''CREATE TABLE time (
    category text,
    duration text
    )''')
    conn.commit()

def dropDuration():
    c.execute('''DROP TABLE time''')
    conn.commit()
    createDuration()

def getCount():
    c.execute("SELECT COUNT(*) FROM activity")
    count = c.fetchone()
    return count[0]

def fetchActivity():
    c = conn.cursor()
    c.execute('''SELECT rowid, * FROM activity ''')
    items = c.fetchall()
    for log in items:
        print(log[0], '\t ', log[1], '\t ', log[2], '\t ', log[3], '\t ', log[4])

def fetchOne(idx):
    c = conn.cursor()
    c.execute(''' SELECT * FROM activity WHERE rowid=?''', (idx,))
    items = c.fetchone()
    return items

def addActivity(start, end, category, note):
    c = conn.cursor()
    start = datetime(date.today().year,date.today().month,date.today().day,int(start[:start.index(":")]),int(start[start.index(":")+1:]))
    end = datetime(date.today().year,date.today().month,date.today().day,int(end[:end.index(":")]),int(end[end.index(":")+1:]))
    c.execute("INSERT INTO activity (start_time, end_time, category, note) VALUES (?,?,?,?)", (start, end, category, note))
    addDuration(start, end, category)
    conn.commit()

def deleteActivity(del_idx):
    c.execute("SELECT * FROM activity WHERE rowid=?", (del_idx,))
    time = c.fetchone()
    print(time)
    print(type(time))
    start = time[0]
    end = time[1]
    category = time[2]
    subtractDuration(start, end, category)
    c.execute("DELETE FROM activity WHERE rowid=?", (del_idx,))
    conn.commit()
    print("Deleted activity")

def editActivity(edit_idx, start, end, category, note):
    c = conn.cursor()
    start = datetime(date.today().year,date.today().month,date.today().day,int(start[:start.index(":")]),int(start[start.index(":")+1:]))
    end = datetime(date.today().year,date.today().month,date.today().day,int(end[:end.index(":")]),int(end[end.index(":")+1:]))

    c.execute('''SELECT * FROM activity WHERE rowid=?''', (edit_idx,))
    item = c.fetchone()

    if item[2] == category:
        print('category has not changed')
    else:
        # category has changed
        print('category changed')
        subtractDuration(item[0], item[1], item[2]) # item needs to be obj. datetime
        addDuration(start, end, category)

    '''
    fetch original row
        if category has changed:
            subtract duration from old category
            add duration to new category
        else (category is same)
            if new end - start == old end - start:
                update values
            else (duration has changed):
                subtract old duration from category
                add new duration to category
    '''

    c.execute("UPDATE activity SET start_time=?, end_time=?, category=?, note=? WHERE rowid=?", (start, end, category, note, edit_idx))
    conn.commit()
    print("Edited activity")

def addDuration(start, end, category):
    c = conn.cursor()
    c.execute('''SELECT DISTINCT(category) from time''')
    items = [i[0] for i in c.fetchall()]
    time = end - start
    
    if category in items:
        print("category already exists\n")
        c.execute('''SELECT * from time WHERE category=?''',(category,))
        item = c.fetchone()

        t = datetime.strptime(item[1], "%H:%M:%S")
        td2 = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        time += td2
        c.execute('''UPDATE time SET duration=? WHERE category=?''', (str(time), category))
    else:
        c.execute('''INSERT INTO time (category, duration) VALUES (?,?)''', (category, str(time)))
        print('Duration inserted sucessfully. ')
    
    conn.commit()

def subtractDuration(start, end, category):
    c = conn.cursor()
    time = end - start

    # fetch current time duration
    c.execute('''SELECT * from time WHERE category=?''',(category,))
    item = c.fetchone()

    # convert string -> datetime object -> timedelta and subtract deleted activity time duration
    t = datetime.strptime(item[1], "%H:%M:%S")
    td2 = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    time = td2 - time

    # update new time duration for category
    c.execute('''UPDATE time SET duration=? WHERE category=?''', (str(time), category))
    conn.commit()

def createMock():
    addActivity('12:00','13:30',"food","this is a note")
    addActivity('13:31','14:00',"study","this is another note")
    addActivity('14:00','15:00',"workout","this is another random note")
    addActivity('15:00','17:00',"food","this is another random note")
    addActivity('17:00','19:00',"study","this is another random note")
    addActivity('19:00','21:00',"game","this is another random note")
    addActivity('21:00','23:00',"study","this is another random note")
    addActivity('23:00','23:59',"prep","this is another random note")


