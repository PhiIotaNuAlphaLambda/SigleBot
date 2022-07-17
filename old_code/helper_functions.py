import re
from new_tweet import NewTweet

def verify_valid_url(arr_url_objs):
  """
  Returns URL object where index 0 is the correct Sigle-formatted url.
  """
  arr_url_objs[0]['expanded_url'] = find_sigle_url(arr_url_objs)
  return arr_url_objs

def find_sigle_url(arr):
  """
  Identifies and returns Sigle-formatted blog post URL.
  """
  blog_url_re = r"https://app.sigle.io/[a-zA-z0-9._]+/[a-zA-z0-9_-]+"
  for url_obj in arr:
    match = re.search(blog_url_re, url_obj['expanded_url'])
    if match:
      return match.string
  raise Exception("No URLs match Sigle Blog Pattern.")

def delete_duplicate_links(tweets_list):
  """
  Compares the URL in each tweet.
  When duplicate, keeps the older post.
  """
  urls_list = []
  for tweet in tweets_list:
    if tweet.post_url not in urls_list:
      urls_list.append(tweet.post_url)

  
  for url in urls_list:
    compare_tweets = []
    compare_tweets_inds = []
    for i, tweet in enumerate(tweets_list):
      if url == tweet.post_url:
        compare_tweets.append(tweet)
        compare_tweets_inds.append(i)
    compare_tweets_inds.reverse()
    for ind in compare_tweets_inds:
      tweets_list.pop(ind)
    tweets_list.append(identify_newest_tweet(compare_tweets))
  
  return tweets_list

def identify_newest_tweet(tweets_list):
  newest_tweet = tweets_list[0]
  if len(tweets_list) == 1: return newest_tweet

  for tweet in tweets_list[1:]:
    if newest_tweet.tweet_datetime > tweet.tweet_datetime:
      newest_tweet = tweet
  
  return newest_tweet
          