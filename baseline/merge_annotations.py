#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
from util import *
from letter import *


def mappingBetweenFiles(wordList,rawData):
	rawToWord={}
	wordToRaw={}
	rawData=addSpaces(rawData)
			
	startDoc=getStartPos(rawData,wordList)
	rawData=rawData[startDoc:]
	rawData=rawData.split()
	rawPos=0
	wordPos=0
	while(1):
		if(rawPos>=len(rawData) or wordPos>=len(wordList)):
			break
#		print "comparing",rawData[rawPos],wordList[wordPos].word
#		print "comparing",repr(rawData[rawPos]),repr(wordList[wordPos].word)
		if(rawData[rawPos]=="NULL"):
			rawToWord[rawPos]=(wordPos,)
			rawPos+=1
			continue
		if(rawData[rawPos]==wordList[wordPos].word):
#			print "word matched perfectly",rawData[rawPos],wordList[wordPos].word
			rawToWord[rawPos]=(wordPos,)
			wordToRaw[wordPos]=(rawPos,)
			wordPos+=1
		else:
			if(wordPos+1  < len(wordList)  and  wordList[wordPos].word+wordList[wordPos+1].word==rawData[rawPos] ):
#				print "word 1 matched perfectly",rawData[rawPos],wordList[wordPos].word+wordList[wordPos+1].word
				rawToWord[rawPos]=(wordPos,wordPos+1)
				wordToRaw[wordPos]=(rawPos,)
				wordToRaw[wordPos+1]=(rawPos,)
				wordPos+=2
			elif(not isNum(rawData[rawPos]) and wordPos+1  < len(wordList)  and  wordList[wordPos].word[:len(wordList[wordPos].word)-1]+wordList[wordPos+1].word[:len(wordList[wordPos+1].word)-1]==rawData[rawPos] ):
#				print "word 2 matched perfectly",rawData[rawPos],wordList[wordPos].word[:len(wordList[wordPos].word)-1]+wordList[wordPos+1].word[:len(wordList[wordPos+1].word)-1]
#				print wordList[wordPos].word
#				print wordList[wordPos+1].word
				rawToWord[rawPos]=(wordPos,wordPos+1)
				wordToRaw[wordPos]=(rawPos,)
				wordToRaw[wordPos+1]=(rawPos,)
				wordPos+=2
			elif( wordPos+2 < len(wordList ) and (wordList[wordPos].word+wordList[wordPos+2].word==rawData[rawPos] or wordList[wordPos].word+u'\u093e'+wordList[wordPos+2].word==rawData[rawPos])):
#				print "word 3 matched perfectly",rawData[rawPos],wordList[wordPos].word+wordList[wordPos+2].word, "extra",wordList[wordPos+1].word
				rawToWord[rawPos]=(wordPos,wordPos+1,wordPos+2)
				wordToRaw[wordPos]=(rawPos,)
				wordToRaw[wordPos+1]=(rawPos,)
				wordToRaw[wordPos+2]=(rawPos,)
				wordPos+=3
			elif (rawPos+2 < len(rawData) and rawData[rawPos]+rawData[rawPos+1]+rawData[rawPos+2]==wordList[wordPos].word):
#				print "word 4 matched perfectly"
				rawToWord[rawPos]=(wordPos,)
				rawToWord[rawPos+1]=(wordPos,)
				rawToWord[rawPos+2]=(wordPos,)
				wordToRaw[wordPos]=(rawPos,rawPos+1,rawPos+2)
				rawPos+=2
				wordPos+=1
			elif(rawPos +4 < len(rawData) and rawData[rawPos]+rawData[rawPos+2]+rawData[rawPos+4]==wordList[wordPos].word):
#				print "word 5 matched perfectly"
				rawToWord[rawPos]=(wordPos,)
				rawToWord[rawPos+1]=(wordPos,)
				rawToWord[rawPos+2]=(wordPos,)
				rawToWord[rawPos+3]=(wordPos,)
				rawToWord[rawPos+4]=(wordPos,)
				wordToRaw[wordPos]=(rawPos,rawPos+1,rawPos+2,rawPos+3,rawPos+4)
				rawPos+=4
				wordPos+=1
			elif(rawPos+1< len(rawData) and rawData[rawPos]+rawData[rawPos+1]==wordList[wordPos].word):
#				print "word 6 matched perfectly"
				rawToWord[rawPos]=(wordPos,)
				rawToWord[rawPos+1]=(wordPos,)
				wordToRaw[wordPos]=(rawPos,rawPos+1)
				rawPos+=1
				wordPos+=1
			elif(rawData[rawPos].replace(u'\u0902',u'\u0901')==wordList[wordPos].word or rawData[rawPos].replace(u'\u0901',u'\u0902')==wordList[wordPos].word):
#				print "word 7 matched perfectly",rawData[rawPos],wordList[wordPos].word
				rawToWord[rawPos]=(wordPos,)
				wordToRaw[wordPos]=(rawPos,)
				wordPos+=1
			elif(rawPos +2 < len(rawData) and rawData[rawPos+2]==wordList[wordPos+1].word):
