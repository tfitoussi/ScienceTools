#!/usr/bin/python3
#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as colormap
from scipy.spatial import ConvexHull
from matplotlib.patches import Polygon
from mplsettings import *
from terminal_output import tsignals

class Graph2Dmatrix(object):
    def __init__(self,xlabel="",ylabel="",title="",xlog=False,ylog=False,grid=False,colors_list=std_colors_list):
        self.fig = plt.figure(figsize=(12,9))
        self.ax = self.fig.add_subplot(111)
        if xlog:
            self.ax.set_xscale('log')
        if ylog:
            self.ax.set_yscale('log')
        if grid:
            self.ax.grid(b=True,which='major')

        self.ax.set_xlabel(xlabel,fontsize=label_size)
        self.ax.set_ylabel(ylabel,fontsize=label_size)
        if not (title == ""):
            self.ax.set_title(title,fontsize=label_size)
            
        self.map_added = False
        self.cbar = False
        self.colors_list = colors_list
        self.autocolor = 0
        self.lastcolor = colors_list[0]

        self.legend1 = []
        self.plotlist1 = []


    def add_map(self,matrix,extent=None,cmap="jet",clim=[]):
        if self.map_added == True:
            print(tsignals.WARNING+"Beware a map has already been set for this image and will be erased"+tsignals.ENDC)
        self.im = self.ax.matshow(matrix,cmap=plt.cm.get_cmap(cmap),extent=extent,
                origin='lower',aspect="auto", zorder=1)
        self.map_added = True
        if len(clim) == 2:
            self.im.set_clim(clim[0],clim[1])
        self.cbar = True

    def add_vectors(self, xarray, yarray, vx, vy, color="limegreen", zorder=5):
        self.ax.quiver(xarray, yarray, vx, vy, color=color, units='width', pivot='mid',zorder=zorder)
        
    def add_point(self, x, y, label="", marker='x', linewidth=2, s=80, color='blue',
           cmap="jet", clim=[], cbar=False, zorder=5):
        if self.map_added == True:
            print(tsignals.WARNING+"Beware a map has already been set for this image and will be erased"+tsignals.ENDC)

        if len(color) == 0:
            color = self.colors_list[self.autocolor % len(self.colors_list)]
            self.autocolor += 1
        elif type(color) == str:
            if color == "same":
                color = self.lastcolor
        else:
            self.map_added = True

        if cbar: 
            self.cbar = cbar 
            self.im = self.ax.scatter(x, y, marker=marker, s=s, linewidth=linewidth, c=color,
                        cmap=cmap,zorder=zorder)
        else:
            self.ax.scatter(x, y, marker=marker, s=s, linewidth=linewidth, c=color,zorder=zorder)
        if label:
            self.ax.annotate(" "+label, (x, y), fontsize=label_size, color=color,zorder=zorder)

        if len(clim) == 2:
            self.im.set_clim(clim[0],clim[1])

    def add_curve(self, x, y, color="", linestyle='-', linewidth=2, zorder=5):
        if len(color) == 0:
            color = self.colors_list[self.autocolor % len(self.colors_list)]
            self.autocolor += 1
        elif type(color) == str:
            if color == "same":
                color = self.lastcolor
        self.lastcolor = color

        plot = self.ax.plot(x,y,color=color,linewidth=linewidth,linestyle=linestyle,zorder=zorder)

    def add_vertical(self,xmin,xmax=0,label="",leg=1,color="",linestyle='-',linewidth=2,alpha=0.5,zorder=5):
        if len(color) == 0:
            color = self.colors_list[self.autocolor % len(self.colors_list)]
            self.autocolor += 1
        elif type(color) == str:
            if color == "same":
                color = self.lastcolor
        self.lastcolor = color
        if xmax == 0:
            plot = self.ax.axvline(xmin,color=color,linewidth=linewidth,linestyle=linestyle,zorder=zorder)
        else:
            plot = self.ax.axvspan(xmin,xmax,color=color,alpha=alpha,zorder=zorder)
        if not label == "":
            if leg==1:
                self.legend1 = np.append(self.legend1,[label])
                self.plotlist1 = np.append(self.plotlist1,[plot])
            else:
                self.legend2 = np.append(self.legend2,[label])
                self.plotlist2 = np.append(self.plotlist2,[plot])


    def add_area(self,x, y, label="",color="",alpha=0.5, zorder=3):
        if len(color) == 0:
            color = self.colors_list[self.autocolor % len(self.colors_list)]
            self.autocolor += 1
        elif type(color) == str:
            if color == "same":
                color = self.lastcolor
        self.lastcolor = color

        # Encircle data
        p = np.c_[x,y]
        hull = ConvexHull(p)
        poly = Polygon(p[hull.vertices,:],color=color,alpha=alpha,zorder=zorder)
        self.ax.add_patch(poly)
        if not label == "":
            self.legend1 = np.append(self.legend1,[label])
            self.plotlist1 = np.append(self.plotlist1,[poly])

        return p[hull.vertices,:]


    def plot(self,save="",cbarlabel='',xlim=[],ylim=[],close_fig=True,leg_pos="best"):
        plt.sca(self.ax)

        plt.gca().xaxis.tick_bottom()

        if np.size(xlim) != 0: # not empty
            self.ax.set_xlim(xlim)
        if np.size(ylim) != 0: # not empty
            self.ax.set_ylim(ylim)

        if self.cbar: 
            cbar = plt.colorbar(self.im, ax=self.ax)
            if cbarlabel != '':
                cbar.ax.set_ylabel(cbarlabel,fontsize=label_size)

        if len(self.legend1) > 0:    
            leg = plt.legend(self.plotlist1,self.legend1,fontsize='xx-large',loc=leg_pos)
            plt.gca().add_artist(leg)

        if not (save == ""):
            save = save.replace(".","_")
            #plt.savefig(save+".pdf",bbox_inches='tight')
            plt.savefig(save+".png",bbox_inches='tight')
            if close_fig:
                plt.close(self.fig)
        else:
            plt.show()
