from scipy import *
import datetime as dt
from tools import *

from netCDF4 import Dataset
from scipy.io import netcdf
 

##DMSP example
#dataset2 = Dataset('./files/rfe2_PS.APL_V0116S024CE0018_SC.U_DI.A_GP.F16-SSUSI_PA.APL-SDR-DISK_DD.20141216_SN.57583-00_DF.NC')
#data2= array(dataset2.variables['DMSP_LATITUDE'])

#   './files/rfe2_poes_m02_20141216_raw.nc'
dataset = Dataset('./files/rfe2_PS.APL_V0116S024CE0018_SC.U_DI.A_GP.F16-SSUSI_PA.APL-SDR-DISK_DD.20141216_SN.57583-00_DF.NC')


var=dataset.variables.keys()

data=[]
for n in range(len(var)):
    values=array(dataset.variables[var[n]])
    data.append(values)

    
    
print var




