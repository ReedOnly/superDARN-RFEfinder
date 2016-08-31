#Plot superDARN fan plot Kristian Reed 10.08.2016


import os

from scipy import *
from fanRfe import *
from secondsToStr import *
import time



start=time.clock()

rfe=load(os.getcwd()+'/Files/2016-08-15-20.30/2014-12-15-0730.npy')

newpath=(os.getcwd()+'/Files/')
plotFanRfe(rfe[187,6],rfe[187,5],newpath,rfe[187,7],[rfe[187,0]], param='velocity',interval=60, fileType='fitacf',
                                scale=[-500,500],coords='mag',gsct=False,fill=True,
                                show=True, png=True,pdf=False,dpi=300)

end=time.clock()
print secondsToStr(end-start)