#!/usr/bin/env python
import psycopg2
from app import helper, db
from app.models import *
from pprint import pprint



def addtodb():
   ###Copies CSV files to create resturant and comment tables.  Creates badge table using 'create_badge_list' helper fct###
    print 'copying restuarant and comment tables'
     
    conn = psycopg2.connect("dbname=foodo user=blake password=bloopers")
    cur = conn.cursor()
    copyit = "BEGIN; ALTER TABLE rest DISABLE TRIGGER ALL; ALTER TABLE comment DISABLE TRIGGER ALL; COPY rest (name,street,zipcd) FROM '/home/blake/blakedev/Practice/flaskwork/foodo/tmp/rest_tbl.csv' DELIMITER ',' CSV; COPY comment (restnm,date,code,quote) FROM '/home/blake/blakedev/Practice/flaskwork/foodo/tmp/comment_tbl.csv' DELIMITER ',' CSV; COMMIT;"
    cur.execute(copyit)
    conn.commit()
    cur.close()
    conn.close()

def create_badge_list():
    badge_list = {}
    with open('tmp/badges.csv','r') as badges:
        i = 1
        for line in badges:
            badge_list.setdefault(i,line.encode('utf-8'))
            i+=1
    return badge_list

def make_badges():
    print 'Making badge dict'
    
    code_dct = create_badge_list() 
    
    for k in code_dct:
        if not Badge.query.filter_by(code=k).first():
            db.session.add(Badge(k,code_dct[k]))
    db.session.commit()
            
    
if __name__ == "__main__":
#     addtodb()
    make_badges()



