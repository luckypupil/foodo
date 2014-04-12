#!/usr/bin/env python

import psycopg2

def addtodb():
    conn = psycopg2.connect("dbname=foodo user=blake password=bloopers")

    cur = conn.cursor()


    copyit = "BEGIN; ALTER TABLE rest DISABLE TRIGGER ALL; ALTER TABLE comment DISABLE TRIGGER ALL; COPY rest (name,street,zipcd) FROM '/home/blake/blakedev/Practice/flaskwork/foodo/tmp/rest_tbl.csv' DELIMITER ',' CSV; COPY comment (restnm,date,code,quote) FROM '/home/blake/blakedev/Practice/flaskwork/foodo/tmp/comment_tbl.csv' DELIMITER ',' CSV; COMMIT;"

    cur.execute(copyit)

    conn.commit()
    cur.close()
    conn.close()
    
if __name__ == "__main__":
    addtodb()



