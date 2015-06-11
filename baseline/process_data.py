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
#from identify_connectives import *
from annotated_data import *



#def processRawFile(data,connList,connSplitList,extraDelimiters):
#	extraDelimiters.append(fullStop)
#	discourseUnits=getDiscourseUnit(data,extraDelimiters)
#	spans=findAllOccurences(extraDelimiters,data)
#	spans.insert(0,0)
#	spans.append(len(data))
#	num=0
#	discourseFileInst=discourseFile()
#	for unit in discourseUnits :
#		unit=discourseUnit(unit,spans[num],[num+1])
#		discourseFileInst.addUnit(unit)
#		num+=1
#	return discourseFileInst


if len(sys.argv)<2:
	print "Please give folder location"
	exit()
dataLocation=sys.argv[1]
rawFileList=folderWalk(dataLocation+"/raw")
annFileList=folderWalk(dataLocation+"/ann")
connList=loadConnList("connectives/compConnectiveList.list")
connSplitList=loadConnList("connectives/splitConnectiveList.list",True)
discourseFileCollection=[]
fileNum=0
for rawFile in rawFileList:
	fd=codecs.open(rawFile,"r",encoding="utf-8")
#	discourseFileInst=processRawFile(fd.read(),connList,connSplitList,[])
	(sentenceList,globalWordList)=extractSSFannotations(rawFile)
	if(sentenceList==None or globalWordList==None):
		print "Continuing"
		continue
	discourseFileInst=discourseFile(sentenceList,globalWordList,fd.read())
	discourseFileInst.addDiscourseRelationInfo(extractRelation(rawFile))
	discourseFileCollection.append(discourseFileInst)
#	identifyConnectives(discourseFileInst,connList,connSplitList)
	fd.close()
	fileNum+=1
	print "*"*90,fileNum,"files done"

exportModel("processedData/annotatedData",discourseFileCollection)
print "processed %d files correctly"%(fileNum)
