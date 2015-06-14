#!/bin/bash
for i in `seq 1 20`;
do
	echo $i
	time python  identify_connectives.py > o1
done 
