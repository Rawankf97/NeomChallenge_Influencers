from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import sqlite3
import threading
import os
import datetime
from sliding_window import Window
import action_based
from multiprocessing import Process, Queue
from flask import Flask


ckey = 'NtJfBOAWmEk8IHc16ZX1Xa08o'
csecret = 'fSNuS4GufFlQfofbHQA2RFREPORnIdswGMasxCrK3vcsqImnKr'
atoken = '792467080851419136-00fWXmEW57ySHjMZeBjGhfAuiRlmYIa'
asecret = 'Fe30kpGr4kluV2diYE3hzZ0QKFGofzcW4GHDTKULPpQs1'
"""
ckey = "dACc1SyJSy9dUsQG9Zvh6wqYc"
csecret = "WgN3Vf822bta0iqKfCMNksFRV3BXc6l1DWNOoMOKHWRAHdF0xz"
atoken = "728958577084399616-hnGHSrBILK8WSKErHOswrpAUue9SRvk"
asecret = "8MymupK42HkF4JVKykSfkOxmSz6Gb0rWoJjFXisSaMooP"
"""
# , is_quote_status, quoted_status, retweeted_status, retweeted


tableName = None
conn = None
c = None

# stopping values:
startTime = time.time()
count = 0
tweets = []
dataBuffer = False


# location constraint libraries:


# Query initialization varibles:
# Stream Constraints:
boundingBox = None
StreamLanguage = []
keywords = None
# Influence result filters:
isFollowersFilter = False
followersFrom = None
followersTo = None
verified = None
top_K = 10

tweetScore = 1
retweetScore = 1
qouteScore = 1
replyScore = 1

isLocationKeywordConstraint = 'N'
isLocationConstraint = 'N'
window_size = 1
update_interval = 0.5


class listener(StreamListener):
    def on_status(self, status):
        print(status)

    def on_error(self, status_code):
        print(status_code)

    def on_data(self, data):

        global startTime
        global count
        global tweets
        global dataBuffer
        global isLocationKeywordConstraint, keywords
        timeDef = time.time() - startTime

        if(timeDef < 5 or count > 150):

            """
            try:
                saveFile= open('riyadh1.json','a')
                saveFile.write(data)
                saveFile.close()
                return True
            except BaseException as e:
                print ('failed on data', str(e))
                time.sleep(5)
            """

            item = json.loads(data)

            if isLocationKeywordConstraint != 'Y':
                inText = True
            else:
                inText = False
                for keyword in keywords:
                    if keyword in item['text']:
                        inText = True
                        break

            if (inText):
                tweets.append(item)
                count += 1

        else:
            dataBuffer = True
            count = 0
            startTime = time.time()

        return True


