#!/usr/bin
import json
from pprint import pprint

class Span():
	def __init__(self,Span):
		try:
			self.CharacterSpanList=Span.get("CharacterSpanList")
			self.RawText=Span.get("RawText")
			self.TokenList=Span.get("TokenList")
		except:
			print Span

class Relation():
	def __init__(self,RelationInfo,JsonFile,RawDataLocation):
		self.DocID=RelationInfo["DocID"]
		FileInput=open(RawDataLocation+"/"+self.DocID,"r")
		self.RawData=FileInput.read()
		FileInput.close()
		self.ID=RelationInfo["ID"]
		self.Sense=RelationInfo["Sense"]
		self.Connective_type=RelationInfo["Type"]
		self.Argument1=Span(RelationInfo["Arg1"])
		self.Argument2=Span(RelationInfo["Arg2"])
		self.Connective=Span(RelationInfo["Connective"])
	def PrintInfo(self,FileOut):
		FileOut.write(str(self.DocID)+"\n")
		FileOut.write(str(' '.join(self.Sense))+"\n")
		FileOut.write(str(self.Connective_type)+"\n")
		self.PrintSpan(self.Argument1,FileOut)
		self.PrintSpan(self.Argument2,FileOut)
		self.PrintSpan(self.Connective,FileOut)
	def PrintSpan(self,span,FileOut):
		FileOut.write(span.RawText+"\n")
		

def  extractDiscourseInfo(FilePath,RawDataLocation):
	file_input=open(FilePath,"r")
	data=[]
	for line in file_input.readlines():
		data.append(Relation(json.loads(line),FilePath,RawDataLocation))
	print len(data)
	return data
def Print(data,FilePath):
	FileOut=open(FilePath,"w")
	FileOut.write("Format\nDocId\nSense\nArgument1\nArgument2\nConnective\n-----------------------------------------------------\n")
	for Sentence in data:
		Sentence.PrintInfo(FileOut)
	FileOut.close()
