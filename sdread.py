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
import pandas as pd
import time


#Function for identifying reverse flow events
def rfeFinder(rad,beam,gate,velocity,fov,timeEvent,rsep,rfe):
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

#Function for reading superdarn data and returning rfe matrix
def sdread(rfe,rad,sTime,eTime):
    veltime=True   #Plotting of time diagram over velocities
    vel, t = [], []
    velC=0              #Total number of data elements
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
    
    myScan = pydarn.sdio.radDataReadAll(myPtr)
    
    
    #Iterate thorugh all data from selected time period
    print 'Radars to analyze: '+ str(len(myScan))
    for myBeam in myScan:
        count+=1
        if (myBeam == None): continue
        vel.append( myBeam.fit.v )
        t.append( myBeam.time )
        if not myBeam.fit.v:
            print 'empty'
            continue
        velC=velC+len(myBeam.fit.v)
        
        
        beam=myBeam.bmnum
        gate=array(myBeam.fit.slist)
        velocity=array(myBeam.fit.v)
        rsep=myBeam.prm.rsep
        timeEvent=myBeam.time#int(myBeam.time.strftime("%Y%m%d%H%M"))
        radId=myBeam.stid
        
        site = pydarn.radar.site(radId=radId, dt=myBeam.time)
        fov = pydarn.radar.radFov.fov(site=site, rsep=rsep,
                                          ngates=myBeam.prm.nrang + 1,
                                          nbeams=site.maxbeam,coords='mag',
                                          date_time=myBeam.time)
        
        print '...Analyzing radar '+rad+' beam '+str(beam)#Progress
        print '**Beam ' + str(count) +' out of '+str(len(myScan))+ ' **'+secondsToStr(time.clock()-timerS)
        rfe=rfeFinder(rad,beam,gate,velocity,fov,timeEvent,rsep,rfe)
        
        
    

    
    #Plot velocities as function of the time interval
    if veltime:
        ax = gca()
        for i in range(len(t)):
            if not vel[i]: continue
            plt.scatter([dates.date2num(t[i])]*len(vel[i]), vel[i], s=1)
        plt.ylim([-1000, 1000])
        plt.xlim([dates.date2num(sTime), dates.date2num(eTime)])
        tloc = dates.MinuteLocator(interval=10)
        tfmt = dates.DateFormatter('%H:%M')
        ax.xaxis.set_major_locator(tloc)
        ax.xaxis.set_major_formatter(tfmt)
        plt.ylabel('Velocity [m/s]')
        plt.grid()
        plt.show()
    
    print 'Number of Velocity: ',velC
    print 'Number of RFE: ',len(rfe)-1

    return rfe




