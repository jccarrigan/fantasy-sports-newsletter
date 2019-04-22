from datetime import datetime, timedelta

import pandas as pd
import tweepy

class twitterApi:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key=consumer_key
        self.consumer_secret=consumer_secret
        self.access_token=access_token
        self.access_token_secret=access_token_secret


    def twitter_auth(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        return tweepy.API(auth)

    def tweets_to_df(self, handle, days=1):
      api = self.twitter_auth()
      days_since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
      timeline = [r for r in tweepy.Cursor(api.user_timeline,
                                           lang="en",
                                           id=handle,
                                           since=days_since).items(15)]
      tweets = [[tweet.created_at,tweet.favorite_count, tweet.favorited, tweet.retweet_count, tweet.text, tweet.id] for tweet in timeline]
      df = pd.DataFrame(tweets, columns = ['created_at', 'favorite_count', 'favorited', 'retweet_count', 'text', 'id'])
      df['handle'] = handle
      df['text'] = df['text'].apply(lambda x: x.replace(u'\r', u' ') if isinstance(x, str) or isinstance(x, unicode) else x)
      df['text'] = df['text'].apply(lambda x: x.replace(u'\n', u' ') if isinstance(x, str) or isinstance(x, unicode) else x)
      return df

    def get_tweet_list(self, handles):
      start_time = datetime.now()
      tweet_list = []
      for handle in handles:
        current_time = datetime.now()
        time_diff = (current_time - start_time).seconds
        if time_diff < 300:
          try:
            tweet_list.append(self.tweets_to_df(handle))
          except:
            print("%s does not exist" % handle)
        else:
          break
      return pd.concat(tweet_list, axis=0, ignore_index=True)
