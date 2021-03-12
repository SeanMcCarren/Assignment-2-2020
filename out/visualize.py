'''
visualize the obtained results
'''

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy import cumsum
import seaborn as sns
from matplotlib.patches import Rectangle
import matplotlib.lines as lines
import subprocess
import os
import json
import csv

# READ DATA
import store

LOCs = store.LOCStore()
RESULTS = store.Results()

releases = []
with open('/usr/jquery-data/jquery_releases.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        releases.append(row)

# Testing on partial dataset? Cut part out!
#releases = releases[:17]

# Releases is reversed? So reverse it back!
releases = releases[::-1]

matrix = np.empty((len(releases), len(releases)), dtype=float)
matrix[:,:] = np.NaN
#print(RESULTS.get('1.11.0', '1.4.2'))
for i_1, release_1 in enumerate(releases):
    for i_2, release_2 in enumerate(releases[:i_1]):
        tag_1 = release_1['tag']
        tag_2 = release_2['tag']
        try:
            matrix[i_1, i_2] = RESULTS.get(tag_1, tag_2)
        except:
            matrix[i_1, i_2] = 0
        
locs = np.array([LOCs.get(r['tag']) for r in releases])

label_names = [r['tag'] for r in releases]

#Get color distribution
#c_map = plt.get_cmap('Blues')
c_map = matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","cyan","lightgreen","yellow","red"])

#create the figure for the heasmap
fig, axes = plt.subplots(2, figsize=(20,40))

#compute where the rectangle start
box_start = np.union1d([0],cumsum(locs))
s = sum(locs)

# Make the lines inbetween the boxes.
for i, p in enumerate(box_start):
    if ( i < len(label_names) and (label_names[i].split('.')[1] != label_names[i-1 if i-1 >0 else 0].split('.')[1])):
        axes[0].add_line(lines.Line2D([0, s], [p, p], linewidth = 1.2, color = 'black'))
        axes[0].add_line(lines.Line2D([p, p], [0, s], linewidth = 1.2, color = 'black'))
    else:
        axes[0].add_line(lines.Line2D([0, s], [p, p], linewidth = 1, color = 'grey'))
        axes[0].add_line(lines.Line2D([p, p], [0, s], linewidth = 1, color = 'grey'))

# Make all the boxes
for c in range(len(locs)):
    for r in range(len(locs)):
        if (c>r):
            rect = Rectangle((box_start[r],box_start[c]),locs[r],locs[c],linewidth=1,edgecolor=None,facecolor=c_map(matrix[c,r]))
            axes[0].add_patch(rect)

# this is for the legend
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))
            
# Setup the labels
axes[0].set_ylim([0,s])   
axes[0].set_xlim([0, s])
axes[0].invert_yaxis()
axes[0].set_xticks(box_start[:-1]+0.5*locs) #put labels in the middle of the box
axes[0].set_yticks(box_start[:-1]+0.5*locs)
axes[0].set_xticklabels(label_names, rotation = 90)
axes[0].set_yticklabels(label_names)
axes[0].grid(False)

# Setup the legend
axes[1].imshow(gradient, aspect = '5', cmap=c_map)
axes[1].grid(False)
axes[1].set_xticks([0,254])
axes[1].set_yticks([]) 
axes[1].set_xticklabels(['0','1'])

plt.savefig('heatmap.png')

# For the barplot
keys = [key for key in LOCs.DONE][::-1]
vals = [LOCs.DONE[key] for key in keys]
plt.figure()

fig = plt.figure(figsize = (15,8))
ax = plt.gca()
ax.yaxis.grid(True)
# creating the bar plot
plt.bar(keys, vals)
plt.xticks(rotation='vertical')
plt.xlabel('Version')
plt.ylabel('Lines of JavaScript')
plt.savefig('barplot.png')