#				print "ahem ahem"
				rawToWord[rawPos]=(wordPos,)
				rawToWord[rawPos+1]=(wordPos,)
				wordToRaw[wordPos]=(rawPos,rawPos+1)
				rawPos+=1
				wordPos+=1
			elif(wordPos +1 < len(wordList) and rawPos+1 < len(rawData) and wordList[wordPos+1].word==rawData[rawPos+1]):
#				print "-"*30,"SKIPPED 1",rawData[rawPos],wordList[wordPos].word
				rawToWord[rawPos]=(wordPos,)
				wordToRaw[wordPos]=(rawPos,)
				wordPos+=1
			elif(wordPos+2 < len(wordList) and rawPos+1< len(rawData) and rawData[rawPos+1]==wordList[wordPos+1].word+wordList[wordPos+2].word):
#				print "-"*30,"SKIPPED 2",rawData[rawPos],wordList[wordPos].word
				rawToWord[rawPos]=(wordPos,)
				wordToRaw[wordPos]=(rawPos,)
				rawToWord[rawPos+1]=(wordPos+1,wordPos+2)
				wordToRaw[wordPos+1]=(rawPos+1,)
				wordToRaw[wordPos+2]=(rawPos+1,)
				wordPos+=3
				rawPos+=1

			elif(wordPos+2 < len(wordList) and rawPos + 2< len(rawData) and rawData[rawPos+2]==wordList[wordPos+2].word):
#				print "-"*30,"SKIPPED 3"
				rawToWord[rawPos]=(wordPos,)
				wordToRaw[wordPos]=(rawPos,)
				wordPos+=1
				rawPos+=1
				rawToWord[rawPos]=(wordPos,)
				wordToRaw[wordPos]=(rawPos,)
				wordPos+=1
			elif(wordPos +2 < len(wordList) and rawPos+1 < len(rawData) and wordList[wordPos+2].word==rawData[rawPos+1]):
#				print "-"*30,"SKIPPED 4",rawData[rawPos],wordList[wordPos].word
				rawToWord[rawPos]=(wordPos,wordPos+1)
				wordToRaw[wordPos]=(rawPos,)
				wordToRaw[wordPos+1]=(rawPos,)
				wordPos+=2
			elif (wordPos+2 < len(wordList) and rawData[rawPos]==wordList[wordPos+2].word):
#				print "-"*30,"SKIPPED 5"
				rawToWord[rawPos-1]=list(rawToWord[rawPos-1])
				rawToWord[rawPos-1].append(wordPos)
				rawToWord[rawPos-1].append(wordPos+1)
				rawToWord[rawPos-1]=tuple(rawToWord[rawPos-1])
				wordToRaw[wordPos]=(rawPos-1,)
				wordToRaw[wordPos+1]=(rawPos-1,)
				rawToWord[rawPos]=(wordPos+2,)
				wordPos+=3
			elif(rawPos+2 < len(rawData) and isNum(rawData[rawPos]) and isNum(rawData[rawPos+2]) and rawData[rawPos+1]=="," and (rawData[rawPos]+","+rawData[rawPos+2]==wordList[wordPos] or convertNum(rawData[rawPos])+"," +convertNum(rawData[rawPos+2]) == wordList[wordPos].word)):
#				print "number detected"
				rawToWord[rawPos]=(wordPos,)
				rawToWord[rawPos+1]=(wordPos,)
				rawToWord[rawPos+2]=(wordPos,)
				wordToRaw[wordPos]=(rawPos,rawPos+1,rawPos+2)
				rawPos+=2
				wordPos+=1
			elif(rawPos+4 < len(rawData) and isNum(rawData[rawPos]) and isNum(rawData[rawPos+2]) and isNum(rawData[rawPos+4]) and rawData[rawPos+1]=="," and rawData[rawPos+3]=="," and ( convertNum(rawData[rawPos])+","+convertNum(rawData[rawPos+2]) +","+ convertNum(rawData[rawPos+4]) == wordList[wordPos].word or rawData[rawPos]+","+rawData[rawPos+2]+","+rawData[rawPos+4]==wordList[wordPos].word)):
#				print "large number detected"
				rawToWord[rawPos]=(wordPos,)
				rawToWord[rawPos+1]=(wordPos,)
				rawToWord[rawPos+2]=(wordPos,)
				rawToWord[rawPos+3]=(wordPos,)
				rawToWord[rawPos+4]=(wordPos,)
				wordToRaw[wordPos]=(rawPos,rawPos+1,rawPos+2,rawPos+3,rawPos+4)
				rawPos+=4
			else:
				print "ISSUES"
				print rawData[rawPos]==wordList[wordPos].word+wordList[wordPos].word
				edit=editDistance(rawData[rawPos],wordList[wordPos].word)
				if(edit <= 2 ) :
					print "will be solved"
				print edit
				loop=0
				while(rawPos < len(rawData) and wordPos < len(wordList)  and loop < 3):
					print rawData[rawPos],wordList[wordPos].word
					rawPos+=1
					wordPos+=1
					loop+=1
