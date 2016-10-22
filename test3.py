
import sqlite3 as lite
import sys
import time
import random


def get_imf(year,day,hour,minute):
    """Parameters:
    Year: (int)
    day: (int)
    hour: (int)
    minute: (int)
    
    Returns:
    imf[0]:Bx(float)
    imf[1]:By(float)
    imf[2]Bz(float)"""
    

    #Connect to IMF database
    con = lite.connect(os.getcwd()+'/omni/imf_database.db')
    
    with con:
        
        cur = con.cursor()    
        cur.execute("SELECT Bx,By,Bz FROM IMF_mag WHERE Year=:year AND Day=:day\
                    AND Hour=:hour AND Minute=:minute",
                    {"year":year,"day":day,"hour":hour,"minute":minute})
        imf= cur.fetchone()
        
    return imf[0],imf[1],imf[2]
    



timeS=time.clock()
for n in range(10):
    y=random.randint(2012,2015)
    d=random.randint(1,365)
    h=random.randint(0,23)
    m=random.randint(0,59)
    Bx,By,Bz=get_imf(y,d,h,m)
    print Bz

timeEl=time.clock()-timeS
print "Time used: %s"%timeEl


sTime.timetuple().tm_yday