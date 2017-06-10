#Code used for finding RFEs and making the plots used in the Master Theisis of Kristian Reed
#Written by Kristian Reed 10.06.2017

##See line 462!!#Kristian Reed 14.08.2016

"""The fan module

Module generating fan plots

Methods
-----------------------------------------
plotFan     plot a scan of data
overlayFan  plot a scan of data on a map
-----------------------------------------

"""
from davitpy import utils
import numpy
import math
import matplotlib
import matplotlib.colors as colors
import calendar
import pylab
import matplotlib.pyplot as plot
import matplotlib.lines as lines
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as patches
from matplotlib.collections import PolyCollection, LineCollection
from matplotlib.figure import Figure
import matplotlib.cm as cm
from matplotlib.backends.backend_agg import FigureCanvasAgg
from mpl_toolkits.basemap import Basemap, pyproj
from davitpy.utils.timeUtils import *
from davitpy.pydarn.sdio.radDataRead import *
import davitpy.pydarn.plotting.plotMapGrd
import logging


def plotFanRfe(lon,lat,newpath, imf, sTime, rad, interval=60, fileType='fitex', param='velocity',
            filtered=False, scale=[], channel=None, coords='geo',
            colors='lasse', gsct=False, fov=True, edgeColors='face',
            lowGray=False, fill=True, velscl=1000., legend=True,
            overlayPoes=False, poesparam='ted', poesMin=-3., poesMax=0.5,
            poesLabel=r"Total Log Energy Flux [ergs cm$^{-2}$ s$^{-1}$]",
            overlayBnd=False, show=True, png=False, pdf=False, dpi=500,
            tFreqBands=[]):
    """A function to make a fan plot

    Parameters
    ----------
    sTime : datetime
        The start time you want to plot
    rad
        A list of 3 letter radar codes, e.g. ['bks'], e.g. ['bks','wal','gbr']
    interval : Optional[int]
        The the time period to be plotted, in seconds.  default = 60
    fileType : Optional[str]
        The file type to plot, valid inputs are 'fitex','fitacf', 'lmfit'.
        default = 'fitex'
    param : Optional[str]
        The parameter to be plotted, valid inputs are 'velocity', 'power',
        'width', 'elevation', 'phi0'.  default = 'velocity'
    filtered : Optional[boolean]
        A flag indicating whether the data should be boxcar filtered.
        default = False
    scale : Optional[list]
        The min and max values of the color scale, i.e. [min,max].  If this is
        set to [], then default values will be used
    channel : Optional[char]
        The channel for which to plot data.  default = 'a'
    coords : Optional[str]
        The coordinate system to use; valid inputs are anything handled by
        coord_conv (see davitpy.utils.get_coord_dict).  Default:  geo
    colors : Optional[str]
        The color map to use, valid inputs are 'lasse', 'aj'.
        default = 'lasse'
    gsct : Optional[boolean]
        A flag indicating whether to plot ground scatter as gray.
        default = False
    fov : Optional[boolean]
        A flag indicating whether to overplot the radar fields of view.
        default = True
    edgeColors : Optional[str]
        Edge colors of the polygons, default = 'face'
    lowGray : Optional[boolean]
        A flag indicating whether to plot low velocities in gray.
        default = False
    fill : Optional[boolean]
        A flag indicating whether to plot filled or point RB cells.
        default = True
    velscl : Optional[float]
        The velocity to use as baseline for velocity vector length, only
        applicable if fill = 0.  default = 1000
    legend : Optional[boolean]
        A flag indicating whether to plot the legend, only applicable if
        fill = 0.  default = True
    overlayPoes : Optional[boolean]
        A flag indicating whether to overlay poes data.  default = False
    poesparam : Optional[str]
        The poes parameter to plot.  default = 'ted'.  available params can be
        found in :class:`gme.sat.poes.poesRec`
    poesMin : Optional[float]
        The min value for the poes data color scale.  default = -3.
    poesMax : Optional[float]
        The max value for the poes data color scale.  default = 0.5
    poesLabel : Optional[str]
        The label for the poes color bar.  default = r"Total Log Energy Flux
        [ergs cm$^{-2}$ s$^{-1}$]"
    overlayBnd : Optional[boolean]
        A flag indicating whether to plot an auroral boundary determined from
        fitting poes data.  default = False
    show : Optional[boolean]
        A flag indicating whether to display the figure on the screen.  This
        can cause problems over ssh.  default = True
    pdf : Optional[boolean]
        A flag indicating whether to output to a pdf file.  default = False.
        WARNING: saving as pdf is slow
    png : Optional[boolean]
        A flag indicating whether to output to a png file.  default = False
    dpi : Optional[int]
        Dots per inch if saving as png.  default = 300
    tFreqBands : optional
        Upper and lower bounds of frequency in kHz to be used.  Must be unset
        (or set to []) or have a pair for each radar, and for any band set to
        [] the default will be used.  default = [[8000,20000]],
        [[8000,20000],[8000,20000]], etc.

    Returns
    -------
    Nothing

    Examples
    --------
        import datetime as dt
        pydarn.plotting.fan.plotFan(dt.datetime(2013,3,16,16,30),['fhe','fhw'],param='power',gsct=True)
        pydarn.plotting.fan.plotFan(dt.datetime(2013,3,16,16,30),['fhe','fhw'],param='power',gsct=True,tFreqBands=[[10000,11000],[]])
    
    """
    savepath=newpath+str(rad)+sTime.strftime("%Y%m%d.%H%M.%S.") + '%.2f' % lon +'.fan.png'
    import os
    if os.path.exists(savepath): return         #Skip if current plot already exists

    from davitpy import pydarn
    from davitpy import gme
    import datetime as dt
    import pickle
    from matplotlib.backends.backend_pdf import PdfPages

    import davitpy.models.aacgm as aacgm
    # Is this leftover from a debugging point?
    # Not sure where os is needed here.
    import os
    import copy
    from davitpy.utils.coordUtils import coord_conv

    tt = dt.datetime.now()

    # check the inputs
    assert(isinstance(sTime, dt.datetime)), 'error, sTime must be a datetime \
           object'
    assert(isinstance(rad, list)), "error, rad must be a list, eg ['bks'] or \
           ['bks','fhe']"
    for r in rad:
        assert(isinstance(r, str) and len(r) == 3), 'error, elements of rad \
               list must be 3 letter strings'
    assert(param == 'velocity' or param == 'power' or param == 'width' or
           param == 'elevation' or param == 'phi0'), ("error, allowable params \
           are 'velocity','power','width','elevation','phi0'")
    assert(scale == [] or len(scale) == 2), (
        'error, if present, scales must have 2 elements')
    assert(colors == 'lasse' or colors == 'aj'), "error, valid inputs for color \
        are 'lasse' and 'aj'"

    # check freq band and set to default if needed
    assert(tFreqBands == [] or len(tFreqBands) == len(rad)), 'error, if \
        present, tFreqBands must have same number of elements as rad'
    tbands = []
    for i in range(len(rad)):
        if tFreqBands == [] or tFreqBands[i] == []:
            tbands.append([8000, 20000])
        else:
            tbands.append(tFreqBands[i])

    for i in range(len(tbands)):
        assert(tbands[i][1] > tbands[i][0]), 'error, frequency upper bound must \
            be > lower bound'

    if(scale == []):
        if(param == 'velocity'): scale = [-200, 200]
        elif(param == 'power'): scale = [0, 30]
        elif(param == 'width'): scale = [0, 150]
        elif(param == 'elevation'): scale = [0, 50]
        elif(param == 'phi0'): scale = [-numpy.pi, numpy.pi]

    fbase = sTime.strftime("%Y%m%d")

    cmap, norm, bounds = utils.plotUtils.genCmap(param, scale, colors=colors,
                                                 lowGray=lowGray)

    # open the data files
    myFiles = []
    myBands = []
    for i in range(len(rad)):
        f = radDataOpen(sTime, rad[i], sTime + dt.timedelta(seconds=interval),
                        fileType=fileType, filtered=filtered, channel=channel)
        if(f is not None):
            myFiles.append(f)
            myBands.append(tbands[i])

    assert(myFiles != []), 'error, no data available for this period'

    xmin, ymin, xmax, ymax = 1e16, 1e16, -1e16, -1e16

    allBeams = [''] * len(myFiles)
    sites, fovs, oldCpids, lonFull, latFull = [], [], [], [], []
    lonC, latC = [], []

    # go through all open files
    for i in range(len(myFiles)):
        # read until we reach start time
        allBeams[i] = radDataReadRec(myFiles[i])
        while (allBeams[i] is not None and allBeams[i].time < sTime):
            allBeams[i] = radDataReadRec(myFiles[i])
            

        # check that the file has data in the target interval
        if(allBeams[i] is None):
            myFiles[i].close()
            myFiles[i] = None
            continue

        # get to field of view coords in order to determine map limits
        t = allBeams[i].time
        site = pydarn.radar.site(radId=allBeams[i].stid, dt=t)
        sites.append(site)
        # Make lists of site lats and lons.  latC and lonC are used
        # for finding the map centre.
        xlon, xlat = coord_conv(site.geolon, site.geolat, "geo", coords,
                                altitude=0., date_time=t)
        latFull.append(xlat)
        lonFull.append(xlon)
        latC.append(xlat)
        lonC.append(xlon)
        myFov = pydarn.radar.radFov.fov(site=site, rsep=allBeams[i].prm.rsep,
                                        ngates=allBeams[i].prm.nrang + 1,
                                        nbeams=site.maxbeam, coords=coords,
                                        date_time=t)
        fovs.append(myFov)
        for b in range(0, site.maxbeam + 1):
            for k in range(0, allBeams[i].prm.nrang + 1):
                lonFull.append(myFov.lonFull[b][k])
                latFull.append(myFov.latFull[b][k])
        oldCpids.append(allBeams[i].cp)

        k = allBeams[i].prm.nrang
        tfreq=allBeams[i].prm.tfreq
        b = 0
        latC.append(myFov.latFull[b][k])
        lonC.append(myFov.lonFull[b][k])
        b = site.maxbeam
        latC.append(myFov.latFull[b][k])
        lonC.append(myFov.lonFull[b][k])

    # Now that we have 3 points from the FOVs of the radars, calculate the
    # lat,lon pair to center the map on. We can simply do this by converting
    # from Spherical coords to Cartesian, taking the mean of each coordinate
    # and then converting back to get lat_0 and lon_0
    lonC, latC = (numpy.array(lonC) + 360.) % 360.0, numpy.array(latC)
    xs = numpy.cos(numpy.deg2rad(latC)) * numpy.cos(numpy.deg2rad(lonC))
    ys = numpy.cos(numpy.deg2rad(latC)) * numpy.sin(numpy.deg2rad(lonC))
    zs = numpy.sin(numpy.deg2rad(latC))
    xc = numpy.mean(xs)
    yc = numpy.mean(ys)
    zc = numpy.mean(zs)
    lon_0 = numpy.rad2deg(numpy.arctan2(yc, xc))
    lat_0 = numpy.rad2deg(numpy.arctan2(zc, numpy.sqrt(xc * xc + yc * yc)))


    # Now do some stuff in map projection coords to get necessary width and
    # height of map and also figure out the corners of the map
    t1 = dt.datetime.now()
    lonFull, latFull = (numpy.array(lonFull) + 360.) % 360.0, \
        numpy.array(latFull)

    tmpmap = utils.mapObj(coords=coords, projection='stere', width=10.0**3,
                          height=10.0**3, lat_0=lat_0, lon_0=lon_0,
                          datetime=sTime)
    x, y = tmpmap(lonFull, latFull)
    if len(x)==0: return
    minx = x.min() * 1.05     # since we don't want the map to cut off labels
    miny = y.min() * 1.05     # or FOVs of the radars we should alter the
    maxx = x.max() * 1.05     # extrema a bit.
    maxy = y.max() * 1.05
    width = (maxx - minx)
    height = (maxy - miny)
    llcrnrlon, llcrnrlat = tmpmap(minx, miny, inverse=True)
    urcrnrlon, urcrnrlat = tmpmap(maxx, maxy, inverse=True)

    dist = width / 50.
    cTime = sTime

    # Clear temporary figure from memory.
    fig = plot.gcf()
    fig.clf()

    myFig = plot.figure(figsize=(12, 8))

    # draw the actual map we want
    #myMap= utils.mapObj(coords=coords, projection='stere', lat_0=lat_0,
