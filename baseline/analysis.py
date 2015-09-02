
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
import operator

from util import *
from extract_relations import *
from ssf_api import *
from letter import *
from merge_annotations import *
from annotated_data import *
from feature import *



def genAttrMaps(attrList,errorList):
	attrMapList=[]
	for attrName in attrList:
		attrMap={}
		for error in errorList:
			if(getattr(error,attrName) in attrMap):
				attrMap[getattr(error,attrName)].append(error)
			else:
				attrMap[getattr(error,attrName)]=[error]
		attrMapList.append((attrName,attrMap))
	return attrMapList
def printAttrMaps(attrMapList,folderName):
	createDirectory("analysis/"+folderName+"/")
	for attrName,attrMap in attrMapList:
		FD=codecs.open("analysis/"+folderName+"/"+attrName,"w")
		sortedList=sorted(attrMap.items(), key=operator.itemgetter(1))
		sortedList.sort(lambda x,y : -1*cmp(len(x[1]),len(y[1])))
		for item in sortedList:
#			print item
			FD.write("-"*100 + "\n")
			FD.write(str(item[0])+" Frequency: " +str(len(item[1])) +"\n")
			for i in item[1]:
				FD.write("------\n")
				i.printFeatureDesc(FD)
		FD.close()

def basicAnalysis(errorList,analysisFolderName):
	attrList=errorList[0].attrList
	attrMapList=genAttrMaps(attrList,errorList)
	printAttrMaps(attrMapList,analysisFolderName)
