#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
import subprocess
import operator
from util import *
from extract_relations import *
from ssf_api import *
from letter import *
from merge_annotations import *
from annotated_data import *
from feature import *
from render_dependency_tree_api import *
from tree_api import *

from argument_match_accuracy import *
from argument_experiments import *

from model_api import *
from crf_api import *
connList=loadConnList("lists/compConnectiveList.list")
connSplitList=loadConnList("lists/splitConnectiveList.list",True)


from os import listdir
from os.path import isfile, join
discourseFileCollection= [ "./processedData/collection/"+str(f) for f in listdir("./processedData/collection/") if isfile(join("./processedData/collection",f)) ]
discourseFileCollection=folderWalk("./processedData/collection/")

	
def generate_baseline(conn,wordList):
	genArg1Span=[]
	genArg2Span=[]
	pos=conn[-1]+1
	while(pos<len(wordList) and wordList[conn[-1]].sentenceNum==wordList[pos].sentenceNum):
		genArg2Span.append(pos)
		pos+=1
	sentenceBegin=False
	if(wordList[conn[0]].sentenceNum!=wordList[conn[0]-1].sentenceNum or wordList[conn[0]].sentenceNum!=wordList[conn[0]-2].sentenceNum):
		sentenceBegin=True
#	if(sentenceBegin):
 	pos=conn[0]-1
	while(pos>=0 and wordList[pos].sentenceNum==wordList[conn[0]-1].sentenceNum):
		genArg1Span.append(pos)
		pos-=1
	return (genArg1Span,genArg2Span)

def generateArg1PositionFeatures(conn,discourseFile,relationNum):
	sentenceList=discourseFile.sentenceList
	wordList=discourseFile.globalWordList

	feature=Feature("lists/compConnectiveList.list","lists/tagSet.list","lists/chunkSet.list",discourseFile.globalWordList,discourseFile.sentenceList,conn)

	feature.wordFeature(conn)
	feature.tagFeature(conn)
	feature.chunkFeature(conn)
	p=feature.connectivePosInSentence(conn)
	c=feature.numberOfChunksBeforeConn(conn)

#Setting feature class label
	arg1Span=wordList[conn[0]].arg1Span
	arg2Span=wordList[conn[0]].arg2Span
	argPos=studyArgumentPos(arg1Span,arg2Span)
	if(argPos=="arg2Before"):
		arg1SentenceNum=wordList[arg2Span[-1]].sentenceNum
	else:
		arg1SentenceNum=wordList[arg1Span[-1]].sentenceNum
	connSentenceNum=wordList[conn[-1]].sentenceNum
	if(arg1SentenceNum==connSentenceNum):	
		feature.setClassLabel("Same-Sentence")
	else:
	 	feature.setClassLabel("Prev-Sentence")
#setting sample descritption:

	feature.sampleDescription["connective"]=getSpan(conn,wordList)
	feature.sampleDescription["connective label"]=feature.classLabel
	feature.sampleDescription["rawFileName"]=discourseFile.rawFileName
	feature.sampleDescription["relationNum"]=relationNum
	feature.sampleDescription["number of chunks before conn"]=c
	feature.sampleDescription["connPos"]=p
	 
	return feature

def argTreePosition(argNodeList,connNode,nodeDict):

	argInConnSubTree=False
	argInInImmediateParent=False
	argInHigherLevel=False

	for node in argNodeList:
		if(findNode(node,connNode,nodeDict,0,15)):
			argInConnSubTree=True
	currNode=connNode
	iterationNum=0
	while(1):           
		parentNode=nodeDict[currNode].nodeParent
		if(parentNode=="None"):
			break
		for node in argNodeList:
			if(findNode(node,parentNode,nodeDict,0,10,currNode)):
				if(iterationNum==0):
					argInInImmediateParent=True
				else:
					argInHigherLevel=True
		iterationNum+=1
		currNode=parentNode
	return (argInConnSubTree,argInInImmediateParent,argInHigherLevel)

def arg1SubTreeExtraction(relationNum,discourseFileNum):
	discourseFile=loadModel(discourseFileCollection[discourseFileNum])
	conn=findConnectives(discourseFile.globalWordList)[relationNum]
	wordList=discourseFile.globalWordList
	sentence=discourseFile.sentenceList[wordList[conn[-1]].sentenceNum]

	nodeDict=sentence.nodeDict
	connNode=sentence.chunkList[wordList[conn[-1]].chunkNum].nodeName

	arg2Span=wordList[conn[0]].arg2Span
	arg1Span=wordList[conn[0]].arg1Span
	argPos=studyArgumentPos(arg1Span,arg2Span)
	if(argPos=="arg2Before"):