#                         lon_0=lon_0, llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat,
#                         urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat,
#                         datetime=sTime)
    #coastLineWidth=0.5, coastLineColor='k',
                         #fillOceans='w', fillContinents='w', fillLakes='w',
            
    width2 = 111e3*80
    myMap = utils.mapObj(boundinglat=65., lon_0=0, coords='mlt',datetime=sTime)
    
    #myMap = utils.mapObj(boundinglat=70.,gridLabels=True, coords='mlt',datetime=sTime)
    
    
    # overlay fields of view, if desired
    if(fov == 1):
        for i, r in enumerate(rad):
            pydarn.plotting.overlayRadar(myMap, fontSize=12, codes=['inv','cly','rkn','lyr'], dateTime=sTime)
            # this was missing fovObj! We need to plot the fov for this
            # particular sTime.
            pydarn.plotting.overlayFov(myMap, codes=['inv','cly','rkn','lyr'], dateTime=sTime, maxGate=60,
                                      lineColor='gray', lineWidth=0.8)
######            
            pydarn.plotting.overlayFov(myMap, codes=r, dateTime=sTime, maxGate=60,
                                      lineColor='k', lineWidth=1.0)
            
            pydarn.plotting.overlayRadar(myMap, fontSize=12, codes=r, dateTime=sTime)

    logging.debug(dt.datetime.now() - t1)
    # manually draw the legend
    if((not fill) and legend):
        # draw the box
        y = [myMap.urcrnry * .82, myMap.urcrnry * .99]
        x = [myMap.urcrnrx * .86, myMap.urcrnrx * .99]
        verts = [x[0], y[0]], [x[0], y[1]], [x[1], y[1]], [x[1], y[0]]
        poly = patches.Polygon(verts, fc='w', ec='k', zorder=11)
        myFig.gca().add_patch(poly)
        labs = ['5 dB', '15 dB', '25 dB', '35 dB', 'gs', '1000 m/s']
        pts = [5, 15, 25, 35]
        # plot the icons and labels
        for w in range(6):
            myFig.gca().text(x[0] + .35 * (x[1] - x[0]), y[1] * (.98 - w *
                             .025), labs[w], zorder=15, color='k', size=8,
                             va='center')
            xctr = x[0] + .175 * (x[1] - x[0])
            if(w < 4):
                myFig.scatter(xctr, y[1] * (.98 - w * .025), s=.1 * pts[w],
                              zorder=15, marker='o', linewidths=.5,
                              edgecolor='face', facecolor='k')
            elif(w == 4):
                myFig.scatter(xctr, y[1] * (.98 - w * .025), s=.1 * 35.,
                              zorder=15, marker='o', linewidths=.5,
                              edgecolor='k', facecolor='w')
            elif(w == 5):
                y = LineCollection(numpy.array([((xctr - dist / 2., y[1] *
                                   (.98 - w * .025)), (xctr + dist / 2., y[1] *
                                                       (.98 - w * .025)))]),
                                   linewidths=.5, zorder=15, color='k')
                myFig.gca().add_collection(y)

    bbox = myFig.gca().get_axes().get_position()
    # now, loop through desired time interval

    tz = dt.datetime.now()
    cols = []
    bndTime = sTime + dt.timedelta(seconds=interval)

    ft = 'None'
    # go though all files
    pcoll = None
    for i in range(len(myFiles)):
        scans = []
        # check that we have good data at this time
        if(myFiles[i] is None or allBeams[i] is None): continue
        ft = allBeams[i].fType
        # until we reach the end of the time window
        while(allBeams[i] is not None and allBeams[i].time < bndTime):
            # filter on frequency
            if (allBeams[i].prm.tfreq >= myBands[i][0] and
                    allBeams[i].prm.tfreq <= myBands[i][1]):
                scans.append(allBeams[i])
            # read the next record
            allBeams[i] = radDataReadRec(myFiles[i])
        # if there is no data in scans, overlayFan will object
        if scans == []: continue
        intensities, pcoll = overlayFanRfe(scans, myMap, myFig, param, coords,
                                        gsct=gsct, site=sites[i], fov=fovs[i],
                                        fill=fill, velscl=velscl, dist=dist,
                                        cmap=cmap, norm=norm)
        


    # if no data has been found pcoll will not have been set, and the following
    # code will object
    if pcoll:
        cbar = myFig.colorbar(pcoll, orientation='vertical', shrink=.65,
                              fraction=.1, drawedges=True)

        l = []
        # define the colorbar labels
        for i in range(0, len(bounds)):
            if(param == 'phi0'):
                ln = 4
                if(bounds[i] == 0): ln = 3
                elif(bounds[i] < 0): ln = 5
                l.append(str(bounds[i])[:ln])
                continue
            if((i == 0 and param == 'velocity') or i == len(bounds) - 1):
                l.append(' ')
                continue
            l.append(str(int(bounds[i])))
        cbar.ax.set_yticklabels(l)
        cbar.ax.tick_params(axis='y', direction='out')
        # set colorbar ticklabel size
        for ti in cbar.ax.get_yticklabels():
            ti.set_fontsize(12)
        if(param == 'velocity'):
            cbar.set_label('Velocity [m/s]', size=14)
            cbar.extend = 'max'

        if(param == 'grid'): cbar.set_label('Velocity [m/s]', size=14)
        if(param == 'power'): cbar.set_label('Power [dB]', size=14)
        if(param == 'width'): cbar.set_label('Spec Wid [m/s]', size=14)
        if(param == 'elevation'): cbar.set_label('Elev [deg]', size=14)
        if(param == 'phi0'): cbar.set_label('Phi0 [rad]', size=14)

    # myFig.gca().set_rasterized(True)
    # label the plot
    tx1 = myFig.text((bbox.x0 + bbox.x1) / 2.,
                     bbox.y1 + .02, cTime.strftime('%Y/%m/%d'), ha='center',
                     size=14, weight=550)
    tx2 = myFig.text(bbox.x1 + .02, bbox.y1 + .02, cTime.strftime('%H:%M - ') +
                     bndTime.strftime('%H:%M      '), ha='right', size=13,
                     weight=550)
    tx3 = myFig.text(bbox.x0, bbox.y1 + .02, '[' + ft + ']', ha='left',
                     size=13, weight=550)
    # label with frequency bands
    tx4 = myFig.text(bbox.x1 + .02, bbox.y1, 'Frequency:', ha='right',
                     size=8, weight=550)
    
 
    for i in range(len(rad)):
        myFig.text(bbox.x1 + .02, bbox.y1 - ((i + 1) * .015), rad[i] + ': '+
                   str(tfreq/ 1e3) +
                   ' MHz', ha='right', size=8, weight=550)
    
        #Add magnetometer data
    if imf[1] =='pm': imf[1]=0
    if imf[2] =='pm': imf[2]=0
    print imf[1]
    tx5 = myFig.text(bbox.x1 +0.02, bbox.y1-0.04, 'OMNI By: '+ '%.2f'%imf[1]+' nT', ha='right',
                     size=11, weight=450)
    tx6 = myFig.text(bbox.x1 +0.02, bbox.y1-0.06, 'OMNI Bz: '+ '%.2f'%imf[2]+' nT', ha='right',
                     size=11, weight=450)
    if(overlayPoes):
        pcols = gme.sat.poes.overlayPoesTed(myMap, myFig.gca(), cTime,
                                            param=poesparam, scMin=poesMin,
                                            scMax=poesMax)
        if(pcols is not None):
            cols.append(pcols)
            pTicks = numpy.linspace(poesMin, poesMax, 8)
            cbar = myFig.colorbar(pcols, ticks=pTicks, orientation='vertical',
                                  shrink=0.65, fraction=.1)
            cbar.ax.set_yticklabels(pTicks)
            cbar.set_label(poesLabel, size=14)
            cbar.ax.tick_params(axis='y', direction='out')
            # set colorbar ticklabel size
            for ti in cbar.ax.get_yticklabels():
                ti.set_fontsize(12)

    if(overlayBnd):
        gme.sat.poes.overlayPoesBnd(myMap, myFig.gca(), cTime)

