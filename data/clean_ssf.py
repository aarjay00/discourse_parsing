#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup
import ssf

def folderWalk(folderPath):
	import os
	fileList = []
	for dirPath , dirNames , fileNames in os.walk(folderPath) :
		for fileName in fileNames :
			fileList.append(os.path.join(dirPath , fileName))
	return fileList

files=folderWalk("./ssf")
for f in files:
	print "processing",f
	fd=open(f,"r")
	data=fd.read()
	fd.close()
	data = BeautifulSoup(data)
	formattedData=data.find_all('sentence')
	fd=open(f,"w")
	for sentence in formattedData:
		fd.write(str(sentence)+"\n")
	fd.close()
	node=ssf.node()
	node.read_ssf_from_file("./sample.ssf")
