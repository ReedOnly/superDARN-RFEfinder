#superDARN rfe plotter        Kristian reed 09.08.2016

#Script for cobining two or more .npy rfe lists for making one overview plot
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
from davitpy import pydarn
import davitpy.pydarn.sdio
from davitpy.pydarn.plotting import *
from davitpy.utils import *

import os
import sys
sys.path.append('../..')
sys.path.append('../')
import datetime as dt

import matplotlib.pyplot as plt
from matplotlib import *
from scipy import *
import pandas as pd

from sdread import *
from secondsToStr import *
from fanRfe import *
import time




SaveXlsx=True      #Save as .xlsx spreadsheet
SaveNpy=True        #Save as .npy file
RFEplot=True        #Make RFE plot

timerS=time.clock()

#Make path for storage

newpath=os.getcwd()+'/'+datetime.datetime.now().strftime("%Y-%m-%d-%H.%M/")

if not os.path.exists(newpath):
	os.makedirs(newpath)

#Loading stored file
rfe1=load(os.getcwd()+'/data1.npy')
rfe2=load(os.getcwd()+'/data2.npy')
#rfe3=load(os.getcwd()+'/data1.npy')


        
rfe=append(rfe1,rfe2,axis=0)    #Merge the two lists of rfe together
        
pandasRfe=pd.DataFrame(rfe,columns=['Site','Beam','Gate','RelVel','RadLength','Lat(mag)','Lon(mag)','Time'])
        
    
#Output result
print pandasRfe[['Time','Site','Beam','Gate','RelVel','RadLength']]




#Creating map with RFE
if RFEplot:
    plt.figure(figsize=(9,9))
    plt.title(str(radars)+' from '+sTime.strftime("%Y.%m.%d %H:%M")+' until '+ eTime.strftime("%H:%M UTC"),fontsize="x-large")
    width = 111e3*60
    m = plotUtils.mapObj(width=width, height=width, lat_0=90., lon_0=60, coords='mag')
    # Plotting some radars
    overlayRadar(m, fontSize=12, codes=['inv','rkn','cly'])
    # Plot radar fov
    overlayFov(m, codes=['inv','rkn','cly'], maxGate=70, beams=[])#0,6,11,12,13,15
    #Add RFE points
    for i in range(len(rfe)):
        #Coordinates in map projection
        x,y=m(rfe[i,6],rfe[i,5])
        #x,y=lon,lat
        m.scatter(x, y, s=50, marker='o', facecolors='none', edgecolors='r', zorder=2)
    
    pylab.savefig(newpath+str(sTime.strftime("%Y-%m-%d-%H%M.png")))
    print 'Saved rfe plot'
    #plt.show()
    
    #Make MLT plot
    mlat=array(rfe[:,5],dtype=float)
    mlt=array(rfe[:,4],dtype=float)
    mltplot(newpath,sTime,eTime,radars,mlat,mlt)
    


#Produce .npy file
if SaveNpy:
    save(newpath+str(rfe[0,7].strftime("%Y-%m-%d-%H%M.npy")),rfe)
    print 'Saved .npy file'
    
#Produce .xlsx file
if SaveXlsx:
    pandasRfe.to_excel(newpath+str(rfe[0,7].strftime("%Y-%m-%d-%H.xlsx")))
    print 'Saved .xlsx file'




    
timerE=time.clock()
print 'Total time used: '+secondsToStr(timerE-timerS)
    
    
#shalala