########Adding red circle for found RFE
    #Coordinates in map projection
    x,y=myMap(lon,lat)
    #x,y=lon,lat
    myMap.scatter(x, y, s=500, linewidths=2.5,marker='o', facecolors='None', edgecolors='r',zorder=10)
    
    
    #Overlaying convection plot
    ax = myFig.add_subplot(111)
    mapDatObj = davitpy.pydarn.plotting.plotMapGrd.MapConv(sTime, myMap, ax)
    #mapDatObj.overlayMapFitVel()
    if mapDatObj.mapData is not None: mapDatObj.overlayCnvCntrs()       #Put this on if available
    #mapDatObj.overlayHMB(hmbCol='Green')
    #pydarn.plotting.overlayFov(myMap, codes=['inv','cly'], dateTime=sTime,maxGate=60)
                                       #fovObj=fovs[i],maxGate=70

    # handle the outputs
    if png is True:
        # if not show:
        #   canvas = FigureCanvasAgg(myFig)
        savepath=newpath+str(rad)+sTime.strftime("%Y%m%d.%H%M.%S.") + '%.2f' % lon +'.fan.png'
        print savepath
        myFig.savefig(savepath, dpi=dpi)
        
    if pdf:
        # if not show:
        #   canvas = FigureCanvasAgg(myFig)
        logging.info('Saving as pdf...this may take a moment...')
        savepath=newpath+str(rad)+sTime.strftime("%Y%m%d.%H%M.%S.") + '%.2f' % lon +'.fan.pdf'
        print savepath
        myFig.savefig(savepath, dpi=dpi)
    if show:
        myFig.show()
        

    myFig.clear()                  #Clear figure
    plot.clf()
    plot.close(myFig)
    pylab.close(myFig)
    #plot.close(plot.gcf())			#Close figure
    

    


