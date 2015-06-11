#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
import codecs
sys.setdefaultencoding("utf-8")

import re
import ssf
from util import *
from bs4 import BeautifulSoup


class Sentence():
	def __init__(self):
#		print "-"*30,"adding sentence"
		self.chunkList=[]
		self.wordNumList=[]
		return
	def addChunk(self,chunk):
#		print "-"*30,"adding chunk"
		self.chunkList.append(chunk)
	def addWord(self,word):
#		print "-"*30,"adding word to sentence"
		self.wordNumList.append(word)

class Chunk():
	def __init__(self,tag,features_string,sentenceNum):
#		print "-"*30,"new chunk with tag - %s and f = %s"%(tag,features_string)
		self.chunkTag=tag
		self.featureSet=FeatureSet(features_string)
		self.wordNumList=[]
		self.sentenceNum=sentenceNum
	def addWord(self,word):
#		print "-"*30,"adding word to chunk"
		self.wordNumList.append(word)
class Word():
	def __init__(self,word,tag,features_string,sentenceNum,chunkNum):
#		print "-"*30,"new word- %s with tag - %s and f = %s"%(word,tag,features_string)
		self.wordTag=tag;
		self.word=word.decode("utf-8")
		self.featureSet=FeatureSet(features_string)
		self.sentenceNum=sentenceNum
		self.chunkNum=chunkNum
		self.sense=None
		self.conn=False
		self.splitConn=False
		self.arg1=False
		self.arg2=False
		self.relationNum=None
class FeatureSet():
	def __init__(self,featureString):
		self.featureDict={}
		self.processFeatureString(featureString)
	def processFeatureString(self,featureString):
		featureSet=re.split(' ',featureString)
		featureSet=featureSet[1:]
		for feature in featureSet:
#			print feature
			feature=re.split('=',feature)
			key=feature[0]
			value=re.split('\"',feature[1])[1]
#			print key,"=",value
			self.featureDict[key]=value

def extractSSFannotations(filePath):
	filePath=filePath.replace("/raw/","/ssf/")
	if not fileExists(filePath) :
		print "No file found"
		return (None,None)
	fileFD=codecs.open(filePath,"r",encoding="utf-8")
	data=fileFD.read()
	fileFD.close()
	beautData = BeautifulSoup(data)
	sentenceList=beautData.find_all('sentence')
	sentenceInstList=[]
	globalWordList=[]
	sentenceNum=0
	wordNum=0
	for sentence in sentenceList:
		sentenceInst=Sentence()
		content=sentence.renderContents()
		lines=re.split("\n",content)
		chunkInst=None
		wordInst=None
		chunkNum=-1
		skip=False
		for line in lines:
			columns=line.split("\t")
#			print line,"--",len(columns)
			if(len(columns)<2): #useless line
				continue
			if(columns[1]=="(("): # new chunk
#				if("NULL" in columns[2]):
#					skip=True
#					continue
				chunkNum+=1
				chunkInst=Chunk(columns[2],columns[3],sentenceNum)
			elif(columns[1]=="))"):
				
			  	if(len(chunkInst.wordNumList)!=0):
					sentenceInst.addChunk(chunkInst)
				else:
					chunkNum-=1
			else:
			  	if(columns[1]=="NULL"):
					continue
				wordInst=Word(columns[1],columns[2],columns[3],sentenceNum,chunkNum)
				chunkInst.addWord(wordNum)
				wordNum+=1
				sentenceInst.addWord(wordNum)
				globalWordList.append(wordInst)
#		print "final stats",len(SSFSentenceInst.wordList),len(SSFSentenceInst.chunkList)
		sentenceInstList.append(sentenceInst)
		sentenceNum+=1
	return (sentenceInstList,globalWordList)
