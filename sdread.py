#Script for searching and plotting RFEs from SuperDARN data
#Usually not nessecary to change this file
#Written by Kristian Reed 10.06.2017

from davitpy import pydarn
import davitpy.pydarn.sdio
from davitpy.pydarn.plotting import *
from davitpy.utils import *
from tools import *
import datetime as dt
from pylab import gca
import matplotlib.pyplot as plt
from matplotlib import *
from scipy import *

#Function for identifying reverse flow events
#def rfeFinder_old(rad,beam,gate,velocity,fov,timeEvent,rsep,rfe):
#    a=100   #Velocity requirements (m/s)
#    b=170
#    c=170
#    for n in range(len(velocity)-3):
#        if (velocity[n+1]>a and velocity[n]<-c) or (velocity[n+1]<-a and velocity[n]>c):
#            if (velocity[n+2]>b and velocity[n]<-c) or (velocity[n+2]<-b and velocity[n]>c):
#                if (velocity[n+3]>c and velocity[n]<-c) or (velocity[n+3]<-c and velocity[n]>c):  #Need 4 gates after each other to count as RFE
#                    if gate[n+1]-gate[n]<=1:#Need to be continuus data for rfe
#                        gateLe,i=0,0
#                        while (abs(velocity[n]-velocity[n+i+1])>300):   #Calculating radial length of RFE
#                            if (gate[n+i+1]-gate[n+i]>1): break#Stopping if not continuus
#                            if (len(velocity[n+i:])<3): break#Stopping of approaching end
#                            gateLe+=1
#                            i+=1
#                        radLe=gateLe*rsep
#                        lat=fov.latCenter[beam, gate[n]]                                        #Finding coordinates
#                        lon=fov.lonCenter[beam, gate[n]]
#                        relVel=abs(velocity[n+1]-velocity[n])
#                        rfe=append(rfe,[[rad,beam,gate[n], relVel,radLe,lat,lon,timeEvent]],axis=0)
#    return rfe
#    
#Enhanched Function for identifying reverse flow events
def rfeFinder(velMatrix):

    
    [cols,rows]=shape(velMatrix)
    
    for i in range(1,rows-1):
        for n in range(cols-3):
            if (velMatrix[n+2,i]>250 and velMatrix[n,i]<-250) or (velMatrix[n+2,i]<-250 and velMatrix[n,i]>250):
                if (abs(velMatrix[n,i]-velMatrix[n+1,i])<200):#200                  #Check for min 2 gate rfe
                    if (abs(velMatrix[n,i]-velMatrix[n+3,i])>500): #500             #Check strong gradient drift
                        if  (abs(velMatrix[n,i]-velMatrix[n,i+1])<200 or \
                            abs(velMatrix[n,i]-velMatrix[n+1,i+1])<200) and \
                            (abs(velMatrix[n,i]-velMatrix[n,i-1])<200 or \
                            abs(velMatrix[n,i]-velMatrix[n+1,i-1])<200):        #Check 2 neighbour beam
                             
                             if (abs(velMatrix[n,i]-velMatrix[n+2,i+1])>500 or \
                                abs(velMatrix[n,i]-velMatrix[n+3,i+1])>500) and \
                                (abs(velMatrix[n,i]-velMatrix[n+2,i-1])>500 or \
                                abs(velMatrix[n,i]-velMatrix[n+3,i-1])>500):  
                             
                             
                                return n,i            #Return index of RFE
    return None,None

