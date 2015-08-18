fd=open("o2","r")
dic={}
dic1={}
for i in fd.readlines():
	i=i.split("-"*30)[1]
	i=i.split()
	if(i[1]=="Yes"):
		if i[0] in dic:
			dic[i[0]]+=1
		else:
			dic[i[0]]=1
	elif(i[1]=="No"):
		if i[0] in dic1:
			dic1[i[0]]+=1
		else:
			dic1[i[0]]=1
	else:
		print "hmm"

keys=dic.keys()
keys.extend(dic1.keys())


keys=set(keys)

for key in keys:
	if(key not in dic):
		dic[key]=0
	if(key not in dic1):
		dic1[key]=0
	print key,dic[key],dic1[key],dic[key]*1.0/(dic[key]+dic1[key])
