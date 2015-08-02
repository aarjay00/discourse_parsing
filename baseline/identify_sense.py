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

def searchConn(wordList):
	wordPos=0
	posList=[]
	while(wordPos<len(wordList)):
		if(not wordList[wordPos].conn):
			wordPos+=1
			continue
		l=[]
		while(wordList[wordPos].conn):
			l.append(wordPos)
			wordPos+=1
		posList.append(l)
		wordPos+=1
	return posList

def searchSplitConn(wordList,sentenceList):
	posList=[]
	for sentence in sentenceList:
		p1=[]
		wordPos=sentence.wordNumList[0]
		while(wordPos < sentence.wordNumList[-1]):
			if(not wordList[wordPos].splitConn):
				wordPos+=1
				continue
			l=[]
			while(wordList[wordPos].splitConn):
				l.append(wordPos)
				wordPos+=1
			p1.append(l)
		for i in p1:
		 	for j in p1:
				if(i[0] != j[0] and wordList[i[0]].relationNum==wordList[j[0]].relationNum):
					posList.append((i,j))
	return posList

def identifyConnectives(discourseFileInst,connList,connSplitList):
	positiveSetSingle=[]
	negativeSetSingle=[]
	wordList=discourseFileInst.globalWordList
	sentenceList=discourseFileInst.sentenceList
	
	connSingleSet=[]
	connSplitSet=[]

	connSingleSet=searchConn(wordList)
	connSplitSet=searchSplitConn(wordList,sentenceList)

	return (connSingleSet,connSplitSet)

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
#		feature.aurFeature(conn)
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
#		feature.tagNeighbor(conn[0],-1)
#		feature.tagNeighbor(conn[1],1)
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
connSingleSet=[]
connSplitSet=[]
	
fileNum=0
featureCollectionSingle=[]
featureCollectionSplit=[]
for discourseFile in discourseFileCollection:
#	for sentence in discourseFile.sentenceList:
#		chunkNum=0
#		for chunk in sentence.chunkList:
#			for word in chunk.wordNumList:
#				print discourseFile.globalWordList[word].word,
#			print chunk.chunkTag+"0",chunkNum,
#			chunkNum+=1
#		print "\n"
	singleSet,splitSet=identifyConnectives(discourseFile,connList,connSplitList)
	wordList=discourseFile.globalWordList
	sentenceList=discourseFile.sentenceList
	print discourseFile.rawFileName,"-"*100
	for conn in singleSet:
		word=wordList[conn[0]]
		print word.word
		arg1Span= word.arg1Span
		arg2Span= word.arg2Span
		chunkList=sentenceList[word.sentenceNum].chunkList
#		print arg1Span
		print "-"*60
		print "arg1","-"*10
		for pos in arg1Span:
			print wordList[pos].word,wordList[pos].wordTag,
		print ""
		for pos in  arg1Span:
#		print sentenceList[wordList[pos].sentenceNum].chunkList[wordList[pos].chunkNum].chunkTag,
			if(wordList[pos].wordTag=="VM"):
				print wordList[pos].word
				try:
					print wordList[pos].featureSet.featureDict["af"],"----",wordList[pos].extraFeatureSet.featureDict.get("vpos"),"----",wordList[pos].extraFeatureSet.featureDict.get("af")
				except:
					print "XXX"
		print ""
		print "arg2","-"*10
		for pos in arg2Span:
			print wordList[pos].word,
		print ""
		for pos in  arg2Span:
			if(wordList[pos].wordTag=="VM"):
				print wordList[pos].word
				try:
					print wordList[pos].featureSet.featureDict["af"],"----",wordList[pos].extraFeatureSet.featureDict.get("vpos"),"----",wordList[pos].extraFeatureSet.featureDict.get("af")
				except:
					print "XXX"
#			print sentenceList[wordList[pos].sentenceNum].chunkList[wordList[pos].chunkNum].chunkTag,wordList[pos].wordTag,
		print ""
		if(wordList[conn[0]].sense.split(".")[0]=="_Without_sense"):
			continue
#		featureCollectionSingle.append(genFeatureSingleConn(conn,(wordList[conn[0]].sense).split(".")[0],discourseFile))
	connSingleSet.extend(singleSet)
	connSplitSet.extend(splitSet)
	fileNum+=1

print len(connSingleSet),len(connSplitSet)

category=[]
gender=[]
number=[]
person=[]
case=[]

for discourseFile in discourseFileCollection:
	wordList=discourseFile.globalWordList
	for word in wordList:
		tam=word.featureSet.featureDict["af"].split(",")
		try:
			if tam[1] not in category and tam[1]!="":
				category.append(tam[1])
			if tam[2] not in gender and tam[2]!="":
				gender.append(tam[2])
			if tam[3] not in number and tam[3]!="":
				number.append(tam[3])
			if tam[4] not in person and tam[4]!="":
				person.append(tam[4])
			if tam[5] not in case and tam[5]!="":
				case.append(tam[5])
		except:
			print "here here"
			print word.word,word.featureSet.featureDict["af"]
print "category"
for i in category:
	print i
print "gender"
for i in gender:
	print i
print "number"
for i in number:
	print i
print "person"
for i in person:
	print i
print "case"
for i in case:
	print i


exit()
classList=[]
for feature in featureCollectionSingle:
	classList.append(feature.classLabel)
classList=list(set(classList))
print classList


a=0.0
b=0.0
c=0.0
d=0.0
max_acc=-1
min_acc=100
max_precision=-1
min_precision=100
time=1
for i in range(0,time):
	#x,y,z,l=runModel(featureCollectionSplit,8,1,1)
	x,y,z,l=runModel(featureCollectionSingle,classList,10,1,1)
	a+=x
	b+=y
	c+=z
	d+=l
	max_acc=max(max_acc,z)
	min_acc=min(min_acc,z)
	max_precision=max(max_precision,l)
	min_precision=min(min_precision,l)
print "Accuracy",max_acc,"-",min_acc
print "F-measure",max_precision,"-",min_precision
print a/time,b/time,c/time,d/time