def overlayFanRfe(myData, myMap, myFig, param, coords='geo', gsct=0, site=None,
               fov=None, gs_flg=[], fill=True, velscl=1000., dist=1000.,
               cmap=None, norm=None, alpha=1):

    """A function of overlay radar scan data on a map

    Parameters
    ----------
    myData : pydarn.sdio.radDataTypes.scanData or
             pydarn.sdio.radDataTypes.beamData or
             list of pydarn.sdio.radDataTypes.beamData objects
        A radar beam object, a radar scanData object, or simply a list of
        radar beams
    myMap :
        The map we are plotting on
    myFig :
        Figure object that we are plotting to
    coords : Optional[str]
        The coordinates we are plotting in.  Default: geo
    param : Optional[str]
        The parameter to be plotted, valid inputs are 'velocity', 'power',
        'width', 'elevation', 'phi0'.  default = 'velocity
    gsct : Optional[boolean]
        A flag indicating whether we are distinguishing ground scatter.
        default = 0
    intensities : Optional[  ]
        A list of intensities (used for colorbar)
    fov : Optional[pydarn.radar.radFov.fov]
        A radar fov object
    gs_flg : Optional[  ]
        A list of gs flags, 1 per range gate
    fill : Optional[boolean]
        A flag indicating whether to plot filled or point RB cells.
        default = True
    velscl : Optional[float]
        The velocity to use as baseline for velocity vector length, only
        applicable if fill = 0.  default = 1000
    lines : Optional[  ]
        An array to have the endpoints of velocity vectors.  only applicable if
        fill = 0.  default = []
    dist : Optional [float]
        The length in map projection coords of a velscl length velocity vector.
        default = 1000. km

    Returns
    -------
    intensities

    pcoll

    lcoll


    Example
    -------
        overlayFan(aBeam,myMap,param,coords,gsct=gsct,site=sites[i],fov=fovs[i],
                   verts=verts,intensities=intensities,gs_flg=gs_flg)

    """
    from davitpy import pydarn
    if(site is None):
        site = pydarn.radar.site(radId=myData[0].stid, dt=myData[0].time)
    if(fov is None):
        fov = pydarn.radar.radFov.fov(site=site, rsep=myData[0].prm.rsep,
                                      ngates=myData[0].prm.nrang + 1,
                                      nbeams=site.maxbeam, coords=coords,
                                      date_time=myData[0].time)

    if(isinstance(myData, pydarn.sdio.beamData)): myData = [myData]

    gs_flg, lines = [], []
    if fill: verts, intensities = [], []
    else: verts, intensities = [[], []], [[], []]

    # loop through gates with scatter
    for myBeam in myData:
        for k in range(0, len(myBeam.fit.slist)):
            if myBeam.fit.slist[k] not in fov.gates: continue
            r = myBeam.fit.slist[k]

            if fill:
                x1, y1 = myMap(fov.lonFull[myBeam.bmnum, r],
                               fov.latFull[myBeam.bmnum, r])
                x2, y2 = myMap(fov.lonFull[myBeam.bmnum, r + 1],
                               fov.latFull[myBeam.bmnum, r + 1])
                x3, y3 = myMap(fov.lonFull[myBeam.bmnum + 1, r + 1],
                               fov.latFull[myBeam.bmnum + 1, r + 1])
                x4, y4 = myMap(fov.lonFull[myBeam.bmnum + 1, r],
                               fov.latFull[myBeam.bmnum + 1, r])

                # save the polygon vertices
                verts.append(((x1, y1), (x2, y2), (x3, y3), (x4, y4),
                              (x1, y1)))

                # save the param to use as a color scale
                if(param == 'velocity'):
                    intensities.append(myBeam.fit.v[k])
                elif(param == 'power'):
                    intensities.append(myBeam.fit.p_l[k])
                elif(param == 'width'):
                    intensities.append(myBeam.fit.w_l[k])
                elif(param == 'elevation' and myBeam.prm.xcf):
                    intensities.append(myBeam.fit.elv[k])
                elif(param == 'phi0' and myBeam.prm.xcf):
                    intensities.append(myBeam.fit.phi0[k])

            else:
                x1, y1 = myMap(fov.lonCenter[myBeam.bmnum, r],
                               fov.latCenter[myBeam.bmnum, r])
                verts[0].append(x1)
                verts[1].append(y1)

                x2, y2 = myMap(fov.lonCenter[myBeam.bmnum, r + 1],
                               fov.latCenter[myBeam.bmnum, r + 1])

                theta = math.atan2(y2 - y1, x2 - x1)

                x2, y2 = x1 + myBeam.fit.v[k] / velscl * (-1.0) * \
                    math.cos(theta) * dist, y1 + myBeam.fit.v[k] / velscl * \
                    (-1.0) * math.sin(theta) * dist

                lines.append(((x1, y1), (x2, y2)))
                # save the param to use as a color scale
                if(param == 'velocity'):
                    intensities[0].append(myBeam.fit.v[k])
                elif(param == 'power'):
                    intensities[0].append(myBeam.fit.p_l[k])
                elif(param == 'width'):
                    intensities[0].append(myBeam.fit.w_l[k])
                elif(param == 'elevation' and myBeam.prm.xcf):
                    intensities[0].append(myBeam.fit.elv[k])
                elif(param == 'phi0' and myBeam.prm.xcf):
                    intensities[0].append(myBeam.fit.phi0[k])

                if(myBeam.fit.p_l[k] > 0):
                    intensities[1].append(myBeam.fit.p_l[k])
                else:
                    intensities[1].append(0.)
            if(gsct):
                gs_flg.append(myBeam.fit.gflg[k])

    # do the actual overlay
    if(fill):
        # if we have data
        if(verts != []):
            if(gsct == 0):
                inx = numpy.arange(len(verts))
            else:
                inx = numpy.where(numpy.array(gs_flg) == 0)
                x = PolyCollection(numpy.array(verts)[numpy.where(
                                   numpy.array(gs_flg) == 1)], facecolors='.3',
                                   linewidths=0, zorder=5, alpha=alpha)
                myFig.gca().add_collection(x, autolim=True)

            pcoll = PolyCollection(numpy.array(verts)[inx],
                                   edgecolors='face', linewidths=0,
                                   closed=False, zorder=4, alpha=alpha,
                                   cmap=cmap, norm=norm)
            # set color array to intensities
            pcoll.set_array(numpy.array(intensities)[inx])
            myFig.gca().add_collection(pcoll, autolim=True)
            return intensities, pcoll
    else:
        # if we have data
        if(verts != [[], []]):
            if(gsct == 0):
                inx = numpy.arange(len(verts[0]))
            else:
                inx = numpy.where(numpy.array(gs_flg) == 0)
                # plot the ground scatter as open circles
                x = myFig.scatter(numpy.array(verts[0])[numpy.where(
                                  numpy.array(gs_flg) == 1)],
                                  numpy.array(verts[1])[numpy.where(
                                      numpy.array(gs_flg) == 1)],
                                  s=.1 * numpy.array(intensities[1])[
                                  numpy.where(numpy.array(gs_flg) == 1)],
                                  zorder=5, marker='o', linewidths=.5,
                                  facecolors='w', edgecolors='k')
                myFig.gca().add_collection(x, autolim=True)

            # plot the i-s as filled circles
            ccoll = myFig.gca().scatter(numpy.array(verts[0])[inx],
                                        numpy.array(verts[1])[inx],
                                        s=.03 * numpy.array(
                                        intensities[1])[inx], cmap=cmap, zorder=6,
                                        marker='o', linewidths=.5,
                                        edgecolors='face',
                                        norm=norm)

            # set color array to intensities
            ccoll.set_array(numpy.array(intensities[0])[inx])
            myFig.gca().add_collection(ccoll)
            # plot the velocity vectors
            lcoll = LineCollection(numpy.array(lines)[inx], linewidths=.5,
                                   zorder=12, cmap=cmap, norm=norm)
            lcoll.set_array(numpy.array(intensities[0])[inx])
            myFig.gca().add_collection(lcoll)

            return intensities, lcoll


