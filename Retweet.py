from BotDataCollecter import Scraping
from TweetClassification import TweetClassification
from RetwwetBot import RetweetAll
import threading
import sys




th1=threading.Thread(target=Scraping)
th1.start()
th1=threading.Thread(target=TweetClassification)
th1.start()
th1=threading.Thread(target=RetweetAll)
th1.start()



