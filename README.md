# Intelegent RetweetBot
The idea is to retweet the tweets with particular hashtag to make it in trend. We can simply scrap tweet by tag and retweet. But thier are some anti tweets with our hashtag.
so the the concept of Intelegent Bot come. Here we Scrap the Tweets with particular word and then classify my deep learning model to check whether it's pro tweet or anti tweet.
save the tweetids of pro and ant tweet and retweet the pro tweet only.

### Steps
#### 1. Make Developer account
first step is make developer account by visit https://developer.twitter.com/en/apply-for-access
you need to follow the steps and you will get the APIkey,APIsecretkey,Accesstoken,Accesstokensecret
then save it in format
{"USER":[APIkey,APIsecretkey,Accesstoken,Accesstokensecret]}
in file Secret.json
You can add multiple accouts if want.
#### 2. Data Collection
second step is Data collection.
Add hashtag for you want to collect data in file named TODAY
Run the BotDataCollector by
```python BotDataCollector.py USER```
User is same we set in json file
Run it by adding pro and anti tweet tags

#### 3. Data Processing
In this place all protweetfiles in Data/pro directory and anti in Data/anti direcotry
then run
```python Cleaning.py```
it will add Data/PROTweetProccessed.txt and Data/AntiTweetProcessed.txt files
check it manualy and correct the tweets if found some wrong.

#### 3. Train Netwok
The Start Training by 
```python NeuralNetwork.py```
it will save the model.

#### 4. Run Retweetbot.
Now run the
```python Retweet.py.py```
it will data collection , classification and retweet the pro tweets only








