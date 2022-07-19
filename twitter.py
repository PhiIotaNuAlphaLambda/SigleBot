from decouple import config
import tweepy
import re
from app import RetweetedTweet, db
from datetime import datetime
import pprint

pp = pprint.PrettyPrinter()

class NewTweet:
  
  def __init__(self, author_id, tweet_id, post_url, tweet_datetime):
    self.author_id = author_id
    self.tweet_id = tweet_id
    self.post_url = post_url,
    self.tweet_datetime = tweet_datetime


def initialize_tweepy_client():
  """
  Initializes and returns tweepy client based on credentials
  stored in environment variables.
  """
  client = tweepy.Client(
    bearer_token = config('TWITTER_BEARER_TOKEN'),
    consumer_key = config('TWITTER_API_KEY'),
    consumer_secret = config('TWITTER_API_SECRET'),
    access_token = config('SIGLEBOT_TOKEN'),
    access_token_secret= config('SIGLEBOT_SECRET')
  )
  return client


def query_twitter(tweepy_client):
  """
  Sends command to Twitter API to retrieve all tweets that include 'app.sigle.io' in
  any capacity.
  """
  query_string = 'url: app.sigle.io'
  twitter_response = tweepy_client.search_recent_tweets(query=query_string, tweet_fields=['entities', 'author_id', 'created_at'], max_results=100)
  return twitter_response


def verify_valid_url(arr_url_objs):
  """
  Returns URL object where index 0 is the correct Sigle-formatted url.
  """
  found_url = find_sigle_url(arr_url_objs)
  return found_url


def find_sigle_url(arr):
  """
  Identifies and returns Sigle-formatted blog post URL.
  """
  blog_url_re = r"https://app.sigle.io/[a-zA-z0-9._]+/[a-zA-z0-9_-]+"
  for url_obj in arr:
    match_url = re.search(blog_url_re, url_obj['expanded_url']).group()
    if match_url:
      return match_url
  raise Exception("No URLs match Sigle Blog Pattern.")


def organize_tweets(downloaded_tweets):
  """
  Returns list of tweets which have valid URL that matches the pattern for a story posted on a sigle.io blog.
  """
  new_tweets = []

  for tweet in downloaded_tweets.data:
    try:
      url = verify_valid_url(tweet.entities["urls"])
    except Exception as e:
      continue

    new_tweets.append(
      NewTweet(
        tweet.author_id,
        tweet.id,
        url,
        tweet.created_at
      )
    )
  return new_tweets


def deduplicate_tweets(new_tweets_list, model):
  """
  Compares list up tweets against recently tweeted links stored in database, removing them from the list of tweets that are to be retweeted.
  """
  new_tweets_list = deduplicate_own_list(new_tweets_list)

  new_tweets_list = deduplicate_in_db(new_tweets_list, model)
  return new_tweets_list


def deduplicate_in_db(new_tweets_list, model):
  db_pulled_urls = []
  db_tweets = model.query.all()
  for db_tweet in db_tweets:
    db_pulled_urls.append(db_tweet.post_url)

  deduplicated_tweets = []
  print(type(new_tweets_list[0].post_url[0]))
  for tweet in new_tweets_list:
    if tweet.post_url[0] not in db_pulled_urls:
      print(f"starting length {len(deduplicated_tweets)}")
      deduplicated_tweets.append(tweet)
      print(f"ending length {len(deduplicated_tweets)}")

  return deduplicated_tweets


def deduplicate_own_list(new_tweets_list):
  print(f"Original length {len(new_tweets_list)}")
  deduplicated_urls = []

  local_deduplicated_tweets = []

  for tweet in new_tweets_list:
    if tweet.post_url[0] not in deduplicated_urls:
      local_deduplicated_tweets.append(tweet)
      deduplicated_urls.append(tweet.post_url[0])

  print(f"Ending length {len(local_deduplicated_tweets)}")  
  return local_deduplicated_tweets


def log_retweeted_urls(successfully_retweeted_urls):
  """
  Record tweet into the DB to ensure it doesn't get tweeted again anytime soon.
  """
  for post_url in successfully_retweeted_urls:
    adding_tweet = RetweetedTweet(post_url=post_url, date_retweeted=datetime.now())
    db.session.add(adding_tweet)
    db.session.commit()
    print('tweet committed')
  
  return True


def send_retweets(cleaned_tweets_list, tweepy_client):
  successfully_retweeted_urls = []
  for tweet in cleaned_tweets_list:
    try:
      if config('DEBUG', cast=bool) is not True:
        tweepy_client.retweet(tweet.tweet_id)
      successfully_retweeted_urls.append(tweet.post_url[0])
      # print(f"Retweeted & Archived Tweet ID {tweet.tweet_id} with link to {tweet.post_url[0]}")
    except:
      continue
  return successfully_retweeted_urls


def activate_siglebot():
  """
  String of commands to run SigleBot's code.
  """
  tweepy_client = initialize_tweepy_client()
  downloaded_tweets = query_twitter(tweepy_client)
  downloaded_tweets = organize_tweets(downloaded_tweets)
  downloaded_tweets = deduplicate_tweets(downloaded_tweets, RetweetedTweet)
  sent_urls = send_retweets(downloaded_tweets, tweepy_client)
  log_retweeted_urls(sent_urls)
  return True
  