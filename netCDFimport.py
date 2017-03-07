from scipy import *
import datetime as dt

from netCDF4 import Dataset
 

##DMSP example
#dataset2 = Dataset('./files/rfe2_PS.APL_V0116S024CE0018_SC.U_DI.A_GP.F16-SSUSI_PA.APL-SDR-DISK_DD.20141216_SN.57583-00_DF.NC')
#data2= array(dataset2.variables['DMSP_LATITUDE'])


#Load netCDF file   
dataset = Dataset('./files/rfe2_poes_m02_20141216_proc.nc','r')


elements=dataset.variables.keys()

data=[]
for n in range(len(elements)):
    values=array(dataset.variables[elements[n]])
    data.append(values)

    
#Print different variables
print elements



#Import single variable
#importdata=array(dataset.variables['mep_pro_tel0_cps_p1'])