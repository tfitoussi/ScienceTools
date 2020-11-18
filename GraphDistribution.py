#!/usr/bin/python3
#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mplsettings import *

class GraphDistribution(object):
    def __init__(self,xlabel="",ylabel="",title="",xlog=True,ylog=True,colors_list=std_colors_list):
        self.fig = plt.figure(figsize=(12,9))
        self.ax = self.fig.add_subplot(111)
        if xlog:
            self.ax.set_xscale('log')
        if ylog:
            self.ax.set_yscale('log')
        self.ax.grid(b=True,which='major')
        self.ax.tick_params(right=True,top=True,which="both")

        self.ax.set_xlabel(xlabel,fontsize=label_size)
        self.ax.set_ylabel(ylabel,fontsize=label_size)
        if not (title == ""):
            self.ax.set_title(title,fontsize=label_size)
 
        self.legend1 = []
        self.plotlist1 = []
        self.legend2 = []
        self.plotlist2 = []
        
        self.colors_list = colors_list
        self.autocolor = 0
        self.lastcolor = self.colors_list[0]

    def add(self,x0,y0,notes=[],label="",leg=1,linestyle='-',linewidth=2,color="",histo=True,zorder=5):
        if len(color) == 0:
            color = self.colors_list[self.autocolor % len(self.colors_list)]
            self.autocolor += 1
        elif type(color) == str:
            if color == "same":
                color = self.lastcolor
        self.lastcolor = color

        if histo:
            plot = self.ax.plot(x0,y0,color=color,linewidth=linewidth,linestyle=linestyle,
                        drawstyle='steps-mid',zorder=zorder)
        else:
            plot = self.ax.plot(x0,y0,color=color,linewidth=linewidth,linestyle=linestyle,zorder=zorder)
        if len(notes) != 0:
            for i, txt in enumerate(notes):
                self.ax.annotate(txt, (x0[i], y0[i]), rotation=90, fontsize=label_size,
                        color=color,zorder=zorder)
        if not label == "":
            if leg==1:
                self.legend1 = np.append(self.legend1,[label])
                self.plotlist1 = np.append(self.plotlist1,[plot])
            else:
                self.legend2 = np.append(self.legend2,[label])
                self.plotlist2 = np.append(self.plotlist2,[plot])

    def add_data(self,Xmed,Ymed,Xmax=0,Xmin=0,Ymax=0,Ymin=0,notes=[],label='',leg=1,marker='s',
                    color="",linewidth=2,zorder=6):
        if len(color) == 0:
            color = self.colors_list[self.autocolor % len(self.colors_list)]
            self.autocolor += 1
        elif type(color) == str:
            if color == "same":
                color = self.lastcolor
        self.lastcolor = color

        plot = self.ax.scatter(Xmed,Ymed,c=color,marker=marker,zorder=zorder)

        if Xmax !=0 and Xmin != 0:  
            Xerr = [Xmed-Xmin,Xmax-Xmed]
            Yerr = [Ymax-Ymed,-Ymin+Ymed]
            self.ax.errorbar(Xmed,Ymed,xerr=Xerr,yerr=Yerr,linestyle="",linewidth=linewidth,
                 color=color,marker=marker,zorder=zorder)

        if type(Ymax) != int:
            select = (Ymed==0) 
            uplim = (Ymed==0) & (Ymax!=0)
            lowlim = (Ymed==0) & (Ymin!=0)
            if len(Ymax[uplim]) != 0:
                limlength = Ymax[uplim]/2 
                self.ax.errorbar(Xmed[uplim],Ymax[uplim],yerr=limlength,uplims=True,
                    linestyle="", linewidth=linewidth, color=color,marker=marker,zorder=zorder)
            if len(Ymin[lowlim]) != 0:
                limlength = Ymin[lowlim]*2 
                self.ax.errorbar(Xmed[lowlim],Ymin[lowlim],yerr=limlength,lowlims=True,
                    linestyle="", linewidth=linewidth, color=color,marker=marker,zorder=zorder)

        if len(notes) != 0:
            for i, txt in enumerate(notes):
                self.ax.annotate(txt, (Xmed[i], Ymed[i]), rotation=90, fontsize=label_size,
                        color=color,zorder=zorder)
        if not label == "":
            if leg==1:
                self.legend1 = np.append(self.legend1,[label])
                self.plotlist1 = np.append(self.plotlist1,[plot])
            else:
                self.legend2 = np.append(self.legend2,[label])
                self.plotlist2 = np.append(self.plotlist2,[plot])

    def add_area(self,x,ymin,ymax,label="",leg=1,color="",alpha=0.5,step=None,zorder=1):
        if len(color) == 0:
            color = self.colors_list[self.autocolor % len(self.colors_list)]
            self.autocolor += 1
        elif type(color) == str:
            if color == "same":
                color = self.lastcolor
        self.lastcolor = color

        plot = self.ax.fill_between(x,ymin,ymax,step=step,color=color,alpha=alpha,zorder=zorder)
        if not label == "":
            if leg==1:
                self.legend1 = np.append(self.legend1,[label])
                self.plotlist1 = np.append(self.plotlist1,[plot])
            else:
                self.legend2 = np.append(self.legend2,[label])
                self.plotlist2 = np.append(self.plotlist2,[plot])

    def add_vertical(self,xmin,xmax=0,label="",leg=1,color="",linestyle='-',linewidth=2,alpha=0.5,zorder=2):
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

    def add_txt(self,xpos,ypos,txt,color="k",rotation='horizontal',horizontalalignment='left',verticalalignment='bottom'):
        self.ax.text(xpos, ypos, txt, fontsize=label_size, color=color, rotation=rotation, zorder=3,
                horizontalalignment=horizontalalignment, verticalalignment=verticalalignment)

    def str_xticks(self,ticks_labels,rotation='horizontal'):
        self.ax.set_xticks(range(len(ticks_labels)))
        self.ax.set_xticklabels(ticks_labels, rotation=rotation, fontsize=label_size)

    def str_yticks(self,ticks_labels,rotation='horizontal'):
        self.ax.set_yticks(range(len(ticks_labels)))
        self.ax.set_xticklabels(ticks_labels, rotation=rotation, fontsize=label_size)

    def plot(self,save="",xlim=[],ylim=[],leg1_pos="best",leg2_pos="best",close_fig=True):
        plt.sca(self.ax)
        if np.size(self.legend1) != 0: # not empty
            leg = plt.legend(self.plotlist1,self.legend1,fontsize='xx-large',loc=leg1_pos)
            plt.gca().add_artist(leg)
        if np.size(self.legend2) != 0: # not empty
            leg = plt.legend(self.plotlist2,self.legend2,fontsize='xx-large',loc=leg2_pos)
            plt.gca().add_artist(leg)
        
        if np.size(xlim) != 0: # not empty
            self.ax.set_xlim(xlim)
        if np.size(ylim) != 0: # not empty
            self.ax.set_ylim(ylim)

        if not (save == ""):
            save = save.replace(".","_")
            plt.savefig(save+".pdf",bbox_inches='tight')
            plt.savefig(save+".png",bbox_inches='tight')
            if close_fig:
                plt.close(self.fig)
        else:
            plt.show()
