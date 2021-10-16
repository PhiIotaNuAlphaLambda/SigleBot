import pickle
from pickle import Pickler, Unpickler
from datetime import datetime, timedelta, timezone

# within 21 days: recent_archive.txt
# older than 21 days: ancient_archive.txt

def add_to_recent_archive(tweet):
  try:
    f = open("recent_archive.txt", "rb")
    recent_list = Unpickler(f).load()
    f.close()
  except:
    recent_list = []
  recent_list.append(tweet)
  f = open("recent_archive.txt", "wb")
  Pickler(f).dump(recent_list)
  f.close()

def delete_already_tweeted(new_tweets):
  archive_old_retweets()

  try:
    f = open("recent_archive.txt", "rb")
    print("file opened")
    recent_tweets = Unpickler(f).load()
    print("recent_tweets loaded")
    print(recent_tweets)
    f.close()
  except:
    print("file open failed")
    return new_tweets
  
  not_duplicate_tweets = []
  old_urls = tweet_urls_list(recent_tweets)
  for tweet in new_tweets:
    if tweet.post_url not in old_urls:
      not_duplicate_tweets.append(tweet)
  return not_duplicate_tweets

def tweet_urls_list(tweets_list):
  urls = []
  for tweet in tweets_list:
    urls.append(tweet.post_url)
  return urls

def archive_old_retweets():
  try:
    file = open("recent_archive.txt", "rb")
    recent_archive = Unpickler(file).load()
    file.close()
    print("Archive Ancient: Loaded recent_archive.txt")
    print(recent_archive)
  except:
    print("Archive Ancient: Failed to open recent_archive.txt")
    return

  new_recent_archive = []
  add_to_ancient_archive = []
  
  today = datetime.now(tz=timezone.utc)
  for recent_tweet in recent_archive:
    if today - recent_tweet.tweet_datetime > timedelta(days=21):
      add_to_ancient_archive.append(recent_tweet)
    else:
      new_recent_archive.append(recent_tweet)
  
  recent_file = open("recent_archive.txt", "wb")
  Pickler(recent_file).dump(new_recent_archive)
  recent_file.close()

  try:
    ancient_file = open("ancient_archive.txt", "rb")
    ancient_list = Unpickler(ancient_file).load()
    ancient_file.close()
  except:
    ancient_list = []

  for tweet in add_to_ancient_archive:
    ancient_list.append(tweet)

  ancient_file = open("ancient_archive.txt", "wb")
  Pickler(ancient_file).dump(ancient_list)
  ancient_file.close()


