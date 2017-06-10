Code used for finding RFEs and making the plots used in the Master Theisis of Kristian Reed
Written by Kristian Reed 10.06.2017


**THIS CODE COMES WITHOUT ANY WARRANTY**

PS: All the source code is included here, but in order to make DMSP, SWARM, and OMNI data for SuperDARN plots several additional files need to be downloaded.
If you have any questions about the code attached, feel free to contact me at kristian_reed@yahoo.no

Written by Kristian reed 10.06.2017



List of files:		Description:

fanRfe.py		Make custom scan plots of RFEs
singleplot.py		Make plot of single date and time
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
imf_database.db		IMF database for 2014-2016 needed to make plots
makesql.py		script to compile .sql database from .lst file
omni_header.txt		Description of .lst files
2017.lst		example of .lst textfile downloaded from https://omniweb.gsfc.nasa.gov/form/omni_min.html


files/sample/:		Example of RFE search scan from LYR radar
