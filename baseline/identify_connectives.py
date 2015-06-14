#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
from util import *
from extract_relations import *
from ssf_api import *
from letter import *
from merge_annotations import *
from annotated_data import *
from feature import *

def searchConn(conn,wordList):
	conn=conn.split()
	pos=0
	posList=[]
	while(pos<len(wordList)-len(conn)+1):
		found=True
		for j in range(0,len(conn)):
			if(conn[j]!=wordList[pos+j].word):
				found=False
				break
		if(found):
			posList.append(pos)
			pos+=len(conn)
		else:
			pos+=1
	return posList

def identifyConnectives(discourseFileInst,connList,connSplitList):
	positiveSet=[]
	negativeSet=[]
	wordList=discourseFileInst.globalWordList
	for conn in connList:
		posList=searchConn(conn,wordList)
		if(len(posList)>0):
			print "found ",conn,len(posList)
			for i in posList:
#				for j in range(i,i+len(conn.split())):
#					print wordList[j].chunkNum,
#				print "\n"
				if(wordList[i].conn):
					connSpan=[]
					for i in range(i,i+len(conn.split())):
						connSpan.append(i)
					positiveSet.append(connSpan)
					print "Yes",wordList[i].sense
				else:
					connSpan=[]
					for i in range(i,i+len(conn.split())):
						connSpan.append(i)
					negativeSet.append(connSpan)
				 	print "No"
	return (positiveSet,negativeSet)
def genFeatureSingleConn(conn,label,discoureFile):
		print "conn","-"*30,
		for p in conn:
			print discourseFile.globalWordList[p].word,
		print "\n"
		feature=Feature("lists/compConnectiveList.list","lists/tagSet.list","lists/chunkSet.list",discourseFile.globalWordList,discourseFile.sentenceList)
		feature.wordFeature(conn)
		feature.tagFeature(conn)
		feature.chunkFeature(conn)
		feature.chunkNeighbor(conn,1)
		feature.chunkNeighbor(conn,-1)
		feature.chunkNeighbor(conn,2)
		feature.chunkNeighbor(conn,-2)
		feature.setClassLabel(label)
		print feature.featureVector
		return feature

	
connList=loadConnList("lists/compConnectiveList.list")
connSplitList=loadConnList("lists/splitConnectiveList.list",True)


discourseFileCollection=loadModel("processedData/annotatedData")
print len(discourseFileCollection)
positiveSet=[]
negativeSet=[]
fileNum=0
featureCollection=[]
for discourseFile in discourseFileCollection:
	for sentence in discourseFile.sentenceList:
		chunkNum=0
		for chunk in sentence.chunkList:
			for word in chunk.wordNumList:
				print discourseFile.globalWordList[word].word,
			print chunk.chunkTag+"0",chunkNum,
			chunkNum+=1
		print "\n"
	pSet,nSet=identifyConnectives(discourseFile,connList,connSplitList)
	for conn in pSet:
		featureCollection.append(genFeatureSingleConn(conn,"Yes",discourseFile))
	for conn in nSet:
		featureCollection.append(genFeatureSingleConn(conn,"No",discourseFile))
	positiveSet.extend(pSet)
	negativeSet.extend(nSet)
	fileNum+=1
print len(positiveSet),len(negativeSet)
print len(featureCollection)

from sklearn.linear_model import LogisticRegression as maxent
from random import shuffle

shuffle(featureCollection)

cycleLen=20
avgPrecision=0.0
avgRecall=0.0
for i in range(0,cycleLen):
	print "Iteration",i,"-"*50
	size=len(featureCollection)/cycleLen
	start=size*i
	end=start+size
#	print start,end
	test=featureCollection[start:end]
	train=featureCollection[:start]+featureCollection[end+1:]
#	print len(test),len(train)

	dataSet,dataLabels=convertDataSet(train)

	model=maxent()
	model.fit(dataSet,dataLabels)


	truePositives=0
	falsePositives=0
	trueNegatives=0
	falseNegatives=0

	d,l=convertDataSet(test)
	print "model score",model.score(d,l)

	for feature in test:
		arr=numpy.array(feature.featureVector)
		result=model.predict(arr)[0]
#	print "Model",result
#	print "Gold",feature.classLabel
		if(result==feature.classLabel):
			if(feature.classLabel=="Yes"):
				truePositives+=1
			else:
				trueNegatives+=1
		else:
			if(feature.classLabel=="Yes"):
				falseNegatives+=1
			else:
				falsePositives+=1
	print truePositives,falsePositives,trueNegatives,falseNegatives
	precision=(1.0*truePositives)/(truePositives+falsePositives)
	recall=(1.0*truePositives)/(truePositives+falseNegatives)
	print "Precision : %f Recall %f"%(precision,recall)
	avgPrecision=(avgPrecision*i + precision)/(i+1)
	avgRecall=(avgRecall*i + recall)/(i+1)
print "Final",avgPrecision,avgRecall

FD=open("results.txt","a")
FD.write(str(avgPrecision)+" "+str(avgRecall)+"\n")
FD.close()
