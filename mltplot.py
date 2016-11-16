import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec
import os


def mltplot(newpath,sTime,eTime,radars,mlat,mlt):
    #http://stackoverflow.com/questions/36061537/polar-plots-with-magnetic-local-time0-23-as-the-azimuth-against-magnetic-latit
    # set up random data between 0 and 90
    
    fig = plt.figure(figsize=(8, 6)) 
    st=fig.suptitle(str(radars)+' from '+sTime.strftime("%Y.%m.%d %H:%M")+' until '+ eTime.strftime("%H:%M UTC"),fontsize="x-large")
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1]) 
    r = mlat#[np.random.random() * 90.0 for i in range(0,10)]
    
    # set up 24 hours matching the random data above
    hours = np.linspace(0.0,24.0,len(r))
    # scaling the 24 hours to the full circle, 2pi
    theta = hours / 24.0 * (2.0 * np.pi)
    
    # reverse your data, so that 90 becomes 0:
    r_rev = [(ri - 90.0) * -1.0 for ri in r]
    
    # set up your polar plot
    fig1 = plt.subplot(gs[0], projection='polar')
    fig1.scatter(theta, r_rev, color='r', linewidth=0.1)
    
    # define your axis limits
    fig1.set_ylim([0.0, 30.0])
    
    # statically reverse your y-tick-labels
    # caution: this turns your labels into strings
    #          and decouples them from the data
    # 
    # the np.linspace gives you a distribution between 90 and 0 -
    # the number of increments are related to the number of ticks
    # however, you require one more label, because the center is 
    #     omitted.  
    fig1.set_yticklabels(['{:.0f}'.format(ylabel) \
                    for ylabel in np.linspace(90.0,70.0,len(fig1.get_yticklabels())+1)[1:]])
    
    
    # statically turn your x-tick-labels into fractions of 24
    # caution: this turns your labels into strings
    #          and decouples them from the data
    #
    # the number of ticks around the polar plot is used to derive
    #    the appropriate increment for the 24 hours
    fig1.set_xticklabels(['{:.1f}'.format(xlabel) \
                        for xlabel in np.arange(0.0,24.0,(24.0 / len(fig1.get_xticklabels())))])
    
    fig1.grid(True)
    
    fig2=plt.subplot(gs[1])
    plt.scatter(mlt,mlat,color='r', linewidth=0.1)
    plt.axis([0, 24, 70, 90])
    plt.xlabel('Magnetic local time')
    plt.ylabel('Magnetic latitude')
    plt.title('Polar MLT distribution')
    fig2.grid(True)
    
    plt.show()
    fig.savefig(newpath+"/MLTpolar.png",dpi=500)
    

#mlat=array(rfe[:,5],dtype=float)
#mlt=array(rfe[:,4],dtype=float)
#mltplot(mlat,mlt)

