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
	def __init__(self,word_dictionary,tag_path,chunk_path):
		self.wordDictionary=word_dictionary
		self.tagSet=loadSet(tag_path)
		self.chunkSet=loadSet(tag_path)
		self.featureVector=[]
		self.classLabel=None
	def loadSet(self,filePath):
		Set=[]
		fileFD=codecs.open(filePath,"r",encoding="utf-8")
		for line in fileFD.readline():
			Set.append(line)
		return Set
	def tagFeature(self,tagList):
		feature=[]
		for tag in self.tagSet:
			if(tag in tagList):
				feature.append(1)
			else:
				feature.append(0)
		self.featureVector.extend(feature)
		return feature
	def chunkFeature(self,chunkList):
		feature=[]
		for tag in self.tagSet:
			if(tag in tagList):
				feature.append(1)
			else:
				feature.append(0)
	def markList()
		

