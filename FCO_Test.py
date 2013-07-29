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

Stand = []

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
	
	G = []
	REF = []
	xv = []
	TS = dby.index[0][0]
	for i in dby.index:
		if (str(i).count('/') == 2):
			G.append(i[1])
	HH = dby.ix[G]	


# 	if yy == 0:
	FF = []
	for i in dby.index:

		try:
			GH = str(i[1])
			if (GH.count('/') < 4 and GH.count('.') == 0 and GH.count('\'') == 0 and GH.count(':') < 1 and GH.count('=') < 1 and GH.count('xad') < 1 and GH.find('print')<0):
				FF.append(GH)
			else:
				print 'check'
				xv.append((i))
		except:
			print 'problem:', i
			xv.append(i) 		

	for i in G:
		I = [x.startswith(i) for x in FF]
		U = np.where(np.array(I)==True)
		REF.append(U[0])

	# 	QT = np.array(FF)

	dbv = dby.drop(xv) 
	dbv.ix[REF[0]]# Egypt for example

	II = []
	TT = DataFrame(np.zeros([len(REF), 11]))
	PC = DataFrame(np.zeros([len(REF), 11]))

	for j in range(0, len(REF)):
		if (len(REF[j]) > 0):
			jj = str(dbv.ix[REF[j]].index[0][1].split('/')[2])
			II.append(jj.lower())
		else:
			II.append('NULL')

	TT.index = II
	PC.index = II

	TT.columns = ['summary','entry-requirements', 'safety-and-security','health', 'money', 'terrorism', 'local-laws-and-customs', 'natural-disasters','contact-fco-travel-advice-team', 'arctic-travel', 'sahel-region']
	PC.columns = TT.columns

	for i in range(0, len(REF)):
		S = dbv.ix[REF[i]]
		for k in range(0,len(S)):
			if (k == 0):

				TT.ix[i,0] = dbv.ix[dbv.ix[REF[i]].index[0]].values[0]
			else:
				try:
					AV = str(S.index.values[k][1].split('/')[3]) == TT.columns
				except: 
					print 'Weird'

				BV = np.where(AV == True)
				if (len(BV[0])>0):
					BV = BV[0][0]
					TT.ix[i,BV] = dbv.ix[dbv.ix[REF[i]].index[k]].values[0]
				else:
					print TT.columns[k]
					TT.ix[i,k] = 0
				
	for v in range(0,len(REF)):
		Q = np.sum(TT.ix[v])
		PC.ix[v] = np.round((TT.ix[v]*100/Q),1)

	Sd = np.std(PC['contact-fco-travel-advice-team'])			
	Stand.append(Sd)
	Lxc = np.where(PC['contact-fco-travel-advice-team'] > 2*Sd)	 	
		 	
	
	
	
	TT['pageviews'] = TT.sum(axis=1)
	FH = TT.ix[Lxc[0],0]
	for i in range(0,len(FH)):
		FH.ix[i] = 1
	FH.name = 'HighCFCO'
		
	TT['HighCFCO'] = FH
	
	if yy == 0:
		Yest = TT
		YestPCT = PC
	else:
		DBY = TT
		DBPCT = PC
		
		
# //////////////////////////////////////////////////////////////////////////////////////
	
U = Yest['summary'] > 100
U2 = np.where(U==True)

Y2 = Yest.ix[U2[0]]	
Y2['index'] = Y2.index
Y2.drop_duplicates(cols='index', take_last=False, inplace=True)
del Y2['index']

P2 = YestPCT.ix[U2[0]]
P2['index'] = P2.index
P2.drop_duplicates(cols='index', take_last=False, inplace=True)
del P2['index']

#  Day Before - filter indices and remove duplicates /////////////////////////////////

DBY2 = DBY.ix[P2.index]
DBY2['index'] = DBY2.index
DBY2.drop_duplicates(cols='index', take_last=False, inplace=True)
del DBY2['index']

DBP = DBPCT.ix[P2.index]
DBP['index'] = DBP.index
DBP.drop_duplicates(cols='index', take_last=False, inplace=True)
del DBP['index']

# Y2 Yesterday Entries
# P2 Yesterday Percentage share

# DBY2 day before Entries
# DBP day before Percentage share

P2['pageviews'] = Y2['pageviews']
P2['pageviews_dby'] = DBY2['pageviews']
P2['pct_change'] = np.round((100*(P2['pageviews']-P2['pageviews_dby']))/(P2['pageviews_dby']),1) 
P2['HighCFCO'] = Y2['HighCFCO']

 
P2['MedSum'] = np.median(P2['summary'])
P2['Med_Entreq'] = np.median(P2['entry-requirements'])
P2['MedSS'] = np.median(P2['safety-and-security'])
P2['MedHealth'] = np.median(P2['health'])
P2['MedMoney'] = np.median(P2['money'])
P2['MedTerror'] = np.median(P2['terrorism'])
P2['MedLocal'] = np.median(P2['local-laws-and-customs'])
P2['MedNatural'] = np.median(P2['natural-disasters'])
P2['MedContact'] = np.median(P2['contact-fco-travel-advice-team'])
P2['MedArctic'] = np.median(P2['arctic-travel'])
P2['MedSahel'] = np.median(P2['sahel-region'])





pth = '/Users/danielcollins/Documents/FCO2/'
pth2 = '/Users/danielcollins/Documents/FCO_local/' 

CC = pd.read_csv(pth+'cities.csv')

II = []
for i in CC['country']:
	j = i.lower()
	if (j  == 'south-korea '):
		j = 'south-korea'
	II.append(j)

CC.index = II
L = CC.join(P2)
del L['country']

L.index = CC['country']
L.to_csv(pth+'World_VisitsTEST.csv')

 
# // Very lazy - pasting code snippets. Information id duplicated in the two GA calls.



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
l = YY['pageviews']>=100
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
# A = A.rename(columns={'Usa':'USA'})
FF = np.where(A.columns=='Usa')
GG = np.where(A.columns=='Bosnia-And-Herzegovina')
xc = A.columns
xc.values[FF[0]] = 'USA'
if (GG[0]>0):
	xc.values[GG[0]] = 'Bosnia-and-Herzegovina'
A.columns = xc
A.to_csv(pth+'QuickTEST.csv')


II = pd.read_csv(pth+'World_VisitsTEST.csv')
JJ = pd.read_csv(pth+'QuickTEST.csv')

for g in JJ.columns:
	II[g] = JJ[g]

WW = II.rename(columns={'entry-requirements': 'ERQ', 'safety-and-security': 'SAS','local-laws-and-customs': "LLC", 'natural-disasters': 'ND','contact-fco-travel-advice-team': 'CFTA', 'arctic-travel':'ARC', 'sahel-region': "SAHEL"})
	
SD = 2*np.std(WW.icol(12))

for i in range(0,len(WW)):
	if (WW.ix[i,12] > SD):
		WW.ix[i,18] = 1

WW.to_csv(pth+'WV2TEST.csv')
WW.to_csv(pth2+'WV2TESTL.csv')


