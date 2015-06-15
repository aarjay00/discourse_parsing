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
from models import *

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
def genFeatureSingleConn(conn,label,discourseFile):
		print "conn","-"*30,
		for p in conn:
			print discourseFile.globalWordList[p].word,
		print "\n"
		feature=Feature("lists/compConnectiveList.list","lists/tagSet.list","lists/chunkSet.list",discourseFile,discourseFile.globalWordList,discourseFile.sentenceList,conn)
		feature.wordFeature(conn)
		feature.tagFeature(conn)
		feature.tagNeighbor(conn,-1)
		feature.tagNeighbor(conn,1)
		feature.tagNeighbor(conn,-2)
		feature.tagNeighbor(conn,2)
		feature.chunkFeature(conn)
		feature.chunkNeighbor(conn,1)
		feature.chunkNeighbor(conn,-1)
		feature.chunkNeighbor(conn,2)
		feature.chunkNeighbor(conn,-2)
		feature.setClassLabel(label)
		feature.aurFeature(conn)
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

runModel(featureCollection,5)
