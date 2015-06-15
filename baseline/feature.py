#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
import numpy
reload(sys)
sys.setdefaultencoding("utf-8")
from util import *
from letter import *


class Feature():
	def __init__(self,word_dictionary_path,tag_path,chunk_path,discourse_file,global_word_list,sentence_list,conn=None):
		self.discourseFile=discourse_file
		self.wordDictionary=self.loadSet(word_dictionary_path,["First","Last"])
		self.tagSet=self.loadSet(tag_path,["First","Last"])
		self.chunkSet=self.loadSet(chunk_path,["First","Last"])
		self.featureVector=[]
		self.classLabel=None
		self.globalWordList=global_word_list
		self.sentenceList=sentence_list
		if(conn!=None):
			self.connective=""
			for i in conn:
				self.connective=self.connective+" "+self.globalWordList[i].word
			self.connective=self.connective[1:]
			self.conn=conn
		print len(self.tagSet)
		print len(self.chunkSet)
	def loadSet(self,filePath,extra=[]):
		Set=[]
		fileFD=codecs.open(filePath,"r",encoding="utf-8")
		for line in fileFD.readlines():
			line=line.split()
			for word in line:
				Set.append(word)
		Set.extend(extra)
		return Set
	def wordFeature(self,wordList):
		print "wordfeature"
		words=[]
		for word in wordList:
			word=self.globalWordList[word].word
			words.append(word)
		feature=self.markItemsinList(words,self.wordDictionary)
		print feature
		return feature
	def wordNeighbor(self,wordList,offSet):
		print "wordNeighbor"
		words=[]
		if(offSet<0):
			if(wordList[0]+offSet<0):
				words.append("First")
			else:
				words.append(self.globalWordList[wordList[0]+offSet].word)
		else:
			if(wordList[-1]+offSet>=len(self.globalWordList)):
				words.append("Last")
			else:
			 	words.append(self.globalWordList[wordList[-1]+offSet].word)
		feature=self.markItemsinList(words,self.wordDictionary)
		print feature
		return feature
	def tagFeature(self,wordList):
		print "tagfeature"
		tagList=[]
		for word in wordList:
			word=self.globalWordList[word]
			print word.wordTag,
			tagList.append(word.wordTag)
		print ""
		feature=self.markItemsinList(tagList,self.tagSet)
		print feature
		return feature
	def tagNeighbor(self,wordList,offSet):
		print "tagNeighbor"
		tagList=[]
		if(offSet<0):
			if(wordList[0]+offSet<0):
				tagList.append("First")
			else:
				tagList.append(self.globalWordList[wordList[0]+offSet].word)
		else:
			if(wordList[-1]+offSet>=len(self.globalWordList)):
				tagList.append("Last")
			else:
			 	tagList.append(self.globalWordList[wordList[-1]+offSet].word)
		feature=self.markItemsinList(tagList,self.tagSet)
		print feature
		return feature
	def chunkFeature(self,wordList):
		print "chunkfeature"
		chunkList=[]
		for word in wordList:
			word=self.globalWordList[word]
			print self.getChunkInfo(word,0).chunkTag,
			chunkList.append(self.getChunkInfo(word,0).chunkTag)
		print ""
		feature=self.markItemsinList(chunkList,self.chunkSet)
		print feature
	def chunkNeighbor(self,wordList,offSet):
		print "chunkNeighbor",offSet
		chunkList=[]
		if(offSet<0):
			try:
				chunkList.append(self.getChunkInfo(self.globalWordList[wordList[0]],offSet).chunkTag)
			except AttributeError:
				chunkList.append("First")
		else:
			try:
				chunkList.append(self.getChunkInfo(self.globalWordList[wordList[-1]],offSet).chunkTag)
			except AttributeError:
				chunkList.append("Last")
		print chunkList
		feature=self.markItemsinList(chunkList,self.chunkSet)
	def markItemsinList(self,List,Set):
		feature=[]
		for item in Set:
			if(item in List):
				feature.append(1)
			else:
				feature.append(0)
		self.featureVector.extend(feature)
		return feature
	def getChunkInfo(self,word,offSet):
		sentence=self.sentenceList[word.sentenceNum]
		if(word.chunkNum+offSet>=0 and word.chunkNum+offSet<len(sentence.chunkList)):
			chunk=sentence.chunkList[word.chunkNum+offSet]
		else:
			chunk=None
		return chunk
	def aurFeature(self,conn):
		if(self.globalWordList[conn[0]].word != u'\u0914\u0930'):
			self.featureVector.append(0)
			return [0]
		chunkNum=0
                before=False
                after=False
                middle=False
		sentence=self.discourseFile.sentenceList[self.globalWordList[conn[0]].sentenceNum]
                for chunk in sentence.chunkList:
                        if(chunk.chunkTag[:2]=="VG"):
                                if(middle==False):
                                        before=True
                                else:
                                        after=True
                        for word in chunk.wordNumList:
                                if(self.discourseFile.globalWordList[word].word==u'\u0914\u0930'):
                                        middle=True
                        chunkNum+=1
		if(before and after):
			self.featureVector.append(1)
			return [1]
		self.featureVector.append(0)
		return [0]

	def setClassLabel(self,label):
		self.classLabel=label

def convertDataSet(featureCollection):
	data=[]
	labels=[]
	for feature in featureCollection:
		data.append(numpy.array(feature.featureVector))
		labels.append(feature.classLabel)
	labels=numpy.array(labels)
	data=numpy.array(data)
	return data,labels
