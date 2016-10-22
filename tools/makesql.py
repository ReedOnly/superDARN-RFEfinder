#Script for importing .txt file and save as SQL database
import sqlite3 as lite
import sys
import os

#read text file to one list per line
with open(os.getcwd()+'/omni/2015.lst') as input_data:
        imf_rawdata= [map(eval,num.split()) for num in input_data.readlines()]

#Convert list of lists to list of tuples
#for n in range(len(imf_rawdata)): imf_rawdata[n]=tuple(imf_rawdata[n])



#Create .db SQL database for the list
con = lite.connect(os.getcwd()+'/omni/imf_database.db')

with con:

    cur = con.cursor()    
#    cur.execute("DROP TABLE IF EXISTS IMF_mag")
#    cur.execute("CREATE TABLE IMF_mag(Year INT, Day INT, Hour INT, Minute INT,\
#                Bx REAL, By REAL, Bz REAL)")
#    
    cur.executemany("INSERT INTO IMF_mag VALUES(?, ?, ?, ?, ?, ?, ?)", imf_rawdata)