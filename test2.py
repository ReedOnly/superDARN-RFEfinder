import sqlite3 as lite
import sys


con = lite.connect(os.getcwd()+'/omni/imf_database.db')
retrieve=list()
with con:    
    cur = con.cursor()    
    cur.execute("SELECT * FROM IMF_mag")
    data= cur.fetchall()
