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

    def tweets_to_df(self, handle, date=datetime.now().strftime("%Y-%m-%d"), days=1):
      api = self.twitter_auth()
      days_since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
      timeline = [r for r in tweepy.Cursor(api.user_timeline,
                                           lang="en",
                                           id=handle,
                                           since=days_since).items(15)]
      tweets = [[tweet.created_at,tweet.favorite_count, tweet.retweet_count, tweet.text, tweet.id] for tweet in timeline if not tweet.retweeted]

      #transform
      df = pd.DataFrame(tweets, columns = ['created_at', 'favorite_count', 'retweet_count', 'text', 'id'])
      df['created_at'] = df['created_at'] - timedelta(hours=4)
      df = df[df['created_at'].apply(lambda x: x.strftime('%Y-%m-%d')) == date]
      df['handle'] = handle
      df['text'] = df['text'].apply(lambda x: x.replace(u'\r', u' ').replace(u'\n', u' ') if isinstance(x, str) or isinstance(x, unicode) else x)
      return df

    def get_tweet_list(self, handles, date):
      start_time = datetime.now()
      tweet_list = []
      for handle in handles:
        current_time = datetime.now()
        time_diff = (current_time - start_time).seconds
        if time_diff < 300:
          try:
            tweet_list.append(self.tweets_to_df(handle, date))
          except:
            print("%s does not exist" % handle)
        else:
          break
      return pd.concat(tweet_list, axis=0, ignore_index=True)

    def get_list_members(self, owner, slug):
      """
      From any Twitter List, get all of the accounts
      Example: get_list_members(owner='sn_nfl', slug='NFL-Beat-reporter-list')
      Returns: a Pandas DataFrame of all Twitter handles in this list
      """
      api = self.twitter_auth()
      members = []
      # without this you only get the first 20 list members
      for page in tweepy.Cursor(api.list_members, owner, slug).items():
        members.append(page)
      # create a list containing all usernames
      return [m.screen_name for m in members]

    def run(self, owner, slug, project_id, destination_table, date=datetime.now().strftime('%Y-%m-%d')):
      members = self.get_list_members(owner, slug)
      tweets = self.get_tweet_list(members, date)
      tweets.to_gbq(project_id='{}'.format(project_id),
                         destination_table='{}_{}'.format(destination_table, date.replace("-","")), if_exists="replace")
