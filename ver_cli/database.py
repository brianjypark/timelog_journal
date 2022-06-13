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
    createTable()
    conn.commit()

def addActivity(start, end, category, note):
    c = conn.cursor()
    start = datetime(date.today().year,date.today().month,date.today().day,int(start[:start.index(":")]),int(start[start.index(":")+1:]))
    end = datetime(date.today().year,date.today().month,date.today().day,int(end[:end.index(":")]),int(end[end.index(":")+1:]))
    c.execute("INSERT INTO activity (start_time, end_time, category, note) VALUES (?,?,?,?)", (start, end, category, note))
    conn.commit()
    addDuration(start, end, category)

def editActivity(edit_idx, start, end, category, note):
    c = conn.cursor()
    start = datetime(date.today().year,date.today().month,date.today().day,int(start[:start.index(":")]),int(start[start.index(":")+1:]))
    end = datetime(date.today().year,date.today().month,date.today().day,int(end[:end.index(":")]),int(end[end.index(":")+1:]))

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

def deleteActivity(del_idx):
    # c.execute("SELECT * FROM activity WHERE rowid=?", (del_idx))
    # time = c.fetchall()

    
    c.execute("DELETE FROM activity WHERE rowid=?", (del_idx,))
    conn.commit()
    ''' 
    fetch row to be deleted
        subtract duration from duration table with same category
    '''

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
        print(log[0], '\t ', log[1], '\t ', log[2], '\t ', log[3], '\t ', log[4])

def fetchOne(idx):
    c = conn.cursor()
    c.execute(''' SELECT * FROM activity WHERE rowid=?''', (idx,))
    items = c.fetchone()
    return items

def createDuration():

    c.execute('''CREATE TABLE time (
    category text,
    duration text
    )''')
    conn.commit()

def dropDuration():
    c.execute('''DROP TABLE time''')
    conn.commit()

def addDuration(start, end, category):
    c = conn.cursor()
    c.execute('''SELECT DISTINCT(category) from time''')
    items = [i[0] for i in c.fetchall()]
    time = end - start
    
    if category in items:
        print("category already exists\n")
        c.execute('''SELECT * from time WHERE category=?''',(category,))
        item = c.fetchall()

        print(item)
        print(item[0][1])
        print(type(item[0][1]))

        t = datetime.strptime(item[0][1], "%H:%M:%S")
        td2 = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

        print("****************")
        print(t)
        print(type(t))

        print(td2)
        print(type(td2))
        print("*****************")

        time += td2
        c.execute('''UPDATE time SET duration=? WHERE category=?''', (str(time), category))

    else:
        # add new row with category, duration
        c.execute('''INSERT INTO time (category, duration) VALUES (?,?)''', (category, str(time)))
        print('Duration inserted sucessfully. ')
    
    conn.commit()

def editDuration():
    # TO_DO
    pass

def subtractDuration(start, end, category):
    # TO_DO
    pass



