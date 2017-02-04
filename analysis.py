# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 13:29:47 2017

@author: L
"""
import random
import numpy as np
import cPickle
from collections import defaultdict
import sys, re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

city = "chengdu2"
fileName = "%s.txt"%(city)
df = pd.read_csv(fileName, header=None, sep=',')
state = ["city","district","name","lng","lat","privice"]

df.columns = state

#district stsat describe
#this will return a Series Object
df_stat = df['privice'].groupby(df['district'])
describe = df_stat.describe().to_dict()
means = df_stat.mean().to_dict()

describeAll = df['privice'].describe().to_dict()
describeAllNew = {}
for key in describeAll:
    describeAllNew[('全市',key)] = describeAll[key]

means['全市'] = df['privice'].mean()
#plot means
sorted_means =  sorted(means.iteritems(), key=lambda d:d[1], reverse = True )

districtArray = []
stdArray = []
priviceArray = []
countArray = []
for item in sorted_means:
    district = item[0]
    privice = item[1]
    districtArray.insert(0,district)
    priviceArray.insert(0,privice)
    countArray.insert(0,counts[district])
    stdArray.insert(0,std[district])
N = len(priviceArray)
ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars
fig, ax = plt.subplots()
rects1 = ax.bar(ind, priviceArray, width, color='darkorange')

right_data = countArray
axf = ax.twinx()
print len(ax.get_xticks())
print len(right_data)
rects2 = axf.plot(ind, right_data, color='forestgreen')
#axf.set_ylim((0, 20))
axf.set_ylabel('房屋数量/套')
axf.set_ylim(0,4000)

ax.set_xlabel('地区')
ax.set_ylabel('均价/元')
ax.set_title('成都市各区2017年1月二手房房屋均价--房屋数量')
ax.set_xticks(ind+width)
ax.set_xticklabels( districtArray )
def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')
def autolabel_line(rects):
    # attach some text labels
    for rect in rects:
        print rect.get_ydata()
        X = rect.get_xdata()
        Y = rect.get_ydata()
        for x,y in zip(X,Y):
            axf.text(x, 1.01*y, '%d'%int(y),color='forestgreen',
                ha='center', va='bottom')
                
autolabel(rects1)
autolabel_line(rects2)
plt.style.use('ggplot')
plt.show()


boxData = []
boxLables = []
for item in sorted_means:
    district1 = item[0]
    if district1 != '全市' :
        print district1
        df_tmp = df.ix[df.district==district1]
        data = df_tmp['privice'].values
        boxData.append(data)
        boxLables.append(district1) 
    else:
        data = df['privice'].values
        boxData.append(data)
        boxLables.append('全市')
        
fig, ax = plt.subplots()
ax.boxplot((boxData),labels=(boxLables))
ax.set_xlabel('地区')
ax.set_ylabel('价格(/元)')
ax.set_title('成都市各区2017年1月二手房房屋价格统计')
plt.style.use('ggplot')
ax.show()





