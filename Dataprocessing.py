import random,pickle
import numpy as np
basemodelpath="../models/"
def combineCapitalSingle(words):
	combinedWords=[]
	comword=""
	for word in words:
		if len(word)>1 or (len(word)==1 and not 65<=ord(word)<=90 and not 48<=ord(word)<=57 ) :
			if len(comword)>0:
				combinedWords.append(comword)
				comword=""
			combinedWords.append(word)
		else:
			comword+=word
	if len(comword) > 0:
		combinedWords.append(comword)
	return combinedWords

def dividehashTag(hasgtag):
	hasgtag=hasgtag.replace("_"," ")
	allwords=[]
	currentword=""
	for ch in hasgtag:
		if (65<=ord(ch)<=90 or 48<=ord(ch)<=57 or ch==" ") and len(currentword)>0:
			allwords.append(currentword)
			currentword=""
		if ch!=" ":
			currentword+=ch
	allwords.append(currentword)
	allwords=combineCapitalSingle(allwords)
	hasgtag=(" ".join(allwords))
	return hasgtag


def replcaeHashtag(sentence):
	if "#" in sentence:
		sentence1,sentence2=sentence.split("#",1)
		sentences=sentence2.strip().split(" ",1)
		if len(sentences)==1:
			hastag=dividehashTag(sentences[0])
			return sentence1.strip()+" "+hastag,[0]*len(sentence1.split())+[1]*len(hastag.split())
		else:
			hasgtag,sentence2=sentence2.split(" ",1)
			sentence1+dividehashTag(sentences[0])
			hashtag,(sentence2,mask)=dividehashTag(hasgtag),replcaeHashtag(sentence2)
			return sentence1.strip() +" "+ hashtag + " " + sentence2,[0]*len(sentence1.split())+[1]*len(hashtag.split())+mask

	return sentence.strip(),[0]*len(sentence.split())

def clearnSentence(sentence):
	for sep in ["\\n","।","॥"]:
		sentence = sentence.replace(sep, " ")
	while "  " in sentence:
		sentence=sentence.replace("  "," ")
	sentence=sentence.replace("!","").replace("\"","").replace("##","#")
	sentence="".join([s for s in sentence if ord(s)<5000])
	sentence,map=replcaeHashtag(sentence)
	while "  " in sentence:
		sentence=sentence.replace("  "," ")
	return sentence.strip(),map

def prepaireDict(all_sentences,minword=3):
	words=[d1 for data in all_sentences for d1 in data[0].split() if len(d1)>0]
	unique_word,un_count=np.unique(words, return_counts=True)
	unique_word=[w for w,c in zip(unique_word, un_count) if c>=minword]
	dict={w:i for w,i in zip(unique_word,range(1,1+len(unique_word)))}
	with open(basemodelpath+"Dict.pk","wb") as f:
		pickle.dump(dict,f)
	print("Total unique Word",len(dict))
	return dict

def convertdataToNumber(data,dict,label,padding=50):
	indata=[]
	for sent,masks in data:
		words=sent.split()
		assert len(words)==len(masks), "Issue in preprocessing"
		sentindex=[]
		maskindex=[]
		for word,wordmask in zip(words,masks):
			if word in dict:
				sentindex.append(dict[word])
				maskindex.append(wordmask)
		if len(sentindex)>padding:
			sentindex=sentindex[:padding]
			maskindex=maskindex[:padding]
		elif len(sentindex)<padding:
			maskindex=[0]*(padding - len(sentindex)) + maskindex
			sentindex=[0]*(padding-len(sentindex))+sentindex
		indata.append((np.array(sentindex),np.array([[1,0],[0,1]][label]),np.array(maskindex),sent))
	return indata



def prepaireData(padding=50,train=True):
	with open("Data/PROTweetProccessed.txt") as f:
		pro=[d[:-1] for d in f.readlines()]
	with open("Data/AntiTweetProcessed.txt") as f:
		anti=[d[:-1] for d in f.readlines()]
	if train:
		pro,anti=pro[:int(len(pro)*.8)],anti[:int(len(anti)*.8)]
	else:
		pro, anti = pro[int(len(pro)*.8):], anti[int(len(anti)*.8):]
	pro=list(filter(len,map(clearnSentence,pro)))
	anti=list(filter(len,map(clearnSentence,anti)))
	all_sentences=pro+anti
	if train:
		dict=prepaireDict(all_sentences)
	else:
		with open(basemodelpath+"Dict.pk", "rb") as f:
			dict=pickle.load(f)
	prodata=convertdataToNumber(pro,dict,0,padding=padding)
	antidata=convertdataToNumber(anti,dict,1,padding=padding)
	data=prodata+antidata
	random.shuffle(data)
	xdata=[d[0] for d in data]
	ydata=[d[1] for d in data]
	masks=[d[2] for d in data]
	senteces=[d[3] for d in data]
	return np.array(xdata),np.array(ydata),len(dict),np.array(masks),senteces

# xdata,ydata,vocab_size,masks,_=prepaireData()
#
# print(xdata[5].shape)
# print(masks[5].shape)

