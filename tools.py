#Kristian Reed 22.10.2016
#Various fuctions nessecary for things to work

import sqlite3 as lite
import os
from scipy import *
import datetime as dt

def secondsToStr(t):
#return seconds to hh:mm:ss.sss string
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])



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
        
    return imf
    
    
def satorbit(filename):
    """Parameters:
    filename:(string)
    
    Returns:
    lat:float array
    lon:float array
    time: dt.datetime list"""
    
    
    with open(filename, "r") as ins:
        indata = []
        for line in ins:
            line=line.split()
            indata.append(line)
        ins.close()
    
    indata=array(indata)
    lat=array(indata[:,3],dtype='float32')
    lon=array(indata[:,4],dtype='float32')
    
    time=[]
    for n in range(len(indata)):
        tid= dt.datetime.strptime(indata[n,0]+' '+indata[n,1], "%d/%m/%y %H:%M:%S")
        time.append(tid)
        
    return lat, lon, time
