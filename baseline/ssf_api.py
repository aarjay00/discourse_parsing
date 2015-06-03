#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import re
import ssf
from util import *
from bs4 import BeautifulSoup

class SSFSentence():
	def __init__(self):
#		print "-"*30,"adding sentence"
		self.chunkList=[]
		self.wordList=[]
		return
	def addChunk(self,chunk):
#		print "-"*30,"adding chunk"
		self.chunkList.append(chunk)
	def addWord(self,word):
#		print "-"*30,"adding word to sentence"
		self.wordList.append(word)

class Chunk():
	def __init__(self,tag,features_string):
#		print "-"*30,"new chunk with tag - %s and f = %s"%(tag,features_string)
		self.chunkTag=tag
		self.featureSet=FeatureSet(features_string)
		self.wordList=[]
	def addWord(self,word):
#		print "-"*30,"adding word to chunk"
		self.wordList.append(word)
class Word():
	def __init__(self,word,tag,features_string):
#		print "-"*30,"new word- %s with tag - %s and f = %s"%(word,tag,features_string)
		self.wordTag=tag;
		self.word=word
		self.featureSet=FeatureSet(features_string)
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
		return None
	fileFD=open(filePath,"r")
	data=fileFD.read()
	fileFD.close()
	beautData = BeautifulSoup(data)
	sentenceList=beautData.find_all('sentence')
	SSFSentenceInstList=[]
	for sentence in sentenceList:
		SSFSentenceInst=SSFSentence()
		content=sentence.renderContents()
		lines=re.split("\n",content)
		chunkInst=None
		wordInst=None
		for line in lines:
			columns=line.split("\t")
#			print line,"--",len(columns)
			if(len(columns)<2): #useless line
				continue
			if(columns[1]=="(("): # new chunk
				chunkInst=Chunk(columns[2],columns[3])
			elif(columns[1]=="))"):
				SSFSentenceInst.addChunk(chunkInst)
			else:
				wordInst=Word(columns[1],columns[2],columns[3])
				chunkInst.addWord(wordInst)
				SSFSentenceInst.addWord(wordInst)
#		print "final stats",len(SSFSentenceInst.wordList),len(SSFSentenceInst.chunkList)
		SSFSentenceInstList.append(SSFSentenceInst)
	return SSFSentenceInstList
