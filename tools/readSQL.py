#Code used for finding RFEs and making the plots used in the Master Theisis of Kristian Reed
#Written by Kristian Reed 10.06.2017


import sqlite3 as lite



"""Parameters:
Year: (int)
day: (int)
hour: (int)
minute: (int)

Returns:
imf[Bx,By,Bz]:(float)"""


#Connect to IMF database
#con = lite.connect('/scratch/sddata/.radars.sqlite')
con = lite.connect('/scratch/superDARN-RFEfinder/omni/imf_database.db')

with con:
    
    cur = con.cursor()    
    cur.execute("SELECT * from IMF_mag")
    hwd= cur.fetchall()
    

for n in range(len(hwd)):
    print hwd[n]



