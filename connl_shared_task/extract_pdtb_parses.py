#!/usr/bin
import json
from pprint import pprint


class pdtb_sentences():
	def __init__(self,sentence):
		self.parse_tree=sentence["parsetree"]
		self.dependencies=sentence["dependencies"]
		self.words=[]
		for word in sentence["words"]:
			self.words.append((word[0],word[1]))


def print_keys(dic):
	keys=[]
	for key,value in dic.iteritems():
		keys.append(key)
		print key
	return keys

def parse_sentences_dict(sentence_collection):
	parsed_sentences=[]
	for i in sentence_collection:
		parsed_sentences.append(pdtb_sentences(i))
	return parsed_sentences
def print_parsed_sentences(parsed_sentences):
	sentence_num=0
	for i in parsed_sentences:
		print "-"*30,"Sentence number %d"%(sentence_num),"-"*30 
		print i.parse_tree
		print "\tSentence dependencies"
		print i.dependencies
		print "\tSentence Words"
		for word in  i.words:
			print "\t\t",word[0],word[1]
		sentence_num+=1


#taking input file name	
file_name=raw_input("Enter json file\n")
#reading input file and converting json to python dictionary
file_input=open(file_name,"r")
json_data=file_input.read()
data=json.loads(json_data)

#parsing sentence information
sentence_collection=data["wsj_1000"]["sentences"]

parsed_sentences=parse_sentences_dict(sentence_collection)

print_parsed_sentences(parsed_sentences)
#pprint(data)
