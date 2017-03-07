# -*- coding: utf-8 -*-

# for python 2/3 compatibility
from __future__ import division, print_function

# import the module
import nompy

# we also need the Python built-in datetime class to specity date and time
import datetime as dt

# we use matplotlib for plotting
import matplotlib.pyplot as plt

# set the date
start = dt.datetime(2014, 12, 16, 0,8 )
end = dt.datetime(2014, 12, 16, 0, 58)

# as an example, let's add a line at these times
line1_at = dt.datetime(2014, 12, 16, 0, 38)
#line2_at = dt.datetime(2013, 11, 3, 16, 0)

# and a span between these times
span1_start = dt.datetime(2014, 12, 16, 0, 33)
span1_end = dt.datetime(2014, 12, 16, 0, 43)
#span2_start = dt.datetime(2013, 11, 3, 20, 0)
#span2_end = dt.datetime(2013, 11, 3, 21, 0)

#===========================================================================================
# Plot 1: Quick and dirty plotting just to check the solar wind and geomagnetic conditions
#===========================================================================================

#nompy.sw_overview(start, end, vline=[line1_at], vspan=[(span1_start, span1_end)])

#==============================================================================
# Plot 2: Get data and plot
#==============================================================================

# The parameter IDs are displayed if you run help on the get_params() function.
# It might not be displayed properly in IDEs, but you can always see the list in
# the nompy source file (at the top of core.py).

# Let's get the Bz GSM (ID 18) and Vx (ID 22), both 1min and 5min data
# (note that we get 1min data by supplying "min", not "1min")
data_1min = nompy.get_params(start, end, [14,17,18, 22,25,26,27], 'min')
data_5min = nompy.get_params(start, end, [18, 22], '5min')

# data is now a Pandas DataFrame containing the columns 'Bz GSM' and 'Vx'.

# let's plot
figure, axes = plt.subplots(2, 1, figsize=(10, 5))

axes[0].plot(data_1min['Bx'].index, data_1min['Bx'])
axes[0].plot(data_1min['Bz GSM'].index, data_1min['Bz GSM'])
#axes[0].plot(data_5min['Bz GSM'].index, data_5min['Bz GSM'])
axes[0].plot(data_1min['By GSM'].index, data_1min['By GSM'])
axes[0].set_title('OMNI IMF [nT]')
axes[0].legend(['Bx','By','Bz'], loc='lower left')

axes[1].plot(data_1min['Vx'].index, data_1min['Vx'])
axes[1].plot(data_5min['Vx'].index, data_5min['Vx'])
axes[1].set_title('Vx [km/s]')
axes[1].legend(['1min', '5min'], loc='lower left')


#axes[2].plot(data_1min['Temp'].index, data_1min['Temp'])
#axes[2].set_title('Temperature')
#axes[2].legend(['Temp'], loc='lower left')

plt.savefig('./IMFomni.png', dpi=300)