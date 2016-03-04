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



from os import listdir
from os.path import isfile, join




def findConnectives(wordList):
	connList=[]
	conn=[]
	wordNum=-1
	for word in wordList:
		wordNum+=1
		if not word.conn:
			continue
		if(len(conn)!=0 and conn[-1]!=wordNum-1):
			connList.append(conn)
			conn=[]
		conn.append(wordNum)
	if(len(conn)!=0):
		connList.append(conn)
	return connList
		
		
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
def studyArgumentPos(arg1Span,arg2Span):

	arg1Before=True
	arg2Before=True
	for pos2 in arg2Span:
		for pos1 in arg1Span:
			if(pos2<pos1):
				arg1Before=False
	for pos1 in arg1Span:
		for pos2 in arg2Span:
			if(pos1<pos2):
				arg2Before=False
	if(arg1Before):
		return "arg1Before"
	if(arg2Before):
		return "arg2Before"
	return "argOverLap"

def studyArgumentSpan(connSentenceNum,arg1Span,arg2Span,wordList):
	argPos=studyArgumentPos(arg1Span,arg2Span)
	if(argPos=="arg2Before"):
		arg1Span,arg2Span=arg2Span,arg1Span
	arg1Sentence=sorted(set([wordList[pos].sentenceNum for pos in arg1Span]))
	arg2Sentence=sorted(set([wordList[pos].sentenceNum for pos in arg2Span]))

	try:
		if(wordList[arg1Span[0]].sentenceNum!=wordList[arg1Span[1]].sentenceNum):
			arg1Sentence.remove(wordList[arg1Span[0]].sentenceNum)
	except:
		print "ISSUE"
		pass
	try:
		if(wordList[arg2Span[0]].sentenceNum!=wordList[arg2Span[1]].sentenceNum):
			arg2Sentence.remove(wordList[arg2Span[0]].sentenceNum)
	except:
		print "ISSUE"
		pass
	try:
		if(wordList[arg1Span[-1]].sentenceNum!=wordList[arg1Span[-2]].sentenceNum):
			arg1Sentence.remove(wordList[arg1Span[-1]].sentenceNum)
	except:
		print "ISSUE"
		pass
	try:
		if(wordList[arg2Span[-1]].sentenceNum!=wordList[arg2Span[-2]].sentenceNum):
			arg2Sentence.remove(wordList[arg2Span[-1]].sentenceNum)
	except:
		print "ISSUE"
		pass

	print "lenArg1",len(arg1Sentence),connSentenceNum==arg1Sentence[0],arg1Sentence,connSentenceNum
	print "lenArg2",len(arg2Sentence),connSentenceNum==arg2Sentence[0],arg2Sentence,connSentenceNum

	for pos in arg1Span:
		print wordList[pos].word,
	print ""
	for pos in arg2Span:
		print wordList[pos].word,
	print ""

def studyArgumentContinuity(argSpan,wordList):
	if(len(set(argSpan))!=argSpan[-1]-argSpan[0]+1):
		return "discontinuos"
	return "continuos"



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


d={}

def studyConnPos(conn,discourseFile):
	wordList=discourseFile.globalWordList
	sentenceList=discourseFile.sentenceList
	connective=getSpan(conn,wordList)
	connSentenceNum=wordList[conn[0]].sentenceNum
	connChunkNum=wordList[conn[0]].chunkNum
	connSentence=sentenceList[connSentenceNum]
	connChunk=connSentence.chunkList[connChunkNum]
	node=connSentence.nodeDict[connChunk.nodeName]
	c=len(node.childList)
	print c,connective,node.nodeName
	if(connective not in d.keys()):
		d[connective]={}
	if(c not in d[connective].keys()):
		d[connective][c]=0
	d[connective][len(node.childList)]+=1


