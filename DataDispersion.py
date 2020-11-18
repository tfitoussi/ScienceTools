import sys
import numpy as np

class DataDispersion(object):
    def __init__(self,data_x):
        self.data_x = data_x

    def total_disp(self,CL=100):
        '''
            Compute the global median, Confidence Level of data_x in %
        '''
        mean = np.nanmean(self.data_x)
        median = np.nanmedian(self.data_x)
        CLm = np.nanpercentile(self.data_x,50-CL/2)
        CLp = np.nanpercentile(self.data_x,50+CL/2)
        return mean, median, CLm, CLp

    def versus(self,data_y,bins,CL=100):
        '''
            This class is designed to compute the median, 
            Confidence Level of data_x in % in Nbins of data_y
            between the minimum and the maximum of data_y
        '''
        if not len(self.data_x) == len(data_y):
            print("data_x and data_y shall hae the same length.")
            sys.exit()

        ymin, ymax = min(data_y), max(data_y) 
        Nbins = len(bins)-1

        mean = np.zeros(Nbins,dtype=float)
        median = np.zeros(Nbins,dtype=float)
        CLm = np.zeros(Nbins,dtype=float)
        CLp = np.zeros(Nbins,dtype=float)

        for ibin, yl in enumerate(bins[:-1]):
            ym = bins[ibin+1]
            dat = self.data_x[ np.where( (data_y >= yl) & (data_y < ym) ) ]
            if len(dat) == 0: # empty bin
                continue
            mean[ibin] = np.nanmean(dat)
            median[ibin] = np.nanmedian(dat)
            CLm[ibin] = np.nanpercentile(dat,50-CL/2)
            CLp[ibin] = np.nanpercentile(dat,50+CL/2)
        
        return mean, median, CLm, CLp
