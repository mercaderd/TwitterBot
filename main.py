#! ./venv/bin/python3

import tweepy
import time
import feedparser
import hashlib
import random
import sys
import urllib.request
from datetime import datetime
import pickle

from dotenv import dotenv_values


def get_log_str(string):
    return str(datetime.now())+': '+string+'\n'


def log(filename, string):
    logfile=open(filename, 'a')
    logfile.write(get_log_str(string))
    logfile.close()


def get_first_entry(rss_url):
    rss = feedparser.parse(rss_url)
    return rss.entries[0]


def get_rss_feed(rss_url):
    return feedparser.parse(rss_url)


def download_image(url, filename):
    local_filename, headers = urllib.request.urlretrieve(url, filename)
    return local_filename


def init_hashes(filename):
    try:
        f = open(filename,'rb')
        return pickle.load(f)
    except:
        return []


def dump_hashes(filename, hashes):
    if hashes:
        pickle.dump(hashes, open(filename,'wb'))
        return True
    return False




def main():
    config = dotenv_values(".env")
    # enter the corresponding information from your Twitter application:
    CONSUMER_KEY = config['CONSUMER_KEY']
    CONSUMER_SECRET = config['CONSUMER_SECRET']
    ACCESS_KEY = config['ACCESS_KEY']
    ACCESS_SECRET = config['ACCESS_SECRET']
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    logfilename = config['logfile']
    tweetshashesfile = config['hashfile']

    fileimage = config['imagefile']
    ImageIndex = 1;

    filename = open(config['rssfile'], 'r')
    f = filename.readlines()
    filename.close()

    Rmin = 600
    Rmax = 2400
    MaxHashNum = 1000
    MaxEntriesNum = 5

    usernames = config['usernames'].split(',')

    tweetshash = init_hashes(tweetshashesfile)

    while True:
        random.shuffle(f)
        for line in f:
            # print str(datetime.now())
            logstr = str(f.index(line))
            log(logfilename, logstr)
            lista = line.split(' ')
            rss_url = lista[1]
            twtag = lista[0]
            rss = get_rss_feed(rss_url)
            if rss:
                for entrie in rss.entries:
                    if (rss.entries.index(entrie) > MaxEntriesNum): break
                    # print rss.entries.index(entrie)
                    currententriehash = hashlib.md5(entrie.link.encode('utf8') + entrie.title.encode('utf8')).hexdigest()
                    if currententriehash not in tweetshash:
                        tweetshash.append(currententriehash)
                        if (len(tweetshash) > MaxHashNum): tweetshash.pop(0)
                        if dump_hashes(tweetshashesfile, tweetshash):
                            logstr = 'Dumped:' + currententriehash
                            log(logfilename, logstr)
                        tweet = twtag + ' ' + entrie.title + ' ' + entrie.link
                        if (len(entrie.links) > 1):
                            ImageIndex = len(entrie.links) - 1
                        else:
                            ImageIndex = 0;
                        # print ImageIndex
                        try:
                            if (entrie.links[ImageIndex].type == 'image/jpeg'):
                                download_image(entrie.links[ImageIndex].href, fileimage)
                                api.update_status_with_media(tweet, fileimage)

                            else:
                                api.update_status(tweet)

                            logstr = 'TW: ' + tweet
                            log(logfilename, logstr)
                        except tweepy.TweepyException as e:
                            # print "Unexpected error:", sys.exc_info()[0]
                            logstr = 'Error posting tweet: ' + tweet + e.response.text
                            log(logfilename, logstr)
                        SleepTime = random.randint(Rmin, Rmax)
                        logstr = 'Going to sleep for ' + str(SleepTime) + ' secs.'
                        # print logstr
                        log(logfilename, logstr)
                        time.sleep(SleepTime)  # No more tweets in some time
                    else:
                        try:
                            logstr = 'There is no new feed from ' + entrie.id
                        except:
                            logstr = 'There is no new feed from ' + 'UNKNOWN'

                        log(logfilename, logstr)
        for username in usernames:
            try:
                logstr = 'Getting user ' + username
                log(logfilename, logstr)
                user = api.get_user(screen_name=username)
            except tweepy.TweepyException as e:
                logstr = 'Error getting tweets from user ' + username
                log(logfilename, logstr)
                user = None
            if user:
                for status in tweepy.Cursor(api.user_timeline, user_id=user.id).items(4):
                    if not status.retweeted:
                        api.retweet(status.id)
                        logstr = 'Retweeted: ' + status.text
                        log(logfilename, logstr)
                        SleepTime = random.randint(Rmin, Rmax)
                        logstr = 'Going to sleep for ' + str(SleepTime) + ' secs.'
                        # print logstr
                        log(logfilename, logstr)
                        time.sleep(SleepTime)  # No more tweets in some time


if __name__ == '__main__': 
    main()
