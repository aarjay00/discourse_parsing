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

class relation():
	def __init__(self,RelationInfo):
		self.DocID=RelationInfo["DocID"]
		self.ID=RelationInfo["ID"]
		self.Sense=RelationInfo["Sense"]
		self.Connective_type=RelationInfo["Type"]
		self.Argument1=Span(RelationInfo["Arg1"])
		self.Argument2=Span(RelationInfo["Arg2"])
		self.Connective=Span(RelationInfo["Connective"])



file_name=raw_input("Enter pdtb data file\n")
file_input=open(file_name,"r")
data=[]
for line in file_input.readlines():
	data.append(relation(json.loads(line)))
print len(data)
