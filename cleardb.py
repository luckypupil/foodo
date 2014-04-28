#!/usr/bin/env python
import psycopg2
from app import helper, db
from app.models import *
from pprint import pprint



def deletefromdb():
   ###Delete comment and rest tables### 
    print "Deleting comment and rest tables"
    conn = psycopg2.connect("dbname=foodo user=blake password=bloopers")
    cur = conn.cursor()
    delete = "BEGIN; DELETE FROM rest; DELETE FROM comment; COMMIT;"
    cur.execute(delete)
    conn.commit()
    cur.close()
    conn.close()
    
def deletebadges():    
    print "Deleting badge table"
    conn = psycopg2.connect("dbname=foodo user=blake password=bloopers")
    cur = conn.cursor()
    cur.execute('DELETE FROM badge')
    conn.commit()
    cur.close()
    conn.close()
            
        
    
    
if __name__ == "__main__":
    deletefromdb()
    deletebadges()



