import psycopg2
from psycopg2 import sql
import os
# config.py reads database.ini file and returns the connection parameters as a dictionary.
from config import config

def clearDB():
    # execute sql query file with query() routine
    filename = 'clear.sql'
    query(filename)

def fileToDB(fName, table):
    # this will copy data from tsv file to Database
    try:
        # Take configuration parameters, Connect to database and create a cursor
        params = config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()

        # add full path to the file name
        fName = str(os.getcwd()) + "\\" + fName

        # SQL transaction, use SQL string composition module
        cursor.execute(
            sql.SQL("COPY {} FROM %s encoding 'windows-1251'")
                .format(sql.Identifier(table)),
            [fName,])
        conn.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

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