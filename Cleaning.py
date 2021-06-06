import pandas as pd
import numpy as np
import os
import shutil



removeTweetifwordContain=["happybirthday","hashtag","hastag","today","𝐭𝐨𝐝𝐚𝐲","gud morning","good morning","hash tag"," vs ","Retweet","#twitterindia","news","I ",
						  "republic","26","jan","𝐉𝐚𝐧","march","𝐓𝐨𝐩","March",
						  "ਅੱਜ","ਬੇਨਤੀ","ਮਿਤੀ","ਹੈਸਟੇਗ","जयभीम","दिन","ਪਰੇਂਡ","गणतंत्र","सक्रिय साथियों"]


def cleanText(text):
	tlower=text.lower()
	if len(tlower)<5 or tlower[0]=="@":
		return ""
	for word in removeTweetifwordContain:
		if word in tlower:
			return ""
	if text[:2]=="\\n":
		text=text[2:]
	text = text.replace("\\n ","\\n").replace(" \\n","\\n").replace("\\n\\n", "\\n").replace("&amp;","&")
	for i in range(500):
		text=text.replace("\\n"+str(i)+"\\n","\\n")
	def removeExtra(text,index=-1,sep=" "):
		textlist=text.split(sep)
		#while len(textlist)>0 and (len(textlist[index])==0 or textlist[index][0]=="@" or textlist[index][0]=="#" or textlist[index][:2]=="\\n"  or textlist[index][0].isdigit()):
		while len(textlist)>0 and (len(textlist[index])==0 or textlist[index][0]=="@"  or textlist[index][:2]=="\\n"  or textlist[index][0].isdigit()):
			if index==-1:
				textlist=textlist[:-1]
			else:
				textlist=textlist[index+1:]
		return sep.join(textlist)
	text=removeExtra(text,0,"\\n")
	text=removeExtra(text,-1,"\\n")
	text=removeExtra(text,0)
	text=removeExtra(text)
	text=text.split("https")[0]
	return text


def getCleanedTextForFile(file,sep="&^$",tweets="Tweet.txt",cleanedData="Out.csv"):
	with open(file) as f:
		data=np.array([d.split(sep) for d in  f.readlines()])
	data=data[:,:2]
	data=list(filter(lambda x:len(x[1])>5,map(lambda x:(x[0],cleanText(x[1])),data)))
	with open(tweets,"a") as f:
		f.writelines(list(set([d[1]+"\n" for d in data])))
	data=[sep.join(d)+"\n" for d in data]
	with open(cleanedData,"a") as f:
		f.writelines(data)

def ProcessAllFiles(datapath,cleantweets="Tweet.txt",cleanedData="Out.csv",requireWord=None):
	with open(cleantweets,"w") as f:
		pass
	with open(cleanedData,"w") as f:
		pass
	allfiles=[datapath+f for f in os.listdir(datapath)]
	for file in allfiles:
		getCleanedTextForFile(file,tweets=cleantweets,cleanedData=cleanedData)
	with open(cleantweets, "r") as f:
		data = f.readlines()
	if requireWord:
		data=[d for d in data if requireWord in d]
	with open(cleantweets, "w") as f:
		f.writelines(list(set(data)))
	with open(cleanedData, "r") as f:
		data = f.readlines()
	if requireWord:
		data=[d for d in data if requireWord in d]
	with open(cleanedData, "w") as f:
		f.writelines(list(set(data)))

def removeExistedTweets(file,tweets):
	with open(file, "r") as f:
		data = [d[:-1].strip() for d in f.readlines()]
	print("old",len(data))
	data=[d for d in data if d not in tweets]
	print("new",len(data))
	with open(file, "w") as f:
		f.writelines([d+"\n" for d in data])


def process():
	requiredword=None
	ProcessAllFiles("Data/pro/",cleantweets="Data/PROTweet.txt",cleanedData="Data/PROOut.csv",requireWord=requiredword)
	ProcessAllFiles("Data/anti/",cleantweets="Data/AntiTweet.txt",cleanedData="Data/AntiOut.csv",requireWord=requiredword)

	with open("Data/PROTweetProccessed.txt", "r") as f:
		pdata = [d[:-1].strip() for d in f.readlines()]
	with open("Data/AntiTweetProcessed.txt", "r") as f:
		adata = [d[:-1].strip() for d in f.readlines()]

	removeExistedTweets("Data/PROTweet.txt",pdata+adata)
	removeExistedTweets("Data/AntiTweet.txt",pdata+adata)


process()
