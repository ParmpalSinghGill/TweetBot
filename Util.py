import os,random
# import cv2
import numpy as np

def getPunjabiNumber(number):
	number=str(number)
	ascibase = ord("੦")-ord("0")
	punnum=""
	for num in number:
		punnum+=chr(ascibase+ord(num))
	return punnum

def getMixTweets():
	imgpath="Images/"
	with open("DataFiles/AllRownderTweet.txt", "r") as f:
		alrowder = [t.replace("\\n","\n") for t in f.readlines()]
	with open("DataFiles/SimpleTweets.txt", "r") as f:
		simpletweet = [t.replace("\\n","\n") for t in f.readlines()]
	with open("DataFiles/ImageTweet.txt", "r") as f:
		imagetweet = [t.replace("\\n","\n") for t in f.readlines()]
	images=[imgpath+f for f in os.listdir(imgpath) if "jpg" in f]
	random.shuffle(alrowder)
	random.shuffle(imagetweet)
	random.shuffle(images)
	imgtweet=[]
	for i,imt in enumerate(imagetweet):
		imp=images[i%len(images)]
		imgtweet.append((imt,imp))
	simpletweet=[(tw,None) for tw in simpletweet+alrowder]
	totaltweets=simpletweet+imgtweet
	random.shuffle(totaltweets)
	totaltweets=list(set(totaltweets))
	return totaltweets


def getSpecialTweets():
	with open("DataFiles/SpecialFile.txt", "r") as f:
		simpletweet = [t.replace("\\n","\n") for t in f.readlines()]
	totaltweets=[(tw,None) for tw in simpletweet]
	totaltweets
	random.shuffle(totaltweets)
	totaltweets=list(set(totaltweets))
	return totaltweets

def playVideo(videopath):

	# Create a VideoCapture object and read from input file
	cap = cv2.VideoCapture(videopath)
	# Check if camera opened successfully
	if (cap.isOpened() == False):
		print("Error opening video  file")
	while (cap.isOpened()):
		ret, frame = cap.read()
		if ret == True:
			# Display the resulting frame
			cv2.imshow('Frame', frame)
			# Press Q on keyboard to  exit
			if cv2.waitKey(25) & 0xFF == ord('q'):
				break
		# Break the loop
		else:
			break
	# When everything done, release
	# the video capture object
	cap.release()

def getਓਅ(num):
	st=ord("ਅ")
	ls=ord("ਹ")
	diff=ls-st
	fisrt=num//diff
	sec=num%diff
	word=""
	if fisrt>0:
		word+=chr(st+fisrt-1)
	return word+chr(st+sec)

def isTweetContainPunjabi(tweet):
	tweetpart=np.array([ord(t) for t in tweet[0]])
	tweeta=tweetpart>2564
	tweetb=tweetpart<2655
	tweetab=np.bitwise_and(tweeta,tweetb)
	return np.any(tweetab)

def getPunjabiTweet():
	tweets=getMixTweets()
	return list(filter(isTweetContainPunjabi,tweets))



if __name__=="__main__":
	tweets=getPunjabiTweet()
	tweets=[t[0].replace("\n","\\n")+"\n" for t in tweets]
	with open("DataFiles/TWEETIT.txt","w") as f:
		f.writelines(tweets)
	# for i in range(200):
	# 	print(getUrdaAda(i))
	# print(ord("ਅ"))
	# st=ord("ਅ")
	# for i  in range(st,st+90):
	# 	print(i,chr(i))
