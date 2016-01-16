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
	




num=0;
for discourseFileLocation in discourseFileCollection:
	discourseFile=loadModel(discourseFileLocation)
	connList=findConnectives(discourseFile.globalWordList)
	print len(connList)
	num+=len(connList)
	for conn in connList:
		genArg1Span,genArg2Span=generate_baseline(conn,discourseFile.globalWordList)
		result=checkArgumentMatch(conn,genArg1Span,genArg2Span,discourseFile.globalWordList)
		print "arg1",result[0]
		print "arg2",result[1]
		print genArg1Span,discourseFile.globalWordList[conn[0]].arg1Span
		print genArg2Span,discourseFile.globalWordList[conn[0]].arg2Span

print num
