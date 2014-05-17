#!/usr/bin/env python
import psycopg2
from app import helper, db
from app.models import *
from pprint import pprint
import sys
import requests
from sqlalchemy import or_
from datetime import datetime
from app.helper import makeSlug

geoUrl = "https://maps.googleapis.com/maps/api/geocode/json?"

def createCodeDct():
    ### dict of code:badgeName KV pair from csv###
    badge_list = {}
    with open('tmp/csv/badges.csv','r') as badges:
        i = 1
        for line in badges:
            badge_list.setdefault(i,line.encode('utf-8'))
            i+=1
    return badge_list

def addNewBadges(codeDct):
    ###adds any badges from csv not already in badge table ie. {2:'Contamination'}### 
    for k in codeDct:
        if not Badge.query.filter_by(code=k).first():
            db.session.add(Badge(k,codeDct[k]))
    db.session.commit()

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
'--------------------------------------------------------------------------------------------------------------------------------------------------------------'    

def main():
    
    args = sys.argv[1:]
    
    if not args:
        print "Use '--help' flag for functions"
    else:    
        arg = args[0]
        if len(args) > 1: 
            geolimit = args[1]
        else:
            geolimit = False
        
        if arg == '--help':
            print("usage:\n" 
                  "[-m             -->   Fill Rest,Comment tables from CSV]\n"
                  "[-b             -->  Fill Badge tables from CSV]\n"
                  "[-geo [limit]   --> Fill Lat/Lng cols in Rest table]\n"
                  "[-Dm            -->   Delete main tables]\n"
                  "[-Db            -->  Delete badg tables]\n")
            sys.exit(1) 
        else: 
            if arg == '-m': addtodb()
            elif arg == '-b': addNewBadges(createCodeDct())           
            elif arg == '-geo': 
                if not geolimit: 
                    geoCodedb()
                else:
                    geoCodedb(int(geolimit))
                     
            elif arg == '-Dm': deletefromdb()
            elif arg == '-Db': deletebadges()
     
            else: print 'not a valid flag'
         
    sys.exit(1)
        
if __name__ == "__main__":
    main()
    



