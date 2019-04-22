import os
from datetime import datetime
from deps.utils import twitterApi
import pandas as pd
import pandas_gbq

def nfl_player_tweets(request):
    #gcp
    project = os.environ["PROJECT_ID"]
    destination_table = os.environ["DESTINATION_TABLE"]
    #twitter
    consumer_key = os.environ["CONSUMER_KEY"]
    consumer_secret = os.environ["CONSUMER_SECRET"]
    access_token = os.environ["ACCESS_TOKEN"]
    access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

    twitter = twitterApi(consumer_key=consumer_key,
                         consumer_secret=consumer_secret,
                         access_token=access_token,
                         access_token_secret=access_token_secret)

    q = """select distinct twitter from `{}.football.player_info` where twitter is not null order by 1"""
    nfl_player_twitters = pd.read_gbq(project_id=project,
                                      query=q.format(project),
                                      dialect="standard")

    df = twitter.get_tweet_list(list(nfl_player_twitters.twitter))
    pandas_gbq.to_gbq(df, project_id=project,
                      destination_table=destination_table,
                      if_exists="replace")
