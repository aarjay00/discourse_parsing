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




discourseFileCollection=loadModel("processedData/annotatedData")


def completeChunk(posList,wordList):
	start=False
	end=False
	if(posList[0]==0 or wordList[posList[0]-1].chunkNum!=wordList[posList[0]].chunkNum):
		start=True
	if(posList[-1]==len(wordList)-1 or wordList[posList[-1]+1].chunkNum!=wordList[posList[-1]].chunkNum):
		end=True
	return (start,end)
def convertPostList(posList,wordList):
	span=""
	for pos in posList:
		span=span+" " + wordList[pos].word
	return span[1:]
def print_span(posList,wordList):
	for pos in posList:
		print wordList[pos].word,wordList[pos].chunkNum,
	print ""

connList=loadConnList("lists/compConnectiveList.list")

for discourseFileInst in discourseFileCollection:
	print "-"*60
	relationList=discourseFileInst.relationList
	wordList=discourseFileInst.globalWordList
	sentenceList=discourseFileInst.sentenceList
	for relation in relationList:
		if(relation.relationType!="Explicit"):
			continue
		print relation.relationType
		print "Arg1",relation.arg1List
		print "conn",relation.connList
		print "Arg2",relation.arg2List
		if(wordList[relation.connList[0]].conn):
			print "Single Conn",
			if(convertPostList(relation.connList,wordList) in connList):
				print "Yes",
			else:
			 	print "No",wordList[relation.connList[0]-1].word,convertPostList(relation.connList,wordList) ,wordList[relation.connList[-1]+1].word,
		if(wordList[relation.connList[0]].splitConn):
			print "Split Conn",
		if(relation.arg1List[0] < relation.connList[0] and relation.connList[0]<relation.arg2List[0]):
			print "Case 1"
		elif(relation.connList[0] < relation.arg1List[0] and relation.arg1List[0]<relation.arg2List[0]):
			print "Case 2"
			print_span(sentenceList[wordList[relation.arg2List[0]].sentenceNum].wordNumList,wordList)
		elif(relation.connList[0] < relation.arg2List[0] and relation.arg2List[0]<relation.arg1List[0]):
			print "Case 3"
		else:
		 	print "Case 4"
		complete=completeChunk(relation.arg2List,wordList)
		print complete
		if(not complete[1]):
			print_span(relation.arg2List,wordList)
			print_span(sentenceList[wordList[relation.arg2List[0]].sentenceNum].wordNumList,wordList)

