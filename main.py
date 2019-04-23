import os
from datetime import datetime
from deps.utils import twitterApi
import pandas as pd
import pandas_gbq

def nfl_tweets(request):
    #gcp
    project = os.environ["PROJECT_ID"]
    destination_table = os.environ["DESTINATION_TABLE"]
    #twitter
    consumer_key = os.environ["CONSUMER_KEY"]
    consumer_secret = os.environ["CONSUMER_SECRET"]
    access_token = os.environ["ACCESS_TOKEN"]
    access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

    #twitter list members
    owner = os.environ["OWNER"]
    slug = os.environ["SLUG"]

    twitter = twitterApi(consumer_key=consumer_key,
                         consumer_secret=consumer_secret,
                         access_token=access_token,
                         access_token_secret=access_token_secret)

    twitter.run(project_id=project,
                destination_table=destination_table,
                owner=owner,
                slug=slug)

def mlb_tweets(request):
    #gcp
    project = os.environ["PROJECT_ID"]
    destination_table = os.environ["DESTINATION_TABLE"]
    #twitter
    consumer_key = os.environ["CONSUMER_KEY"]
    consumer_secret = os.environ["CONSUMER_SECRET"]
    access_token = os.environ["ACCESS_TOKEN"]
    access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

    #twitter list members
    owner = os.environ["OWNER"]
    slug = os.environ["SLUG"]

    twitter = twitterApi(consumer_key=consumer_key,
                         consumer_secret=consumer_secret,
                         access_token=access_token,
                         access_token_secret=access_token_secret)

    twitter.run(project_id=project,
                destination_table=destination_table,
                owner=owner,
                slug=slug)
