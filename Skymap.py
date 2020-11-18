import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
from matplotlib.patches import Polygon
from mplsettings import * # contains "from matplotlib import rcParams"

colors_list = ['m','b','c','g','y','r','k']

class Skymap(object):
    def __init__(self,title='',zoom=[],coord="gal"):
        if zoom == []:
            self.fig = plt.figure(figsize=(A4width,A4heigth/3.))
            self.hammerproj = True
            self.ax = self.fig.add_subplot(111,projection='hammer')
            self.ax.tick_params(axis='both',which='major',labelsize=label_size)
            labels = ["150$^\degree$","120$^\degree$","90$^\degree$","60$^\degree$","30$^\degree$",
                        "0$^\degree$","-30$^\degree$","-60$^\degree$","-90$^\degree$","-120$^\degree$",
                        "-150$^\degree$"]
            self.ax.set_xticklabels(labels)

        else:
            self.zoom = zoom
            ratio = (zoom[1][1]-zoom[1][0]) / (zoom[0][1]-zoom[0][0]) 
            self.fig = plt.figure(figsize=(A4width,A4width*ratio))
            self.hammerproj = False
            self.ax = self.fig.add_subplot(111)
            self.ax.set_xlim([zoom[0][1],zoom[0][0]])
            self.ax.set_ylim([zoom[1][0],zoom[1][1]])

        if coord == "gal":
            self.ax.set_xlabel("Gal. Long. [deg]",fontsize=label_size)
            self.ax.set_ylabel("Gal. Lat. [deg]",fontsize=label_size)
        elif coord == "supergal":
            self.ax.set_xlabel("Supergal. Long. [deg]",fontsize=label_size)
            self.ax.set_ylabel("Supergal. Lat. [deg]",fontsize=label_size)
        elif coord == "RADEC":
            self.ax.set_xlabel("RA [deg]",fontsize=label_size)
            self.ax.set_ylabel("DEC [deg]",fontsize=label_size)

        self.ax.set_title(title,fontsize=label_size)
        self.ax.grid()
        self.cbar = False
        self.autocolor = 0

        self.legend1 = []
        self.plotlist1 = []
        self.legend2 = []
        self.plotlist2 = []


    def add(self,lons,lats,color="",label="",leg=1,marker='+',size=rcParams['lines.markersize']**2,
            notes=None,rotation='horizontal',cbar=False,cmap='viridis',clim=[],zorder=2):
        plt.sca(self.ax)

        if len(color) == 0:
            color = colors_list[self.autocolor % len(colors_list)]
            self.autocolor += 1
        elif len(color) > 1:
            maxcolor = max(color)

        if self.hammerproj: # minus longitude -> east towards left, west towards right
            lons = -np.copy(lons)
            fontsize = 0.6*label_size
        else: # in degre
            # plot only points in the area of interest (can mess-up the figure size with test
            # otherwise)
            lons = np.copy(lons*180./np.pi)
            lats = np.copy(lats*180./np.pi)
            if type(lons) == np.ndarray:                        
                sel = (lons >= self.zoom[0][0]) & (lons <= self.zoom[0][1]) 
                sel = sel & (lats >= self.zoom[1][0]) & (lats <= self.zoom[1][1])
                lons = lons[sel]
                lats = lats[sel]
                if type(notes) == np.ndarray:                        
                    notes = np.copy(notes[sel])
                if type(color) == np.ndarray:                        
                    color = np.copy(color[sel])
            fontsize = label_size

        sc = self.ax.scatter(lons,lats,c=color,linewidths=0,marker=marker,s=size,
                    cmap=plt.cm.get_cmap(cmap),zorder=zorder)
        if not label == "":
            if leg==1:
                self.legend1 = np.append(self.legend1,[label])
                self.plotlist1 = np.append(self.plotlist1,[sc])
            else:
                self.legend2 = np.append(self.legend2,[label])
                self.plotlist2 = np.append(self.plotlist2,[sc])

        if cbar:
            self.sc = sc
            self.cbar = True
            if len(clim) == 2:
                self.sc.set_clim(clim[0],clim[1])

        horizontalalignment='left'
        verticalalignment='bottom'
        if isinstance(rotation,float) or isinstance(rotation,int):
            if rotation < 0:
                verticalalignment='top'
        if type(notes) == np.ndarray:
            for i, txt in enumerate(notes):
                if len(color) > 1: # same color for point and notes
                    c = plt.cm.get_cmap(cmap)(color[i]/maxcolor)
                else:
                    c = color
                self.ax.annotate(" "+txt,(lons[i],lats[i]),color=c,fontsize=fontsize,zorder=zorder,
                            rotation=rotation,horizontalalignment=horizontalalignment,
                            verticalalignment=verticalalignment)
        elif type(notes) == str:
            self.ax.annotate(" "+notes,(lons,lats),color=color,fontsize=fontsize,zorder=zorder,
                        rotation=rotation,horizontalalignment=horizontalalignment,
                        verticalalignment=verticalalignment)


    def add_vector(self,lon,lat,dir_x,dir_y,amp,zorder=2):
        plt.sca(self.ax)
        if self.hammerproj: # minus longitude -> east towards left, west towards right
            lon = np.copy(-lon)
        else: # in degre
            lon = np.copy(lon*180./np.pi)
            lat = np.copy(lat*180./np.pi)
        self.sc = self.ax.quiver(lon,lat,dir_x,dir_y,amp,pivot='middle',zorder=zorder)


    def add_area(self,lons,lats,label="",leg=1,color="b",alpha=0.5,zorder=1):
        plt.sca(self.ax)
        if self.hammerproj: # minus longitude -> east towards left, west towards right
            lons = -np.copy(lons)
        else: # in degre
            lons = np.copy(lons*180./np.pi)
            lats = np.copy(lats*180./np.pi)
        # Encircle data
        p = np.c_[lons,lats]
        hull = ConvexHull(p)
        poly = Polygon(p[hull.vertices,:],color=color,alpha=alpha,zorder=zorder)
        self.ax.add_patch(poly)
        if not label == "":
            if leg==1:
                self.legend1 = np.append(self.legend1,[label])
                self.plotlist1 = np.append(self.plotlist1,[poly])
            else:
                self.legend2 = np.append(self.legend2,[label])
                self.plotlist2 = np.append(self.plotlist2,[poly])

        if self.hammerproj: # minus longitude -> east towards left, west towards right
            return p[hull.vertices,:]
        else: 
            return p[hull.vertices,:]*np.pi/180.


    def plot(self,save_name='',cbar_label="",leg1_pos="upper left",leg2_pos='upper right',close_fig=True):
        plt.sca(self.ax)
        if self.cbar:
            cbar = plt.colorbar(self.sc,orientation='horizontal',fraction=0.035)
            cbar.ax.set_xlabel(cbar_label,fontsize=label_size)
            cbar.ax.tick_params(axis='both',which='major',labelsize=label_size)
        if np.size(self.legend1) != 0: # not empty
            leg = plt.legend(self.plotlist1,self.legend1,fontsize='xx-large',loc=leg1_pos)
            plt.gca().add_artist(leg)
        if np.size(self.legend2) != 0: # not empty
            leg = plt.legend(self.plotlist2,self.legend2,fontsize='xx-large',loc=leg2_pos)
            plt.gca().add_artist(leg)

        
        if not (save_name == ''):
            save_name = save_name.replace(".","_")
            #plt.savefig(save_name+".pdf",bbox_inches='tight')
            plt.savefig(save_name+".png",bbox_inches='tight')
            if close_fig:
                plt.close(self.fig)
        else:
            plt.show()
