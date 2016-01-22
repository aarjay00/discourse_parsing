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

from tree_api import *

from argument_match_accuracy import *

connList=loadConnList("lists/compConnectiveList.list")
connSplitList=loadConnList("lists/splitConnectiveList.list",True)


from os import listdir
from os.path import isfile, join
discourseFileCollection= [ "./processedData/collection/"+str(f) for f in listdir("./processedData/collection/") if isfile(join("./processedData/collection",f)) ]
discourseFileCollection=folderWalk("./processedData/collection/")




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


def arg1Pos(conn,discourseFile):
	wordList=discourseFile.globalWordList
	arg1Span=wordList[conn[0]].arg1Span
	arg2Span=wordList[conn[0]].arg2Span


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



num=0;

arg1PosFeatureCollection=[]
for discourseFileLocation in discourseFileCollection:
	discourseFile=loadModel(discourseFileLocation)
	wordList=discourseFile.globalWordList
	connList=findConnectives(discourseFile.globalWordList)
	print len(connList)
	num+=len(connList)
	relationNum=0
	for conn in connList:
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

exportModel("./features/arg1PosFeatureCollection",arg1PosFeatureCollection)

print num
