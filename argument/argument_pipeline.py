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

	if(getSpan(conn,wordList)==u'\u0906\u0917\u0947'):
		print "aage Feature",feature.featureList
	
#Setting feature class label
	arg1Span=wordList[conn[0]].arg1Span
	arg2Span=wordList[conn[0]].arg2Span
	argPos=studyArgumentPos(arg1Span,arg2Span)
	if(argPos=="arg2Before"):
		arg1SentenceNum=wordList[arg2Span[-1]].sentenceNum
	else:
		arg1SentenceNum=wordList[arg1Span[-1]].sentenceNum
	connSentenceNum=wordList[conn[0]].sentenceNum
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

def arg2TreePosition(arg2NodeList,connNode,nodeDict):

	arg2InConnSubTree=False
	arg2InInImmediateParent=False
	arg2InHigherLevel=False

	for node in arg2NodeList:
		if(findNode(node,connNode,nodeDict,0,15)):
			arg2InConnSubTree=True
	currNode=connNode
	iterationNum=0
	while(1):           
		parentNode=nodeDict[currNode].nodeParent
		print "parent",iterationNum,parentNode
		if(parentNode=="None"):
			break
		for node in arg2NodeList:
			if(findNode(node,parentNode,nodeDict,0,10,currNode)):
				if(iterationNum==0):
					arg2InInImmediateParent=True
				else:
					arg2InHigherLevel=True
		iterationNum+=1
		currNode=parentNode
	return (arg2InConnSubTree,arg2InInImmediateParent,arg2InHigherLevel)


def arg2SubTreeExtraction(conn,discourseFile):
	wordList=discourseFile.globalWordList
	sentenceList=discourseFile.sentenceList
	sentenceNum=wordList[conn[0]].sentenceNum
	sentence=sentenceList[sentenceNum]
	nodeDict=sentenceList[sentenceNum].nodeDict
	connective=getSpan(conn,wordList)
	print sentenceNum,discourseFile.rawFileName
	arg2Span=wordList[conn[0]].arg2Span
	arg1Span=wordList[conn[0]].arg1Span
	argPos=studyArgumentPos(arg1Span,arg2Span)
	if(argPos=="arg2Before"):
		print "changed",getSpan(conn,wordList)
		arg2Span=arg1Span
#	for pos in arg2Span:
#		print wordList[pos].word,
#	print ""
	arg2ChunkSpan=sorted(set([wordList[i].chunkNum for i in arg2Span]))
#	for pos in arg2ChunkSpan:
#		print sentence.chunkList[pos].chunkTag,
#	print ""
	arg2NodeList=[sentence.chunkList[chunkNum].nodeName for chunkNum in arg2ChunkSpan if chunkNum < len(sentenceList[sentenceNum].chunkList)]
	connNodeList=[sentence.chunkList[wordList[pos].chunkNum].nodeName for pos in conn]
	arg2NodeList=filter(lambda x: x!="BLK" and x not in connNodeList,arg2NodeList)
	for node in arg2NodeList:
		print node,
	print ""	
	connNode=sentence.chunkList[wordList[conn[-1]].chunkNum].nodeName

	print connNode
	feature=Feature("lists/compConnectiveList.list","lists/tagSet.list","lists/chunkSet.list",discourseFile.globalWordList,discourseFile.sentenceList,conn)

	feature.wordFeature(conn)
	feature.connectivePosInSentence(conn)
	feature.connLeafNode(connNode,nodeDict)
	feature.connSubTreeHasVGF(connNode,nodeDict)
	feature.connHasParentVGF(connNode,nodeDict)
	feature.rightWordLocation(conn,nodeDict[connNode],nodeDict[arg2NodeList[0]],nodeDict)
	print nodeDict[connNode].childList	
	


	#setting class label
	
	p=arg2TreePosition(arg2NodeList,connNode,nodeDict)
	print connective,p


	feature.setClassLabel(str(p[0])+str(p[1])+str(p[2]))	
	feature.sampleDescription["connective"]=connective
	feature.sampleDescription["leafNode"]=len(nodeDict[connNode].childList)
	feature.sampleDescription["label"]=feature.classLabel

	if p[0] and p[1] :
		print "HERE"

	if(p[0] and not p[1]): #and not p[1] and not p[2]'''):
		feature.setClassLabel("ConnSubTree")
#	elif(p[1] and p[1] and not p[2]):
#		feature.setClassLabel("ConSubTreeExtra")
	elif(not p[0] and p[1]):
		feature.setClassLabel("ParentSubTree")
	elif(p[0] and p[1]):
#		feature.setClassLabel("ConnAndParentSubTree")
		feature.setClassLabel("ConnSubTree")
	elif(not p[0] and not p[1] and p[2]):
		feature.setClassLabel("OtherSubTree")
	else:
		feature.setClassLabel("Other")
		print "nooooo"
#	elif(not p[0] and p[1] and p[2]):
#		feature.setClassLabel("ParentSubTreeExtra")
#	else:
#		feature.setClassLabel("Other")
	
	#setting up feature description

	feature.sampleDescription["connective"]=connective
	feature.sampleDescription["leafNode"]=len(nodeDict[connNode].childList)
	feature.sampleDescription["label"]=feature.classLabel


	return feature,arg2NodeList,connNode
