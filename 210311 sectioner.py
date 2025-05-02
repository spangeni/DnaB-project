# -*- coding: utf-8 -*-
"""
Updated 05022025

@author: Original draft by Olivia and updated by Sushil
#This script loads your kymo and saves the cropped section on the kymo with high resolution.
"""

from lumicks import pylake
import matplotlib.pyplot as plt
from IPython import get_ipython
import numpy as np
import math
import matplotlib.colors as mcolors
import glob
import pathlib

colors = [(1,0,0,c) for c in np.linspace(0,1,100)]
cmapred = mcolors.LinearSegmentedColormap.from_list('mycmap', colors, N=5)
colors = [(0,1,0,c) for c in np.linspace(0,1,100)]
cmapgreen = mcolors.LinearSegmentedColormap.from_list('mycmap', colors, N=5)
colors = [(0,0,1,c) for c in np.linspace(0,1,100)]
cmapblue = mcolors.LinearSegmentedColormap.from_list('mycmap', colors, N=5)

def ext_neg(n):
    nn = n-10
    if nn < 0:
        return 0
    else:
        return nn

def ext_pos(n,m):
    nn = n+10
    if nn > m:
        return m
    else:
        return nn
    
#%%
direh=r"D:\Sushil\Edwin_Srs2/"
dirl = r"05022023/"
dire=direh+dirl

k = input('what kymo? ')
#k='17'
newf='sections\\' #output folder
pathlib.Path(dire+newf).mkdir(parents=True, exist_ok=True)
#print('kymo',k)
vm=13

filename= glob.glob(dire+'*h '+ k + '*.h5')
file = pylake.File(filename[0])
_, kymo = file.kymos.popitem()

green = kymo.green_image
red = kymo.red_image
xm = green.shape[1]-1
ym = green.shape[0]-1

linetime = kymo.json['scan volume']['pixel time (ms)']*len(green)/1000 #in s

get_ipython().run_line_magic('matplotlib', 'qt5')

# find and save nt/pixel
ax = plt.imshow(green+red, vmax=25)
fig = plt.gcf()
plt.title("click top and bottom bead edges")
fig.canvas.draw()
pts = np.asarray(plt.ginput(n=2, show_clicks=True))
ntppixel = 48502/(max(pts[:,1])-min(pts[:,1]))
plt.close()

# find and save sections
sections = []
keepgoing = 1
mol = 1
clicked=[]
while keepgoing: 
    ax = plt.imshow(green+red, vmax=18)
    fig = plt.gcf()
    fig.canvas.draw()
    
    # click the ends of traces
    pts = np.asarray(plt.ginput(n=2, show_clicks=True))
    plt.close()
    clicked.append(pts)
    
    # convert the clicks
    tl = [math.floor(min(pts[:,0])),math.floor(min(pts[:,1]))]
    br = [math.floor(max(pts[:,0])),math.floor(max(pts[:,1]))]
    sections.append([tl[1],br[1],tl[0],br[0]])
    
    #approximate speed from clicks
    transloc_speed = ((br[1]-tl[1])*ntppixel)/((br[0]-tl[0])*linetime)
    
    #extend the section for a nice image
    sgreen = green[ext_neg(tl[1]):ext_pos(br[1],ym),ext_neg(tl[0]):ext_pos(br[0],xm)]
    sred = red[ext_neg(tl[1]):ext_pos(br[1],ym),ext_neg(tl[0]):ext_pos(br[0],xm)]
    
    #change the axes on the output plot
    extnt = [ext_neg(tl[0])*linetime,ext_pos(br[0],xm)*linetime,
             ext_neg(tl[1])*ntppixel/1000,ext_pos(br[1],ym)*ntppixel/1000]
    
    plt.figure(dpi=300)
    ax=plt.gca()
    ax.set_facecolor("black")
    plt.imshow(sred,cmap=cmapred,vmin=1,vmax=10,extent=extnt)
    plt.imshow(sgreen,cmap=cmapgreen,vmin=1,vmax=10,alpha=0.7,extent=extnt)
    #ax.set_aspect('auto')
    plt.xlabel("Time (s)",fontsize=12)
    plt.ylabel("Position (k nt)",fontsize=12)
    #plt.figtext(0.1,0.02,'Speed (nt/s) = '+str(round(transloc_speed)),wrap=True)
    #ttl = dirl[0:6] + ', kymo ' + k + ', section ' + str(mol)
    #plt.title(ttl)
    plt.tight_layout()
    plt.savefig(dire+newf+k+'-section '+str(mol)+'.png')
    plt.close()
    
    s = input("enter anything to end: ")
    if s:
        keepgoing = 0
    else:
        mol+=1
    
    
# save files
saveme=1
if saveme==1:
    finame2 = dire + newf + k + '-ntppixel.txt'
    np.savetxt(finame2,[ntppixel])
    finame1 = dire + newf + k + '-sections.txt'
    np.savetxt(finame1,sections)
    
get_ipython().run_line_magic('matplotlib', 'inline')

#%%
plt.figure()
plt.figtext(1,1.1,'hey')