def insertBuffer():
    global dataBuffer
    global tweets, tweetScore, retweetScore, qouteScore, replyScore

    while(True):
        if(dataBuffer is True):
            for item in tweets:
                Time = item['created_at']
                print(Time)
                Action_id = item['id_str']
                text = item['text']
                Action_Username = item['user']['screen_name']
                in_reply_to_screen_name = item['in_reply_to_screen_name']
                favourites_count = item['favorite_count']
                verified = item['user']['verified']
                followers_count = item['user']['followers_count']
                if 'retweeted_status' in item:  # causality user for retweet
                    Causality_Username = item['retweeted_status']['user']['screen_name']
                    Causality_id = item['retweeted_status']['user']['id_str']
                    Action_Type = retweetScore
                elif 'quoted_status' in item:  # causality user for quote tweet
                    Causality_Username = item['quoted_status']['user']['screen_name']
                    Causality_id = item['quoted_status']['user']['id_str']
                    Action_Type = qouteScore
                elif in_reply_to_screen_name is not None:
                    Causality_Username = in_reply_to_screen_name  # causality user for reply tweet
                    Causality_id = item['in_reply_to_status_id_str']
                    Action_Type = replyScore
                else:
                    Causality_Username = None  # causality user for original tweet is NULL
                    Causality_id = None
                    Action_Type = tweetScore

                if ('coordinates' in item):
                    if item['coordinates'] is not None:
                        coordinates = str(item['coordinates']['coordinates'])

                    else:
                        coordinates = None

                else:
                    coordinates = None

                c.execute('''INSERT INTO ''' + tableName + '''
                          (Time,Action_id,text,Action_Username,Causality_id,Causality_Username,favourites_count,Action_Type,verified,followers_count,coordinates) VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (Time, Action_id, text, Action_Username, Causality_id, Causality_Username, favourites_count, Action_Type, verified, followers_count, coordinates))
                conn.commit()

            tweets.clear()
            dataBuffer = False


def startStreamListiner():
    global boundingBox, isLocationKeywordConstraint, StreamLanguage, isLocationConstraint
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, listener())

    if (isLocationKeywordConstraint != 'Y' and isLocationConstraint != 'Y'):
        twitterStream.filter(track=keywords, languages=StreamLanguage)
    else:
        twitterStream.filter(locations=boundingBox, languages=StreamLanguage)


def calculateActionScore(scale):
    if scale == 5:
        return 1
    elif scale == 4:
        return 0.75
    elif scale == 3:
        return 0.50
    elif scale == 2:
        return 0.25
    elif scale == 1:
        return 0
    else:
        return None


def initializeQuery(query):
    # Stream constraints varibles:
    global boundingBox, StreamLanguage, keywords
    # Influence result filters:
    global isFollowersFilter, followersFrom, followersTo, verified, top_K, tweetScore, retweetScore, qouteScore, replyScore, isLocationConstraint, isLocationKeywordConstraint
    global window_size, update_interval
    # Keywords Constraint

    keyword, location, language, numOfInfluencers, minFollowers, maxFollowers, windowSize, updateInterval, actionWeights, actionScale, verified = query[
        'keyword'], query['location'], query['language'], query['numOfInfluencers'], query['minFollowers'], query['maxFollowers'], query['windowSize'], query['updateInterval'], query['actionWeights'], query['actionScale'], query['verified']

    if keyword:
        if type(keyword) is str:
            keywords = [keyword]
        else:
            keywords = keyword

    if location:
        boundingBox = []
        for i in location:
            boundingBox.append(float(i))

    if keyword and location:
        isLocationKeywordConstraint = 'Y'
    if not keyword and location:
        isLocationConstraint = 'Y'

    if language:
        if type(language) is str:
            StreamLanguage = [language]
        else:
            StreamLanguage = language

    if numOfInfluencers:
        top_K = int(numOfInfluencers)

    if actionScale:
        tweetScore, retweetScore, qouteScore, replyScore = calculateActionScore(int(actionScale['tweet'])), calculateActionScore(int(actionScale[
            'retweet'])), calculateActionScore(int(actionScale['quoteRetweet'])), calculateActionScore(int(actionScale['reply']))
    else:
        tweetScore = 1
        retweetScore = 1
        qouteScore = 1
        replyScore = 1

    if minFollowers:
        followersFrom = minFollowers
    else:
        followersFrom = 0

    if maxFollowers:
        followersTo = maxFollowers
    else:
        followersTo = 0

    if verified:
        verified = True

    if windowSize:
        window_size = float(windowSize)

    if updateInterval:
        update_interval = float(updateInterval)

    if actionWeights:
        tweetScore, retweetScore, qouteScore, replyScore = float(actionWeights['tweet']), float(actionWeights[
            'retweet']), float(actionWeights['quoteRetweet']), float(actionWeights['reply'])


def main(pqueue, data):

    global tableName, conn, c, window_size, update_interval

    print('Data to process is... ', data)
    initializeQuery(data)

    tableName = time.strftime("A%Y%m%d%H%M%S")
    databaseName = time.strftime("D%Y%m%d%H%M%S" + '.db')

    conn = sqlite3.connect(databaseName, check_same_thread=False)
    c = conn.cursor()

    tb_create = """CREATE TABLE """ + tableName + """
                (Time,Action_id,text,Action_Username,Causality_id,Causality_Username,favourites_count,Action_Type,verified,followers_count,coordinates)"""
    c.execute(tb_create)
    conn.commit()

    t1 = threading.Thread(target=startStreamListiner)
    t2 = threading.Thread(target=insertBuffer)

    window = Window(window_size, databaseName,
                    tableName, update_interval)
    mod = action_based.Model(followersFrom, followersTo, verified,
                             isFollowersFilter, top_K, tweetScore, tableName, pqueue, window_size, update_interval)
    window.add_observer(mod)
    p1 = Process(target=window.start)

    t1.start()
    t2.start()
    p1.start()