def studyconnArg2Pos(conn,arg2Span,discourseFile):
	wordList=discourseFile.globalWordList
	sentenceList=discourseFile.sentenceList
	connective=getSpan(conn,wordList)
	connSentenceNum=wordList[conn[0]].sentenceNum
	connChunkNum=wordList[conn[0]].chunkNum
	connSentence=sentenceList[connSentenceNum]
	connChunk=connSentence.chunkList[connChunkNum]
	connNode=connSentence.nodeDict[connChunk.nodeName]
	arg2Nodes=[]
	for pos in arg2Span:
		word=wordList[pos]
		sentence=sentenceList[word.sentenceNum]
		node=sentence.nodeDict[sentence.chunkList[word.chunkNum].nodeName]
		arg2Nodes.append(node)
	arg2Nodes=set(arg2Nodes)
	children=0
	parent=0
	for node in arg2Nodes:
		if(isParent(connNode,node,connSentence.nodeDict)):
			children+=1
		try:
			if(isParent(node,connNode,connSentence.nodeDict)):
				parent+=1
		except:
		  	print "hmm"
	print "connarg2-",getSpan(conn,wordList),len(arg2Nodes),children,parent

connDict={}

def createConnWiseFolderArg2(conn,discourseFile):
	wordList=discourseFile.globalWordList
	sentenceList=discourseFile.sentenceList
	sentenceNum=wordList[conn[0]].sentenceNum
	connective=getSpan(conn,wordList)
	arg2Span=wordList[conn[0]].arg2Span
	arg1Span=wordList[conn[0]].arg1Span
	argPos=studyArgumentPos(arg1Span,arg2Span)
	if(argPos=="arg2Before"):
		print "changed",getSpan(conn,wordList)
		arg2Span=arg1Span
	arg2ChunkSpan=sorted(set([wordList[i].chunkNum for i in arg2Span]))
	arg2NodeList=[sentenceList[sentenceNum].chunkList[chunkNum].nodeName for chunkNum in arg2ChunkSpan if chunkNum < len(sentenceList[sentenceNum].chunkList)]
	global connDict
	createDirectory("./connwiseArgument2/"+connective+"/")
	if(connective not in connDict):
		connDict[connective]=0
		FD=open("./connwiseArgument2/"+connective+"/desc","w")
		FD.close()
	rootNode=sentenceList[sentenceNum].rootNode
	nodeDict=sentenceList[sentenceNum].nodeDict
	graph = pydot.Dot(graph_type='graph')
	if(len(rootNode)>1):
		print connective
	render_dependency_tree_highlighted(rootNode[0],nodeDict,graph,sentenceList[sentenceNum],wordList,arg2NodeList,"./connwiseArgument2/"+connective+"/"+str(connDict[connective]))
	FD=open("./connwiseArgument2/"+connective+"/desc","a")
	FD.write(str(connDict[connective])+" - "+str(sentenceNum)+" "+discourseFile.rawFileName+"\n")
	FD.close()
	connDict[connective]+=1

def createConnWiseFolderArg1(conn,discourseFile):
	wordList=discourseFile.globalWordList
	sentenceList=discourseFile.sentenceList
	sentenceNum=wordList[conn[0]].sentenceNum
	connective=getSpan(conn,wordList)
	arg2Span=wordList[conn[0]].arg2Span
	arg1Span=wordList[conn[0]].arg1Span
	argPos=studyArgumentPos(arg1Span,arg2Span)
	if(argPos=="arg2Before"):
		print "changed",getSpan(conn,wordList)
		arg1Span=arg2Span
	for pos in arg1Span:
		if wordList[pos].sentenceNum!=sentenceNum:
			return
	print "arg1 in same sentence"

	arg1ChunkSpan=sorted(set([wordList[i].chunkNum for i in arg1Span]))
	arg1NodeList=[sentenceList[sentenceNum].chunkList[chunkNum].nodeName for chunkNum in arg1ChunkSpan if chunkNum < len(sentenceList[sentenceNum].chunkList)]
	global connDict
	createDirectory("./connwiseArgument1/"+connective+"/")
	if(connective not in connDict):
		connDict[connective]=0
		FD=open("./connwiseArgument1/"+connective+"/desc","w")
		FD.close()
	rootNode=sentenceList[sentenceNum].rootNode
	nodeDict=sentenceList[sentenceNum].nodeDict
	graph = pydot.Dot(graph_type='graph')
	if(len(rootNode)>1):
		print connective
	render_dependency_tree_highlighted(rootNode[0],nodeDict,graph,sentenceList[sentenceNum],wordList,arg1NodeList,"./connwiseArgument1/"+connective+"/"+str(connDict[connective]))
	FD=open("./connwiseArgument1/"+connective+"/desc","a")
	FD.write(str(connDict[connective])+" - "+str(sentenceNum)+" "+discourseFile.rawFileName+"\n")
	FD.close()
	connDict[connective]+=1
	connDict[connective]+=1

