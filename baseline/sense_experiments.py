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
		wordList=discourseFile.globalWordList
		sentenceList=discourseFile.sentenceList
		print "conn","-"*30,
		for p in conn:
			print discourseFile.globalWordList[p].word,
		print "\n"
	
		feature=Feature("lists/compConnectiveList.list","lists/tagSet.list","lists/chunkSet.list",discourseFile,discourseFile.globalWordList,discourseFile.sentenceList,conn)
		feature.wordFeature(conn)
		feature.tagFeature(conn)
#		feature.chunkSeqFeature(getChunkSeq(wordList[conn[0]].arg1Span,wordList,sentenceList))
#		feature.chunkSeqFeature(getChunkSeq(wordList[conn[0]].arg2Span,wordList,sentenceList))
#		feature.dependencySeqFeature(getDependencySeq(wordList[conn[0]].arg1Span,wordList,sentenceList))
#		feature.dependencySeqFeature(getDependencySeq(wordList[conn[0]].arg2Span,wordList,sentenceList))
#		feature.tagNeighbor(conn,-1)
		feature.tagNeighbor(conn,1)
#		feature.tagNeighbor(conn,-2)
		feature.tagNeighbor(conn,2)
		feature.chunkFeature(conn)
		feature.chunkNeighbor(conn,1)
#		feature.chunkNeighbor(conn,-1)
		feature.chunkNeighbor(conn,2)
#		feature.chunkNeighbor(conn,-2)
		feature.setClassLabel(label)
#		feature.aurFeature(conn)
#		print feature.featureVector
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
featureDescSingleCollection=[]
featureDescSplitCollection=[]
chunkSeqLen1=0.0
chunkSeqLen2=0.0
max1=-1
min1=100
max2=-1
min2=100
i=0
for discourseFile in discourseFileCollection:
	singleSet,splitSet=identifyConnectives(discourseFile,connList,connSplitList)
	wordList=discourseFile.globalWordList
	sentenceList=discourseFile.sentenceList
	print discourseFile.rawFileName,"-"*100
	for conn in singleSet:
		chunkSeqLen1=(chunkSeqLen1*i+1.0*len(getChunkSeq(wordList[conn[0]].arg1Span,wordList,sentenceList)))/(i+1)
		chunkSeqLen2=(chunkSeqLen2*i+1.0*len(getChunkSeq(wordList[conn[0]].arg2Span,wordList,sentenceList)))/(i+1)
		i+=1
		max1=max(max1,len(getChunkSeq(wordList[conn[0]].arg1Span,wordList,sentenceList)))
		min1=min(min1,len(getChunkSeq(wordList[conn[0]].arg1Span,wordList,sentenceList)))
		max2=max(max2,len(getChunkSeq(wordList[conn[0]].arg2Span,wordList,sentenceList)))
		min2=min(min2,len(getChunkSeq(wordList[conn[0]].arg2Span,wordList,sentenceList)))
		word=wordList[conn[0]]
		print word.word
		arg1Span= word.arg1Span
		arg2Span= word.arg2Span
		chunkList=sentenceList[word.sentenceNum].chunkList
		print "-"*60
		print "arg1","-"*10
		for pos in arg1Span:
			print wordList[pos].word,wordList[pos].wordTag,
		print ""
		
		
		print "arg2","-"*10
		for pos in arg2Span:
			print wordList[pos].word,
		print ""
		connective=getSpan(conn,wordList)
		if(wordList[conn[0]].sense.split(".")[0]=="_Without_sense"):
			continue
		print "getaaa",connective.replace(" ","_"),wordList[conn[0]].sense.split(".")[0]
		featureCollectionSingle.append(genFeatureSingleConn(conn,(wordList[conn[0]].sense).split(".")[0],discourseFile))
		featureDescInst=featureDesc(discourseFile.rawFileName,wordList[conn[0]].sentenceNum,"Single Connective Sense Identification",wordList[conn[0]].sense,len(featureDescSingleCollection))
		featureDescInst.addAttr("singleConnectiveName",getSpan(conn,wordList))
		featureDescInst.addAttr("Arg1",getSpan(word.arg1Span,wordList))
		featureDescInst.addAttr("Arg1SentenceNum",wordList[word.arg1Span[0]].sentenceNum)
		featureDescInst.addAttr("Arg2",getSpan(word.arg2Span,wordList))
		featureDescInst.addAttr("Arg2SentenceNum",wordList[word.arg2Span[0]].sentenceNum)
		featureDescSingleCollection.append(featureDescInst)
	connSingleSet.extend(singleSet)
	connSplitSet.extend(splitSet)
	fileNum+=1

print len(connSingleSet),len(connSplitSet)

extraFeatureList=removeExtraFeatures(featureCollectionSingle)
for featureNum in range(0,len(featureCollectionSingle)):
	featureCollectionSingle[featureNum].cleanFeature(extraFeatureList)
print "featureSize",len(featureCollectionSingle[0].featureVector)



#code to print out filename wrt to sensese	
#dic={}
#for featureDescInst in featureDescSingleCollection:
#	if(featureDescInst.classLabel.split(".")[0] not in dic):
#		dic[featureDescInst.classLabel.split(".")[0]]=[]
#	dic[featureDescInst.classLabel.split(".")[0]].append(featureDescInst)
#for key in dic.keys():
#	FD=open(key+"_files","w")
#	for f in dic[key]:
#		f.printFeatureDesc(FD)
#		FD.write("-"*100+"\n")
#	FD.close()
#---------------------------------------------

#exit()

print "avgLen",chunkSeqLen1
print "avgLen",chunkSeqLen2
print "minmax",min1,max1
print "minmax",min2,max2

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
time=20
accuracyFinal={}
accuracyMax={}
accuracyMin={}
for iteration in range(0,time):
	print "running"
	#x,y,z,l=runModel(featureCollectionSplit,8,1,1)
	x, y, z, err, corr, extra=runModel(featureCollectionSingle,featureDescSingleCollection,classList,"sense_identification",15,1,1)
	for key in x.keys():
		if(key not in accuracyFinal):
			accuracyFinal[key]=0.0
			accuracyMax[key]=-1.0
			accuracyMin[key]=101.0
		accuracyFinal[key]=(accuracyFinal[key]*iteration+x[key])/(iteration+1)
		accuracyMin[key]=min(accuracyMin[key],x[key])
		accuracyMax[key]=max(accuracyMax[key],x[key])

for key in accuracyFinal.keys():
	print key
	print accuracyMin[key],"-",accuracyMax[key]," Avg-",accuracyFinal[key]
