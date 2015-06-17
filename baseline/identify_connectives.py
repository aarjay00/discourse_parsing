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

def searchSplitConn(conn1,conn2,wordList,sentenceList):
	conn1=conn1.split()
	conn2=conn2.split()
	posList=[]
	for sentence in sentenceList:
		p1=[]
		wordPos=sentence.wordNumList[0]
		while(wordPos < sentence.wordNumList[-1]-len(conn1)+2):
			found=True
			for j in range(0,len(conn1)):
				if(conn1[j]!=wordList[wordPos+j].word):
					found=False
					break
			if(found):
				p1.append(wordPos)
				wordPos+=len(conn1)
			else:
			 	wordPos+=1
		if(len(p1)==0):
			continue
		p2=[]
		wordPos=sentence.wordNumList[0]
		while(wordPos < sentence.wordNumList[-1]-len(conn2)+2):
			found=True
			for j in range(0,len(conn2)):
				if(conn2[j]!=wordList[wordPos+j].word):
					found=False
					break
			if(found):
				p2.append(wordPos)
				wordPos+=len(conn2)
			else:
			 	wordPos+=1
		if(len(p2)==0):
			continue
		for i in p1:
		 	for j in p2:
				if(i+len(conn1)<=j):
					posList.append((i,j))
	return posList


def convert_span(i,conn):
	l=[]
	for j in range(i,i+len(conn.split())):
		l.append(j)
	return l
def identifyConnectives(discourseFileInst,connList,connSplitList):
	positiveSetSingle=[]
	negativeSetSingle=[]
	wordList=discourseFileInst.globalWordList
	sentenceList=discourseFileInst.sentenceList
	for conn in connList:
		posList=searchConn(conn,wordList)
		if(len(posList)==0):
			continue
#		print "found ",conn,len(posList)
		for i in posList:
#			for j in range(i,i+len(conn.split())):
#				print wordList[j].chunkNum,
#			print "\n"
			if(wordList[i].conn):
				positiveSetSingle.append(convert_span(i,conn))
#				print "Yes",wordList[i].sense
			else:
				negativeSetSingle.append(convert_span(i,conn))
#			 	print "No"
	positiveSetSplit=[]
	negativeSetSplit=[]
	for conn in connSplitList:
		conn1,conn2=conn[0],conn[1]
		posList=searchSplitConn(conn1,conn2,wordList,sentenceList)
		if(len(posList)==0):
			continue
		for i,j in posList:
		 	if(not (wordList[i].splitConn and wordList[j].splitConn)):
				negativeSetSplit.append((convert_span(i,conn1),convert_span(j,conn2)))
			elif((i==0 or wordList[i-1].splitConn) or (i==len(wordList)-1 or wordList[i+1].splitConn)):
				print "Split",len(positiveSetSplit),len(negativeSetSplit)
				negativeSetSplit.append((convert_span(i,conn1),convert_span(j,conn2)))
			else:
				positiveSetSplit.append((convert_span(i,conn1),convert_span(j,conn2)))

	return (positiveSetSingle,negativeSetSingle,positiveSetSplit,negativeSetSplit)
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

def genFeatureSplitConn(conn,label,discourseFile):
		print "conn","-"*30,
		for p in conn[0]:
			print discourseFile.globalWordList[p].word,
		print "---",
		for p in conn[1]:
			print discourseFile.globalWordList[p].word,
		feature=Feature("lists/splitConnectiveList.list","lists/tagSet.list","lists/chunkSet.list",discourseFile,discourseFile.globalWordList,discourseFile.sentenceList,conn)
		feature.wordFeature(conn[0])
		feature.wordFeature(conn[1])
		feature.tagFeature(conn[0])
		feature.tagFeature(conn[1])
		feature.tagNeighbor(conn[0],-1)
		feature.tagNeighbor(conn[1],1)
		feature.chunkFeature(conn[0])
		feature.chunkFeature(conn[1])
		feature.chunkNeighbor(conn[0],1)
		feature.chunkNeighbor(conn[0],2)
#		feature.chunkNeighbor(conn[0],-1)
		feature.chunkNeighbor(conn[1],-1)
		feature.chunkNeighbor(conn[1],-2)
#		feature.chunkNeighbor(conn[1],1)
		feature.setClassLabel(label)
		return feature

	
connList=loadConnList("lists/compConnectiveList.list")
connSplitList=loadConnList("lists/splitConnectiveList.list",True)


discourseFileCollection=loadModel("processedData/annotatedData")
print len(discourseFileCollection)
positiveSet=[]
negativeSet=[]
positiveSetSplit=[]
negativeSetSplit=[]
fileNum=0
featureCollectionSingle=[]
featureCollectionSplit=[]
for discourseFile in discourseFileCollection:
	for sentence in discourseFile.sentenceList:
		chunkNum=0
		for chunk in sentence.chunkList:
			for word in chunk.wordNumList:
				print discourseFile.globalWordList[word].word,
			print chunk.chunkTag+"0",chunkNum,
			chunkNum+=1
		print "\n"
	pSet,nSet,pSetSplit,nSetSplit=identifyConnectives(discourseFile,connList,connSplitList)
	for conn in pSet:
		featureCollectionSingle.append(genFeatureSingleConn(conn,"Yes",discourseFile))
	for conn in nSet:
		featureCollectionSingle.append(genFeatureSingleConn(conn,"No",discourseFile))
	for conn in pSetSplit:
		featureCollectionSplit.append(genFeatureSplitConn(conn,"Yes",discourseFile))
	for conn in nSetSplit:
		featureCollectionSplit.append(genFeatureSplitConn(conn,"No",discourseFile))
	positiveSet.extend(pSet)
	negativeSet.extend(nSet)
	positiveSetSplit.extend(pSetSplit)
	negativeSetSplit.extend(nSetSplit)
	fileNum+=1
print len(positiveSetSplit),len(negativeSetSplit)
print len(positiveSet),len(negativeSet)
print len(featureCollectionSingle)


a=0.0
b=0.0
c=0.0
d=0.0
time=100
for i in range(0,time):
#	x,y,z,l=runModel(featureCollectionSplit,8,1,1)
	x,y,z,l=runModel(featureCollectionSingle,15,1,1)
	a+=x
	b+=y
	c+=z
	d+=l
print a/time,b/time,c/time,d/time