#				print rawData[rawPos+2],wordList[wordPos+2].word
				return (rawToWord,wordToRaw)
#		print rawPos
		rawPos+=1
#	print "stats %d %d"%(rawPos,wordPos)
	return (rawToWord,wordToRaw)

#	def addUnit(self,discourseUnit):
#		self.discourseUnitList.append(discourseUnit)
#	def addDiscourseRelationList(self,discourseRelationList):
#		self.discourseRelationList=discourseRelationList
#	def addSSFData(self,ssf):
#		self.SSFData=ssf
def getStartPos(rawData,wordList):
	startString=wordList[0].word
	for i in range(1,5):
		startString=startString+" "+wordList[i].word
#	print startString
	startDoc=rawData.find(startString)
#	print startDoc
	if(startDoc==-1):	
#		print "here here 1",wordList[0].word+" "+wordList[1].word+" "+wordList[2].word+" "+wordList[3].word
#		print startDoc
		startDoc=rawData.find(wordList[0].word+" "+wordList[1].word+" "+wordList[2].word+" "+wordList[3].word)
	if(startDoc==-1):
		startDoc=rawData.find(wordList[0].word+" "+wordList[1].word)
#		print "here here 2",wordList[0].word+" "+wordList[1].word
#		print startDoc
	if(startDoc==-1):
#		print "here here 3"
		startDoc=rawData.find(wordList[1].word+" "+wordList[2].word)
		startDoc-=2
		while(rawData[startDoc]!=' '):
			startDoc-=1
#		print startDoc
	if(startDoc<0):
#		print "here here 4"
		startDoc=rawData.find(wordList[2].word+" "+wordList[3].word)
		startDoc-=2
		while(rawData[startDoc]!=' '):
			startDoc-=1
		startDoc-=1
		while(rawData[startDoc]!=' '):
			startDoc-=1
#		print startDoc
	if(startDoc<0):
#		print "here here 5"
		startDoc=rawData.find(wordList[0].word+wordList[1].word+wordList[2].word)
#		print startDoc
#	print "getting startDoc ",startDoc
	return startDoc

def getSpanFromAnn(spans,rawData,wordList,annToWord,wordToAnn):
	
	startDoc=getStartPos(rawData,wordList)
	spans=re.split(';',spans)
	returnSpan=[]
	for span in spans:
		posList=[]
		span=re.split("\.\.",span)
#		print startDoc
#		print rawData[int(span[0]):int(span[1])]
		dataBefore=rawData[startDoc:int(span[0])-1]
		dataAfter=rawData[startDoc:int(span[1])]
		dataBefore=addSpaces(dataBefore).split()
		dataAfter=addSpaces(dataAfter).split()
#		print len(dataBefore),
#		print len(dataAfter),
#		print wordToAnn[len(dataBefore)],
#		print wordToAnn[len(dataAfter)-1]
		for wordNum in range(len(dataBefore),len(dataAfter)):
			wordNumTuple=wordToAnn[wordNum]
			for word in wordNumTuple:
				posList.append(word)
				print wordList[word].word,
		prev=-1
		trimmedPosList=[]
		for pos in posList: 
		 	if(pos!=prev):
				trimmedPosList.append(pos)
			prev=pos
		returnSpan.append(posList)
		print "\n"
	return returnSpan
def editDistance(word1 , word2):

	len_1=len(word1)
	len_2=len(word2)
	x =[[0]*(len_2+1) for _ in range(len_1+1)]#the matrix whose last element ->edit distance
	for i in range(0,len_1+1): #initialization of base case values
		x[i][0]=i
	for j in range(0,len_2+1):
		x[0][j]=j
	for i in range (1,len_1+1):
		for j in range(1,len_2+1):
			if word1[i-1]==word2[j-1]:
				x[i][j] = x[i-1][j-1] 
			else :
				x[i][j]= min(x[i][j-1],x[i-1][j],x[i-1][j-1])+1
	return x[i][j]
def addSpaces(rawData):
	rawData=rawData.replace(fullStop," "+fullStop+" ")
	rawData=rawData.replace("," ," , ")
	rawData=rawData.replace("-" ," - ")
	rawData=rawData.replace("("," ( ")
	rawData=rawData.replace(")"," ) ")
	rawData=rawData.replace("?"," ? ")
	rawData=rawData.replace("'"," ' ")
	rawData=rawData.replace(".",". ")
	return rawData
def convertNum(num):
	returnNum=""
	for letter in num:
		returnNum+=numMap[letter.encode("utf-8")]
	return returnNum
def isNum(word):
	word=word.replace(".","")
	word=word.replace(",","")
#	print word
	num=True
	for letter in word:
		if(letter not in hindiNum):
			num=False
	if(num):
		return True
	num=True
	for letter in word:
		if(letter not in engNum):
			num=False
	return num

