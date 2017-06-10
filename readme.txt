Code used for finding RFEs and making the plots used in the Master Theisis of Kristian Reed
Written by Kristian Reed 10.06.2017


**THIS CODE COMES WITHOUT ANY WARRANTY**

PS: All the source code is included here, but in order to make DMSP, SWARM, and OMNI data for SuperDARN plots several additional files need to be downloaded.
If you have any questions about the code attached, feel free to contact me at kristian_reed@yahoo.no

Written by Kristian reed 10.06.2017



List of files:		Description:

allRadars.py		Plotting vectors of all SuperDARN available		
commands.txt		GitHub commands
dmspPlot_11.py		DMSP data and ground plot
dmspPlot_14.py		DMSP data and ground plot
dmspPlot_19.py		DMSP data and ground plot
dmspPlot_20.py		DMSP data and ground plot
dmspPlot_21.py		DMSP data and ground plot
dmspPlot_24.py		DMSP data and ground plot
dmspPlot_28a.py		DMSP data and ground plot
dmspPlot_28.py		DMSP data and ground plot
dmspPlot_2.py		DMSP data and ground plot
dmspPlot_31.py		DMSP data and ground plot
dmspPlot_36.py		DMSP data and ground plot
dmspPlot_38.py		DMSP data and ground plot
dmspPlot_39.py		DMSP data and ground plot
dmspPlot_40.py		DMSP data and ground plot
dmspPlot_42.py		DMSP data and ground plot
dmspPlot_45.py		DMSP data and ground plot
dmspPlot_46.py		DMSP data and ground plot
dmspPlot.py		DMSP data and ground plot
fanRfe.py		Make custom scan plots of RFEs
readme.txt		This file
mltplot.py		Enhanced polar RFE distribution plot
mltplotClock.py		Clock angle RFE distribution plot
mltplot_old.py		Original polar RFE distribution plot
netCDFimport.py		Read netCDF files
omniIMF.py		Enhanced OMNI plots
omniIMF_old.py		Original OMNI plots
plotRfeMaster.py	Make plots of all RFEs from database
plotRFE.py		Search RFEs from list of times
rfeDistribution.py	Make time duration plot
singleplot.py		Make plot of single date and time
swarm_rfe28.py		SWARM FAC plot
swarm_rfe2.py		SWARM FAC plot


Files needed for search alogirithm for RFEs:

rfefinder.py		Interface for choosing time, radar and output
sdread.py		Actual code for fetching and analyzing for RFEs
tools.py		Files needed for rfefinder.py and sdread.py


tools folder:

fanPlotter.py		Plot leftover scans after RFE search
mergeFiles.py		Merge .npy files together
readSQL.py		manually read .sql database
script.sh		bash script for running python loop


omni folder:
imf_database.db		IMF database needed to make plots
makesql.py		script to compile .sql database from .lst file
omni_header.txt		Description of .lst files
2017.lst		example of .lst textfile downloaded from https://omniweb.gsfc.nasa.gov/form/omni_min.html


files/sample/:		Example of RFE search scan from LYR radar
