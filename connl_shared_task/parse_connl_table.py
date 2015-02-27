#!/usr/bin

file_name=raw_input("Enter connl table input\n")
file_input=open(file_name,"r")
for i in file_input.readlines():
	i=i.replace('_','').split()
	print i