def createConnWiseFolderArg1PrevSentence(conn,discourseFile):
	wordList=discourseFile.globalWordList
	sentenceList=discourseFile.sentenceList
	sentenceNum=wordList[conn[0]].sentenceNum
	connective=getSpan(conn,wordList)
	arg2Span=wordList[conn[0]].arg2Span
	arg1Span=wordList[conn[0]].arg1Span
	argPos=studyArgumentPos(arg1Span,arg2Span)
	if(argPos=="arg2Before"):
		print "changed",getSpan(conn,wordList)
		arg1Span=arg2Span
	for pos in arg1Span:
		if wordList[pos].sentenceNum+1!=sentenceNum:
			return
	print "arg1 in entirely in prev sentence"

	arg1ChunkSpan=sorted(set([wordList[i].chunkNum for i in arg1Span]))
	arg1NodeList=[sentenceList[sentenceNum-1].chunkList[chunkNum].nodeName for chunkNum in arg1ChunkSpan if chunkNum < len(sentenceList[sentenceNum-1].chunkList)]
	global connDict
	createDirectory("./connwiseArgument1Prev/"+connective+"/")
	if(connective not in connDict):
		connDict[connective]=0
		FD=open("./connwiseArgument1Prev/"+connective+"/desc","w")
		FD.close()
	rootNode=sentenceList[sentenceNum-1].rootNode
	nodeDict=sentenceList[sentenceNum-1].nodeDict
	graph = pydot.Dot(graph_type='graph')
	if(len(rootNode)>1):
		print connective
	render_dependency_tree_highlighted(rootNode[0],nodeDict,graph,sentenceList[sentenceNum-1],wordList,arg1NodeList,"./connwiseArgument1Prev/"+connective+"/"+str(connDict[connective]))
	FD=open("./connwiseArgument1Prev/"+connective+"/desc","a")
	FD.write(str(connDict[connective])+" - "+str(sentenceNum)+" "+discourseFile.rawFileName+"\n")
	FD.close()
	connDict[connective]+=1



num=0;


def getPartialMatchArgAccuracy(argResult,argGold):
	
	size=len(argGold)
	score=0

	common=set(argResult) & set(argGold)
	score+=len(common)
	score = score - .5*abs(len(set(argGold)) - len(common)) # nodes not included in final arg
	score = score - .5*abs(len(set(argResult)) - len(common)) # nodes extra in final arg
	score=(score*1.0)/size
	return score
'''

connList=loadConnList("lists/compConnectiveList.list")
connSplitList=loadConnList("lists/splitConnectiveList.list",True)


discourseFileCollection= [ "./processedData/collection/"+str(f) for f in listdir("./processedData/collection/") if isfile(join("./processedData/collection",f)) ]
discourseFileCollection=folderWalk("./processedData/collection/")

arg1PosFeatureCollection=[]
for discourseFileLocation in discourseFileCollection:
	discourseFile=loadModel(discourseFileLocation)
	wordList=discourseFile.globalWordList
	connList=findConnectives(discourseFile.globalWordList)
#	print len(connList)
	num+=len(connList)
	relationNum=0
	for conn in connList:
		createConnWiseFolder(conn,discourseFile)
#		studyConnPos(conn,discourseFile)
#		studyconnArg2Pos(conn,wordList[conn[0]].arg2Span,discourseFile)
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
		arg1PosFeature=generateArg1PositionFeatures(conn,discourseFile,relationNum)
		arg1PosFeatureCollection.append(arg1PosFeature)
		relationNum+=1

sortedList=sorted(connDict.items(), key=operator.itemgetter(1))
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

exportModel("./features/arg1PosFeatureCollection",arg1PosFeatureCollection)

print num
'''
