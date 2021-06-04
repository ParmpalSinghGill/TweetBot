import tweepy
import random
import time,datetime
import os,threading
from Secrets import getKey
from requests.exceptions import ConnectionError

class BOT:
	def __init__(self,hashtag,user="USER",minn=5,maxx=25,base_file_path="DataFiles/NewFiles/"):
		self.user=user
		self.base_file_path=base_file_path
		print("Using",user,"ID")
		self.tweetnumber=1
		APIkey,APIsecretkey,Accesstoken,Accesstokensecret=getKey(user)

		self.hashtag=hashtag
		self.minn,self.maxx=minn,maxx
		self.tweetmaxlength=280

		# Authenticate to Twitter
		self.spsymbol="&^$"
		auth = tweepy.OAuthHandler(APIkey, APIsecretkey)
		auth.set_access_token(Accesstoken, Accesstokensecret)
		# Create API object
		self.api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

	def retweet(self,tweet,tids=[]):
		try:
			if tweet.retweeted:
				tids.append(str(tweet.id))
				print("$$$$$$$****************************  Already Retweeted",self.user,tweet.id,tweet.text.replace("\n","\\n"))
				return True
			elif tweet.id not in tids:
				self.api.retweet(tweet.id)
				if self.user!="ERRPRSTG":
					self.api.create_favorite(tweet.id)
				tids.append(str(tweet.id))
				print("$$$$$$$$$$$$$$$$$+++++++++++ Retweeted from",self.user,tweet.id,tweet.text.replace("\n","\\n"))
				time.sleep(random.randint(self.minn, self.maxx))
				return True
		except tweepy.error.TweepError as e:
			if e.api_code == 327:
				print("**************************** Already Tweeted",tweet.id)
				return True
			print("ERRROR During RETWEET with",self.user,tweet.id,e)
			if e.api_code in [185,429]:
				print("sleeping")
				time.sleep(random.randint(self.minn+2*60,self.maxx+5*60))
		return False

	def addExistedtweets(self,filepath,tweetidlist):
		if os.path.exists(filepath):
			with open(filepath, "r") as f:
				tweetidlist.extend([d[:-1].split(self.spsymbol)[0] for d in f.readlines()[1:]])
		else:
			with open(filepath, "w") as f:
				f.write("ID"+self.spsymbol+"TIME\n")


	def continuslyRetweet(self):
		alreadyTweeted="Intelegent/AlreadyTweeted/"+self.user+".csv"
		os.makedirs("Intelegent/AlreadyTweeted/",exist_ok=True)
		exceptionTweets="Intelegent/Exception/"+self.user+".csv"
		os.makedirs("Intelegent/Exception/",exist_ok=True)
		source="Intelegent/ToRetweet/"+datetime.datetime.now().strftime("Postive_IDS_%Y_%m_%d.csv")
		alreadyTweetedids=[]
		self.addExistedtweets(alreadyTweeted,alreadyTweetedids)
		self.addExistedtweets(exceptionTweets,alreadyTweetedids)
		while True:
			try:
				if not os.path.exists(source):
					continue
				with open(source, "r") as f:
					toretweet=([d[:-1] for d in f.readlines()])
				toretweet=[d for d in toretweet if d not in alreadyTweetedids]
				if len(toretweet)==0:
					print("All Tweetes are Retweeted")
					time.sleep(5*60)
					continue
				random.shuffle(toretweet)
				for tid in toretweet:
					try:
						tweet=self.api.get_status(tid)
					except tweepy.error.TweepError as e:
						if e.api_code == 144:
							alreadyTweetedids.append(tid)
							with open(exceptionTweets, "a") as f:
								f.write(
									tid + self.spsymbol + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
							continue
					if self.retweet(tweet,alreadyTweetedids):
						with open(alreadyTweeted, "a") as f:
							f.write(tid + self.spsymbol +datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ "\n")
					else:
						print("Returned False")
					if "retweeted_status" in dir(tweet):
						if self.retweet(tweet.retweeted_status,alreadyTweetedids):
							if tweet.retweeted_status.id in toretweet:
								toretweet.remove(tweet.retweeted_status.id)
							with open(alreadyTweeted, "a") as f:
								f.write(str(tweet.retweeted_status.id) + self.spsymbol +datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ "\n")
			except Exception as e:
				print("EXCEPTION in continuslyRetweet",e)

with open("TodayTag") as f:
	hashtag=[d[:-1] for d in f.readlines() if len(d)>2][:]

def ReweetUser(userid,mm):
	bot=BOT(hashtag,user=userid,minn=mm[0],maxx=mm[1])
	bot.continuslyRetweet()

def RetweetAll():
	user="USER"
	mm=(1,15)
	print("*********** Start Thread ",user)
	th=threading.Thread(target=ReweetUser,args=(user,mm))
	th.start()
	threds.append(th)

if __name__=="__main__":
	# RetweetAll()
	bot = BOT(hashtag, user="USER", minn=1, maxx=10)
	bot.continuslyRetweet()

