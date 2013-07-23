#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import pagination
from __future__ import division
import os
import sys
import csv
import numpy as np
import pandas as pd
import pandas.io.ga as ga
from pandas import *
from time import sleep
#import oct2py as op
from datetime import timedelta
from decimal import Decimal
import math
import pdb
from collections import Counter
from decimal import *
import csv
import time
import imp
from dateutil import parser
import math


t = datetime.today()

yesterday = t - timedelta(1)
dbyy = t - timedelta(2)

end = yesterday.strftime('%Y-%m-%d')
dbz = dbyy.strftime('%Y-%m-%d')

max_results = 5e5
metrics = ['pageviews']
dimensions = ['date','pagePath']
filters = ['pagePath=~^/foreign-travel-advice/']

for yy in range(0,2):
	
	if yy == 0:
		start_date = end
		end_date = end
	else:
		start_date = dbz
		end_date = dbz

	print "Start Date: %s " % (start_date)
	print "End Date: %s " % (end_date)

	df1 = ga.read_ga(metrics,
					 dimensions = dimensions,
					 start_date = start_date, 
					 end_date = start_date, 
					 token_file_name = '/Users/danielcollins/Documents/GA Python/analytics.dat',
					 filters = filters,
				 
					 )

	dby= df1.sort(['pageviews'], ascending=[0,1])
	# 
	# df2 = ga.read_ga(metrics,
	#                  dimensions = dimensions,
	#                  start_date = end_date, 
	#                  end_date = end_date, 
	#                  token_file_name = '/Users/danielcollins/Documents/GA Python/analytics.dat',
	#                  filters = filters,
	#                  
	#                  )
	# 
	# y = df2.sort(['pageviews'], ascending=[0,1])

	G = []
	for i in dby.index:
		if (str(i).count('/') == 2):
			G.append(i)
	HH = dby.ix[G]		

	if yy == 0:
		l = HH['pageviews']>=100
	else:
		l = HH['pageviews']>=10
	l2 = np.where(l==True)
	TT = list(l2[0])		
	DD = HH.ix[TT]

	IM = []
	for i in DD.index:
		IM.append(str(i[1].split('/')[2]))

	IT = []
	for j in IM:
		IT.append(str.upper(j[0][0])+ j[1:len(j)])

	DD.index = IT
	if yy == 0:
		yx = DD
	else:
		yb = DD

#yx  Yesterday		
#yb  dbyy


ybf = yb.ix[yx.index]	
yx['pageviews_dby'] = ybf['pageviews']	
yx['pct_change'] = np.round((yx.icol(0)-yx.icol(1))*100/yx.icol(0),1)

pth = '/Users/danielcollins/Documents/FCO2/'

CC = pd.read_csv(pth+'cities.csv')

II = []
for i in CC['country']:
	j = i.lower()
	II.append(j)

CC.index = II
T = [y.lower() for y in yx.index]
yx.index = T
# CC.index = CC['country']
L = CC.join(yx)
del L['country']
L.index = CC['country']
L.to_csv(pth+'World_Visits.csv')








t = datetime.today()

yesterday = t - timedelta(1)
dbyy = t - timedelta(14)

end = yesterday.strftime('%Y-%m-%d')
dbz = dbyy.strftime('%Y-%m-%d')

max_results = 1e6
metrics = ['pageviews']
dimensions = ['date','pagePath']
filters = ['pagePath=~^/foreign-travel-advice/']

start = dbyy.strftime('%Y-%m-%d')
end = end

print "Start Date: %s " % (start)
print "End Date: %s " % (end)

df1 = ga.read_ga(metrics,
				 dimensions = dimensions,
				 start_date = start, 
				 end_date = end, 
				 token_file_name = '/Users/danielcollins/Documents/GA Python/analytics.dat',
				 filters = filters,
			 	 max_results=max_results,        
                 chunksize=5000
                 )
				 

df1_conc = pd.concat([x for x in df1])

# dby= df1_conc.sort(['date'], ascending=[0,1])


G = []
for i in df1_conc.index:
	if (str(i).count('/') == 2):
		G.append(i)
HH = df1_conc.ix[G]

YY = HH.ix[HH.index[len(HH.index)-1][0]]
l = YY['pageviews']>100
l2 = np.where(l==True)
TT = list(l2[0])		
DD = YY.ix[TT]   

#  DD is list of countries fulfilling > 100 views yesterday - reference
QQ = HH.unstack()
w2 = []

w = ([('pageviews', x) for x in DD.index])
A = QQ[w]
T = [str.split(str(x[1]), '/')[2] for x in A.columns]
# A.to_csv('Quick.csv')
A.columns = [x.title() for x in T]
A = A.rename(columns={'Usa':'USA'})
A.to_csv(pth+'Quick.csv')


II = pd.read_csv(pth+'World_Visits.csv')
JJ = pd.read_csv(pth+'Quick.csv')

for g in JJ.columns:
	II[g] = JJ[g]
II.to_csv(pth+'WV2.csv')



