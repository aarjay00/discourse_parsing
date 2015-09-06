#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")

from os import listdir
from os.path import isfile, join
import numpy
from sklearn.linear_model import LogisticRegression as maxent
from sklearn.feature_selection import RFE
from sklearn.feature_selection import chi2

dirPath="./featureDist/"

onlyfiles = [ f for f in listdir(dirPath) if isfile(join(dirPath,f)) ]
FD=codecs.open("lists/connSpecDependency.list","w")
FD.close()

for i in onlyfiles:
	if("_" in i):
		continue
	print "opening",i
	FD=codecs.open(dirPath+i,"r")
	dic={}
	label=""
	samples=0
	p=0
	n=0
	coll=[]
	s=[]
	featureslist=[]
	for line in FD.readlines():
		line=line[:-1]
		l=line.split(":")
		if(l[0]=="Label"):
			if(l[1]=="Yes"):
				p+=1
			if(l[1]=="No"):
				n+=1
			samples+=1
			if(s!=[]):		
				coll.append((label,s))
			s=[]
			label=l[1]
			continue
		else:
			if(line not in dic):
				dic[line]={"Yes":0,"No":0}
			dic[line][label]+=1
			s.append(line)
			featureslist.append(line)
	coll.append((label,s))
	FD.close()


	numberOfFeatures=3
	if(p==0 or n==0):
		FD=codecs.open("lists/connSpecDependency.list","a")
		FD.write("conn:"+i+"\n")
		for i in range(0,numberOfFeatures):
			FD.write("noFeature"+str(i)+"\n")
		FD.close()
		continue
	print "Analysis--------------------"
	print p,n
	FD=codecs.open("lists/connSpecDependency.list","a")
	FD.write("conn:"+i+"\n")
	featureslist=list(set(featureslist))
	arrC=[]
	labelC=[]
	for c in coll:
		arr=[]
		for f in featureslist:
			if(f in c[1]):
				arr.append(1)
			else:
				arr.append(0)
#		print arr
		arrC.append(numpy.array(arr))
		labelC.append(c[0])
	model=maxent(solver='liblinear')
	rfe=RFE(model,numberOfFeatures)
	rfe=rfe.fit(arrC,labelC)
	c2,pval=chi2(arrC,labelC)
#	print c2
#	print rfe.support_
#	print rfe.ranking_
	iterator=0
	for i in rfe.ranking_:
		if(i==1):
			print featureslist[iterator],i,c2[iterator],pval[iterator]
			FD.write(featureslist[iterator]+"\n")
		iterator+=1
	FD.close()
#	model.fit(arrC,labelC)
		


	continue
	FD=codecs.open(dirPath+i+"_analysis","w")
	FD.write("number of samlpes "+str(samples)+"\n" )
	usefull=[]
	for x,y in dic.items():
		FD.write(x+" "+str(y["Yes"])+" "+str(y["No"])+"\n")
		if(y["Yes"]==p and y["No"]==n):
			continue
		usefull.append(x)
	FD.write("usefull"+str(len(usefull))+"\n")
	for x in usefull:
		FD.write(x+"\n")
	FD.close()
