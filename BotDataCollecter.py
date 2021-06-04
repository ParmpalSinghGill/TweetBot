import tweepy
import time,datetime
import os
from Secrets import getKey
from tweepy.error import TweepError

class BOT:
	def __init__(self,hashtag,user="FARMER",minn=5,maxx=25,base_file_path="DataFiles/NewFiles/"):
		self.user=user
		self.base_file_path=base_file_path
		self.tweetnumber=1
		APIkey,APIsecretkey,Accesstoken,Accesstokensecret=getKey(user)

		self.hashtag=hashtag
		self.minn,self.maxx=minn,maxx
		self.doneTweet="DataFiles/PSGDONE.csv"
		self.AlwaysRemove="DataFiles/AlwaysRemove.txt"

		# Authenticate to Twitter
		self.spsymbol="&^$"
		auth = tweepy.OAuthHandler(APIkey, APIsecretkey)
		auth.set_access_token(Accesstoken, Accesstokensecret)
		# Create API object
		self.api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


	def getFullText(self,tid,imgpath="",videopath=""):
		status = self.api.get_status(tid, tweet_mode="extended")
		text=status.full_text
		try:
			text=status.retweeted_status.full_text
		except:
			pass
		if imgpath=="" and videopath=="":
			imgpath,videopath=self.getMedia(status)
		return text,imgpath,videopath

	def getImageUrl(self,tweet):
		imagesurl=[]
		try:
			media = tweet.entities.get('media', [])
			if (len(media) > 0):
				for med in media:
					imagesurl.append(med['media_url'])
		except:
			pass
		try:
			media = tweet.extended_entities.get('media', [])
			if (len(media) > 0):
				for med in media:
					imagesurl.append(med['media_url'])
		except:
			pass
		try:
			imagses=self.getImageUrl(tweet.retweeted_status)
			for img in imagses.split(":::::"):
				imagesurl.append(img)
		except:
			pass

		return ":::::".join(set(imagesurl))

	def getVideo(self,tweet):
		try:
			media = tweet.extended_entities.get('media', [])
			for med in media:
				varient=med["video_info"]["variants"]
				index=-1
				video=varient[index]
				while index>-5 and "bitrate" not in video:
					index-=1
					video=varient[index]
				if video["bitrate"]>1000:
					return video["url"]
		except:
			pass
		try:
			return self.getVideo(tweet.retweeted_status)
		except:
			pass

		return ""

	def getMedia(self,tweet):
		return self.getImageUrl(tweet),self.getVideo(tweet)
		# return self.getVideo(tweet)


	def saveTweet(self,tweet,tids,minrt,filepath="test.csv"):
		tid = tweet.id
		if tid in tids:
			return
		rt_Count = tweet.retweet_count
		if rt_Count >= minrt:
			imagepath, videopath = self.getMedia(tweet)
			fulltext,imagepath, videopath = self.getFullText(tid,imagepath,videopath)
			fulltext = fulltext.replace("\n", "\\n")
			line = self.spsymbol.join([str(tid), fulltext, imagepath, videopath]) + "\n"
			with open(filepath, "a") as f:
				f.write(line)


	def saveTweetsInFile(self, tweets, minrt=0, filepath="test.csv"):
		tids=[]
		if not os.path.exists(filepath):
			header=self.spsymbol.join(["ID","Text","Images","Video"])+"\n"
			with open(filepath,"w") as f:
				f.write(header)
		else:
			with open(filepath, "r") as f:
				data=f.readlines()
			tids=[int(d.split(self.spsymbol)[0]) for d in data[1:]]
			self.tweetnumber=len(tids)
		for tweet in tweets:
			self.saveTweet(tweet,tids,minrt,filepath)



	def saveTodaysTweet(self,n=5000):
		os.makedirs(self.base_file_path,exist_ok=True)
		while True:
			try:
				for tag in self.hashtag:
					self.saveTweetsInFile(self.api.search(q=tag, rpp=n), 0,
										  filepath=self.base_file_path + datetime.datetime.now().strftime("Base_FILE_%Y_%m_%d") + ".csv")
			except TweepError as e:
				print("Unable to Connect",e)
			time.sleep(60*1)


with open("TodayTag") as f:
	hashtag=[d[:-1] for d in f.readlines() if len(d)>2][:]

def Scraping():
	bot=BOT(hashtag,user="USER",minn=1,maxx=10,base_file_path="Intelegent/DataFiles/")
	# bot.RetweetFollower()
	bot.saveTodaysTweet()

if __name__=="__main__":
	Scraping()


