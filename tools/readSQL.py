
import sqlite3 as lite
import sys
import time
import random
import os



"""Parameters:
Year: (int)
day: (int)
hour: (int)
minute: (int)

Returns:
imf[Bx,By,Bz]:(float)"""


#Connect to IMF database
con = lite.connect('/scratch/sddata/.radars.sqlite')

with con:
    
    cur = con.cursor()    
    cur.execute("SELECT * from hdw")
    hwd= cur.fetchall()
    

for n in range(len(hwd)):
    print hwd[n]