#		print "changed",getSpan(conn,wordList)
		arg1Span,arg2Span=arg2Span,arg1Span

	connNodeList=[sentence.chunkList[wordList[pos].chunkNum].nodeName for pos in conn]
	
	arg2ChunkSpan=sorted(set([wordList[i].chunkNum for i in arg2Span]))
	arg2NodeList=[sentence.chunkList[chunkNum].nodeName for chunkNum in arg2ChunkSpan if chunkNum < len(sentence.chunkList)]
	arg2NodeList=filter(lambda x: x!="BLK" and x not in connNodeList,arg2NodeList)

	
	
	arg1ChunkSpan=sorted(set([wordList[i].chunkNum for i in arg1Span]))
	arg1NodeList=[sentence.chunkList[chunkNum].nodeName for chunkNum in arg1ChunkSpan if chunkNum < len(sentence.chunkList)]
	arg1NodeList=filter(lambda x: x!="BLK" and x not in connNodeList,arg1NodeList)
	
	feature=Feature("lists/compConnectiveList.list","lists/tagSet.list","lists/chunkSet.list",discourseFile.globalWordList,discourseFile.sentenceList,conn)

	feature.wordFeature(conn)
	feature.connLeafNode(connNode,nodeDict)
	feature.arg2Position(connNode,argTreePosition(arg2NodeList,connNode,nodeDict))
	feature.connParent(connNode,nodeDict)
	feature.connParentParent(connNode,nodeDict)
	feature.connTwoClause(connNode,nodeDict)
	feature.hasParent(nodeDict[connNode],nodeDict)
	feature.hasParentParent(nodeDict[connNode],nodeDict)

	arg1Presence=argTreePosition(arg1NodeList,connNode,nodeDict)

	'''
	if(arg1Presence[0] and not arg1Presence[1] and not arg1Presence[2]):
		print getSpan(conn,wordList),"ConnSubTree"
		feature.setClassLabel("ConnSubTree")
	elif(not arg1Presence[0] and arg1Presence[1] and not arg1Presence[2]):
		print getSpan(conn,wordList),"ParentSubTree"
		feature.setClassLabel("ParentVGF")
	elif(arg1Presence[2]):
		print getSpan(conn,wordList),"ParentParentSubTree"
		feature.setClassLabel("ParentParentVGF")
	'''

	if(arg1Presence[0]):
		feature.setClassLabel("ConnSubTree")
		print getSpan(conn,wordList),"ConnSubTree"
	elif(arg1Presence[1]):
		print getSpan(conn,wordList),"ParentSubTree"
		feature.setClassLabel("ParentVGF")
	else:
		print getSpan(conn,wordList),"ParentParentSubTree"
		feature.setClassLabel("ParentParentVGF")


	for f in feature.featureList:
		feature.sampleDescription[f[0]]=f[1]

	return feature

discourseFileNum=0

connD={}

arg1PosFeatureCollection=[]
arg1ConnInfoCollection=[]
for discourseFileLocation in discourseFileCollection:
	discourseFile=loadModel(discourseFileLocation)
	wordList=discourseFile.globalWordList
	connList=findConnectives(discourseFile.globalWordList)
	relationNum=0
	for conn in connList:
		arg1PosFeature=generateArg1PositionFeatures(conn,discourseFile,relationNum)
		arg1PosFeatureCollection.append(arg1PosFeature)
		connective=getSpan(conn,wordList)
		sentenceNum=wordList[conn[-1]].sentenceNum
		if(connective not in connD):
			connD[connective]=0
		else:
		 	connD[connective]+=1

		arg1ConnInfoCollection.append((discourseFileNum,relationNum))
		relationNum+=1
	discourseFileNum+=1



arg1SSInfoCollection=[]
arg1PSInfoCollection=[]
for iterationNum in range(0,10):
	dataSize=len(arg1PosFeatureCollection)
	start=iterationNum*(dataSize/10)
	end=start+(dataSize/10)
	results=singleIterationClassify(arg1PosFeatureCollection,iterationNum,10)

	for sampleNum in range(start,end):
	
		discourseFileNum=arg1ConnInfoCollection[sampleNum][0]
		relationNum=arg1ConnInfoCollection[sampleNum][1]
		discourseFile=loadModel(discourseFileCollection[discourseFileNum])
		conn=findConnectives(discourseFile.globalWordList)[relationNum]
		wordList=discourseFile.globalWordList
		sentenceList=discourseFile.sentenceList
		sentenceNum=wordList[conn[-1]].sentenceNum
		nodeDict=sentenceList[sentenceNum].nodeDict
		connNode=sentenceList[sentenceNum].chunkList[wordList[conn[-1]].chunkNum].nodeName
	
		arg1Span=wordList[conn[0]].arg1Span
		arg2Span=wordList[conn[0]].arg2Span
		argPos=studyArgumentPos(arg1Span,arg2Span)
	        if(argPos=="arg2Before"):
#			print "changed",getSpan(conn,wordList)
			arg1Span,arg2Span=arg2Span,arg1Span

		arg1NodeList=[(sentenceList[wordList[pos].sentenceNum].chunkList[wordList[pos].chunkNum].nodeName,pos) for pos in arg1Span]
		arg1NodeList=filter(lambda x : x[0]!="BLK",arg1NodeList)

		arg1NodeList=[(sentenceList[wordList[node[1]].sentenceNum].nodeDict[node[0]],node[1]) for node in arg1NodeList]

		arg1Pos=results[sampleNum-start]

		if(results[sampleNum-start]=="Prev-Sentence"):
			arg1PSInfoCollection.append((arg1NodeList,sampleNum))
		else:
			arg1SSInfoCollection.append((arg1NodeList,sampleNum))
'''
createDirectory("./processedData/arg1SSInfoCollection/")
for fileNum in range(0,len(arg1SSInfoCollection)):
	exportModel("./processedData/arg1SSInfoCollection/"+str(fileNum),arg1SSInfoCollection[fileNum])
createDirectory("./processedData/arg1PSInfoCollection/")
for fileNum in range(0,len(arg1PSInfoCollection)):
	exportModel("processedData/arg1PSInfoCollection/"+str(fileNum),arg1PSInfoCollection[fileNum])
'''

arg1SSSubTreeFeatureCollection=[]

for num in range(0,len(arg1SSInfoCollection)):
	

	sampleNum=arg1SSInfoCollection[num][1]
	discourseFileNum=arg1ConnInfoCollection[sampleNum][0]
	relationNum=arg1ConnInfoCollection[sampleNum][1]
	arg1SSSubTreeFeature=arg1SubTreeExtraction(relationNum,discourseFileNum)
	arg1SSSubTreeFeatureCollection.append(arg1SSSubTreeFeature)

runFeatureCombination(arg1SSSubTreeFeatureCollection,False)
