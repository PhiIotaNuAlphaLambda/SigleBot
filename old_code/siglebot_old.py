import tweepy
import secrets
import time
from new_tweet import NewTweet
from helper_functions import delete_duplicate_links, verify_valid_url, delete_duplicate_links
import tweet_log_handler as log




def retweet_sigle_posts(wait_time_minutes):

  print("Checking for new blog posts to tweet.")

  client = tweepy.Client(
    bearer_token = secrets.BEARER_TOKEN,
    consumer_key = secrets.API_KEY,
    consumer_secret = secrets.API_SECRET,
    access_token = secrets.SIGLEBOT_TOKEN,
    access_token_secret= secrets.SIGLEBOT_SECRET
  )

  query = "url: app.sigle.io"

  twitter_response = client.search_recent_tweets(query=query, tweet_fields=['entities', 'author_id', 'created_at'], max_results=100)

  new_tweets = []

  # print(twitter_response.data[0]["created_at"].year)

  for tweet in twitter_response.data:
    try:
      tweet.entities["urls"] = verify_valid_url(tweet.entities["urls"])
    except Exception as e:
      continue

    new_tweets.append(
      NewTweet(
        tweet.author_id,
        tweet.id,
        tweet.entities["urls"][0]['expanded_url'],
        tweet.created_at
      )
    )

  new_tweets = delete_duplicate_links(new_tweets)

  new_tweets = log.delete_already_tweeted(new_tweets)

  for tweet in new_tweets:
    try:
      client.retweet(tweet.tweet_id)
      log.add_to_recent_archive(tweet)
      print(f"Retweeted & Archived Tweet ID {tweet.tweet_id} with link to {tweet.post_url}")
    except:
      continue

  print(f"Waiting {wait_time_minutes} minutes ...")
  time.sleep(wait_time_minutes * 60)




print("How often would you like to loop?\nEnter time in minutes:")
loop_time = int(input())
while True:
  retweet_sigle_posts(loop_time)