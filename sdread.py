#superDARN data read        Kristian reed 02.08.2016


from davitpy import pydarn
import davitpy.pydarn.sdio
from davitpy.pydarn.plotting import *
from davitpy.utils import *

from secondsToStr import *

import datetime as dt
from pylab import gca
import matplotlib.pyplot as plt
from matplotlib import *
from scipy import *
import time


#Function for identifying reverse flow events
def rfeFinder_old(rad,beam,gate,velocity,fov,timeEvent,rsep,rfe):
    a=100   #Velocity requirements (m/s)
    b=170
    c=170
    for n in range(len(velocity)-3):
        if (velocity[n+1]>a and velocity[n]<-c) or (velocity[n+1]<-a and velocity[n]>c):
            if (velocity[n+2]>b and velocity[n]<-c) or (velocity[n+2]<-b and velocity[n]>c):
                if (velocity[n+3]>c and velocity[n]<-c) or (velocity[n+3]<-c and velocity[n]>c):  #Need 4 gates after each other to count as RFE
                    if gate[n+1]-gate[n]<=1:#Need to be continuus data for rfe
                        gateLe,i=0,0
                        while (abs(velocity[n]-velocity[n+i+1])>300):   #Calculating radial length of RFE
                            if (gate[n+i+1]-gate[n+i]>1): break#Stopping if not continuus
                            if (len(velocity[n+i:])<3): break#Stopping of approaching end
                            gateLe+=1
                            i+=1
                        radLe=gateLe*rsep
                        lat=fov.latCenter[beam, gate[n]]                                        #Finding coordinates
                        lon=fov.lonCenter[beam, gate[n]]
                        relVel=abs(velocity[n+1]-velocity[n])
                        rfe=append(rfe,[[rad,beam,gate[n], relVel,radLe,lat,lon,timeEvent]],axis=0)
    return rfe
    
#Enhanched Function for identifying reverse flow events
def rfeFinder(velMatrix):
    a=100   #Velocity requirements (m/s)
    b=170
    c=170
    
    [cols,rows]=shape(velMatrix)
    
    for i in range(1,rows-1):
        for n in range(cols-3):
            if (velMatrix[n+2,i]>250 and velMatrix[n,i]<-250) or (velMatrix[n+2,i]<-250 and velMatrix[n,i]>250):
                if (abs(velMatrix[n,i]-velMatrix[n+1,i])<200):                  #Check for min 2 gate rfe
                    if (abs(velMatrix[n,i]-velMatrix[n+3,i])>500):              #Check strong gradient drift
                        if  (abs(velMatrix[n,i]-velMatrix[n,i+1])<200 or \
                            abs(velMatrix[n,i]-velMatrix[n+1,i+1])<200) and \
                            (abs(velMatrix[n,i]-velMatrix[n,i-1])<200 or \
                            abs(velMatrix[n,i]-velMatrix[n+1,i-1])<200):        #Check neighbour beam
                             
                             if (abs(velMatrix[n,i]-velMatrix[n+2,i+1])>500 or \
                                abs(velMatrix[n,i]-velMatrix[n+3,i+1])>500) and \
                                (abs(velMatrix[n,i]-velMatrix[n+2,i-1])>500 or \
                                abs(velMatrix[n,i]-velMatrix[n+3,i-1])>500):  
                             
                             
                                return n,i            #Return index of RFE
    return None,None

#Function for reading superdarn data and returning rfe matrix
def sdread(rfe,rad,sTime,eTime):
    timerS=time.clock()
    
   
    #Radar parameters
    channel=None
    bmnum=None
    cp=None
    fileType='fitacf'
    filtered=False
    src=None
    count=0
    
    #Fetching data
    myPtr = pydarn.sdio.radDataOpen(sTime,rad,eTime=eTime,channel=channel,
                                    bmnum=bmnum,cp=cp,fileType=fileType,
                                    filtered=filtered, src=src)
    
    myScan = pydarn.sdio.radDataReadScan(myPtr)
    
    
    #Iterate thorugh all data from selected time period
    while (myScan!=None):
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
    #    plt.imshow(velMatrix,cmap=plt.get_cmap('jet'),interpolation='nearest',aspect='auto')
    #    plt.colorbar()
    #    plt.show()

        
        gate,beam=rfeFinder(velMatrix)#Finding the actual RFE
        
        
        
        if gate is None:
            myScan = pydarn.sdio.radDataReadScan(myPtr)
            continue#If no RFE go to next scan
    
        #Finding position and storing RFE data
        relVel=0
        gateLe=0
        
        rsep=myScan[0].prm.rsep
        radLe=gateLe*rsep
        radId=myScan[0].stid
        site = pydarn.radar.site(radId=radId, dt=timeEvent)
        fov = pydarn.radar.radFov.fov(site=site, rsep=rsep,
                                          ngates=myScan[0].prm.nrang + 1,
                                          nbeams=site.maxbeam,coords='mag',
                                          date_time=timeEvent)
        
        lat=fov.latCenter[beam, gate]                    #Finding coordinates
        lon=fov.lonCenter[beam, gate]

        lonMlt, latMlt = coord_conv(lon, lat, 'mag', 'mlt',
                                    altitude=700.,
                                    date_time=timeEvent)
        lonMlt *= 24./360.      #Convert from degrees to hours
        lonMlt %= 24.           #Convert to 24 hr
        
        rfeElement=array([[rad,beam,gate,relVel,lonMlt,lat,lon,timeEvent]])
        rfe=append(rfe,rfeElement,axis=0)
        
        myScan = pydarn.sdio.radDataReadScan(myPtr)
        
        
    
    print 'Number of RFE: ',len(rfe)-1

    return rfe




