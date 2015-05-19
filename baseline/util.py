#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import re

def folderWalk(folderPath):
	import os
	fileList = []
	for dirPath , dirNames , fileNames in os.walk(folderPath) :
		for fileName in fileNames :
			fileList.append(os.path.join(dirPath , fileName))
	return fileList
def findAllOccurences(delimList,inputString):
	searchKey=""
	for delim in delimList:
		searchKey+="|"
		searchKey+=delim
	searchKey=searchKey[1:]
#	print searchKey
	return [m.start() for m in re.finditer(searchKey, inputString)]
def getDiscourseUnit(text,delimList):
	delimString=""
	for i in delimList:
		delimString+=i+" | "
	delimString=delimString[:len(delimString)-3]
	return re.split(delimString,text)
def loadConnList(fileName,split=False):
	fd=open(fileName,"r")
	connList=[]
	for conn in fd.readlines():
		conn=conn[:-1]
		if split:
			connList.append(tuple(conn.split("..")))
		else:
			connList.append(conn)
	return connList