def extractSubtree(connNode,position,nodeDict):


	nodes=[keys for keys,values in nodeDict ]
	
	subTree=[]
	if(position=="ConnSubTree"):
		for node in nodes:
			if(findNode(node,connNode,nodeDict,0,15)):
				subTree.append(node)
		return subTree

	elif(position=="ParentSubTree"):
		parentNode=nodeDict[connNode].nodeParent
		for node in nodes:
			if(findNode(node,parentNode,nodeDict,0,15) and not findNode(node,connNodeList,nodeDict,0,15)):
				subTree.append(node)
		return subTree
	

def arg2SubTreeRefinement(conn,discourseFile):
	wordList=discourseFile.globalWordList
	sentenceList=discourseFile.sentenceList
	sentenceNum=wordList[conn[0]].sentenceNum
	sentence=sentenceList[sentenceNum]
	nodeDict=sentenceList[sentenceNum].nodeDict
	connective=getSpan(conn,wordList)
	print sentenceNum,discourseFile.rawFileName
	arg2Span=wordList[conn[0]].arg2Span
	arg1Span=wordList[conn[0]].arg1Span
	argPos=studyArgumentPos(arg1Span,arg2Span)
	if(argPos=="arg2Before"):
		print "changed",getSpan(conn,wordList)
		arg2Span=arg1Span
#	for pos in arg2Span:
#		print wordList[pos].word,
#	print ""
	arg2ChunkSpan=sorted(set([wordList[i].chunkNum for i in arg2Span]))
#	for pos in arg2ChunkSpan:
#		print sentence.chunkList[pos].chunkTag,
#	print ""
	arg2NodeList=[sentence.chunkList[chunkNum].nodeName for chunkNum in arg2ChunkSpan if chunkNum < len(sentenceList[sentenceNum].chunkList)]
	connNodeList=[sentence.chunkList[wordList[pos].chunkNum].nodeName for pos in conn]
	arg2NodeList=filter(lambda x: x!="BLK" and x not in connNodeList,arg2NodeList)
	for node in arg2NodeList:
		print node,
	print ""	
	connNode=sentence.chunkList[wordList[conn[-1]].chunkNum].nodeName


	
connD={}


num=0;

arg1PosFeatureCollection=[]
arg2SubTreePosFeatureCollection=[]

arg2NodeCollection=[]

discourseFileNum=0

for discourseFileLocation in discourseFileCollection:
	discourseFile=loadModel(discourseFileLocation)
	wordList=discourseFile.globalWordList
	connList=findConnectives(discourseFile.globalWordList)
#	print len(connList)
	num+=len(connList)
	relationNum=0
	for conn in connList:
#		createConnWiseFolder(conn,discourseFile)
#		studyConnPos(conn,discourseFile)
#		studyconnArg2Pos(conn,wordList[conn[0]].arg2Span,discourseFile)
		arg2SubTreePosFeature,arg2NodeList,connNode=arg2SubTreeExtraction(conn,discourseFile)
		arg2SubTreePosFeatureCollection.append(arg2SubTreePosFeature)
		arg2NodeCollection.append((arg2NodeList,connNode,discourseFileNum))
		arg1PosFeature=generateArg1PositionFeatures(conn,discourseFile,relationNum)
		arg1PosFeatureCollection.append(arg1PosFeature)
		continue
		genArg1Span,genArg2Span=generate_baseline(conn,discourseFile.globalWordList)
		result=checkArgumentMatch(conn,genArg1Span,genArg2Span,discourseFile.globalWordList)
#		print "arg1",result[0]
#		print "arg2",result[1]
		print conn	
		print wordList[conn[0]].arg1Span
		print wordList[conn[0]].arg2Span
		for pos in conn:
			print wordList[pos].word+" ",
		print ""
		studyArgumentSpan(wordList[conn[0]].sentenceNum,wordList[conn[0]].arg1Span,wordList[conn[0]].arg2Span,wordList)
#		print "arg1",studyArgumentContinuity(wordList[conn[0]].arg1Span,wordList)
#		print "arg2",studyArgumentContinuity(wordList[conn[0]].arg2Span,wordList)
#		print studyArgumentPos(wordList[conn[0]].arg1Span,wordList[conn[0]].arg2Span)
		relationNum+=1
	discourseFileNum+=1
'''
sortedList=sorted(connD.items(), key=operator.itemgetter(1))
sortedList.reverse()
n=0
for i in sortedList:
	print i[0],i[1]
	n+=i[1]
print n
FD=open("connPos","w")
for connective,pos in d.iteritems():
	FD.write(connective+" num: "+str(len(pos.keys()))+"\n")
	for k,v in pos.iteritems():
		FD.write(str(k)+"-"+str(v)+" ")
	FD.write("\n")
FD.close()
'''

exportModel("./features/arg1PosFeatureCollection",arg1PosFeatureCollection)

coll=loadModel("./features/arg1PosFeatureCollection")
for feature in coll:
	print "arg1",feature.classLabel


#exportModel("./features/arg2SubTreePosFeatureCollection",arg2SubTreePosFeatureCollection)

for i in range(0,10):
	classifier=getModel(arg2SubTreePosFeatureCollection,i,10)