#Function for reading superdarn data and returning rfe matrix
def sdread(rfe,rad,sTime,eTime):
    
   
    #Radar parameters
    channel=None
    bmnum=None
    cp=None
    fileType='fitex'
    filtered=False
    src=None
    
    #Fetching data
    myPtr = pydarn.sdio.radDataOpen(sTime,rad,eTime=eTime,channel=channel,
                                    bmnum=bmnum,cp=cp,fileType=fileType,
                                    filtered=filtered, src=src)
    
    #Starting scan at first beam, and then until next time same beam comes
    myScan=myPtr.readScan(firstBeam=0,useEvery=1,showBeams=True)
    
    #myScan = pydarn.sdio.radDataReadScan(myPtr)
    
    
    #Iterate thorugh all data from selected time period
    nscans=1
    while (myScan!=None):
        #Counting analyzed scans
        nscans=nscans+1
        timeEvent=myScan[0].time#Time for first beam in scan
        print '...Analyzing radar '+rad+' at time: '+str(timeEvent)
        nbeams=max(len(myScan),16)#number of beams          Rows
        nrangs=max(myScan[0].prm.nrang,100)#Number of gates  Cols (Minimum 100x16 matrix)
        
        velMatrix=zeros((nrangs,nbeams))
        
        for n in range(len(myScan)):  #Iterate through all beams to add velocities
            beam=myScan[n].bmnum
            gates=array(myScan[n].fit.slist)
            #if not myScan[beam].fit.v: print 'empty beam';continue
            velocity=array(myScan[n].fit.v)
            
            for gate in range(len(gates)):
                velMatrix[gates[gate],beam]=velocity[gate]
    
        velMatrix[velMatrix>1200]=1200              #High pass filter for noise
        velMatrix[velMatrix<-1200]=-1200
        
        gate,beam=rfeFinder(velMatrix)#Finding the actual RFE
        
        if gate is None:
            #myScan = pydarn.sdio.radDataReadScan(myPtr)
            myScan=myPtr.readScan(firstBeam=0,useEvery=1,showBeams=True)
            continue#If no RFE go to next scan
    
        utc=myScan[beam].time#time where the actal rfe happened
        #Finding mag position
        rsep=myScan[0].prm.rsep
        radId=myScan[0].stid
        site = pydarn.radar.site(radId=radId, dt=utc)
        fov = pydarn.radar.radFov.fov(site=site, rsep=rsep,
                                          ngates=myScan[0].prm.nrang + 20,  #+20 in case some beams are larger
                                          nbeams=site.maxbeam,coords='mag',
                                          date_time=utc)
        lat=fov.latCenter[beam, gate]
        lon=fov.lonCenter[beam, gate]

        #Calculate MLT
        lonMlt, latMlt = coord_conv(lon, lat, 'mag', 'mlt',
                                    altitude=300.,
                                    date_time=utc)
        MLT=lonMlt * 24./360.      #Convert from degrees to hours
        MLT %= 24.           #Convert to 24 hr
        
###########        
#        #Sorting for MLT and range
#        if not (8 < MLT < 16):
#            myScan=myPtr.readScan(firstBeam=0,useEvery=1,showBeams=True)
#            continue     #Sort out for newly opened flux
#        if gate < 20:
#            myScan=myPtr.readScan(firstBeam=0,useEvery=1,showBeams=True)
#            continue              # Skip the first 600 km (38 for pyk, 30 for han)
        
            
            
            #Get IMF magnetic field from database
        imfAve=array([[0,0,0]])
        for n in range(-10,6):          #Making average from -15 to +6 min
            utcTmp=utc
            utcTmp=utcTmp + dt.timedelta(minutes=n)
            imfTmp=array([get_imf(utcTmp)])
            if not (imfTmp[0,0]==50):
                imfAve=append(imfAve,imfTmp,axis=0)
        imfAve=delete(imfAve,0,axis=0)
        if len(imfAve)<1: imf=[0,0,0]
        else:
            imf=[average(imfAve[:,0]),average(imfAve[:,1]),average(imfAve[:,2])]
        
            for a in range(3):
                #if abs(imfAve[:,a].max()-imfAve[:,a].min())>5:imf[a]='ls'       #mark large spread of > 5
                if imfAve[:,a].max()>0 and imfAve[:,a].min()<0: imf[a]='pm' #mark if imf change from negative to positive
            

        #Normal get IMF function
        imf=get_imf(utc)

        rfeElement=array([[rad,beam,gate,lonMlt,MLT,lat,lon,imf,timeEvent]])
        rfe=append(rfe,rfeElement,axis=0)
        
        #myScan = pydarn.sdio.radDataReadScan(myPtr)
        myScan=myPtr.readScan(firstBeam=0,useEvery=1,showBeams=True)        
        
    print 'number of analyzed scans: ', nscans
    print 'Number of RFE: ',len(rfe)-1,' ---> ', float(len(rfe)-1)/float(nscans)*100.0, '%'

    return rfe




