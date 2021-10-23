import psycopg2
from config import config

def clearDB():
    # execute sql query file with query() routine
    filename = 'clear.sql'
    query(filename)

def insertDB(city, rubric, date, eventId, eventName):
    try:
        # Take configuration parameters, Connect to database and create a cursor
        params = config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()

        # insert into event table but once
        cursor.execute('SELECT id FROM events WHERE id = %s', [eventId])
        records = cursor.fetchall()
        if len(records) < 1:
            query = 'INSERT INTO events (id, name, city) VALUES (%s, %s, %s)'
            val = (eventId, eventName, city)
            cursor.execute(query, val)
            #print("Insert events")

        # insert into dates table, prevent dublicates
        cursor.execute('SELECT * FROM dates WHERE event_id = %s AND date = %s', [eventId, date])
        records = cursor.fetchall()
        if len(records) < 1:        
            query = 'INSERT INTO dates (event_id, date) VALUES (%s, %s)'
            val = (eventId, date)
            cursor.execute(query, val)
            #print("Insert dates")

        # insert into rubrics, prevent dublicates
        cursor.execute('SELECT * FROM rubrics WHERE event_id = %s AND rubric = %s', [eventId, rubric])
        records = cursor.fetchall()
        if len(records) < 1:
            query = 'INSERT INTO rubrics (event_id, rubric) VALUES (%s, %s)'
            val = (eventId, rubric)
            cursor.execute(query, val)
            #print("Insert rubrics")

        conn.commit()
        cursor.close()
        #print("Insert DONE")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print("DB connection closed")

def query(filename):
    try:
        print("clearing DB")
        # Take configuration parameters, Connect to database and create a cursor
        params = config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()

        # read sql query from file
        f = open(filename, 'r')
        query = " ".join(f.readlines())
        # execute
        cursor.execute(query)
        conn.commit()
        cursor.close()
        print("Clearing DONE")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print("DB connection closed")