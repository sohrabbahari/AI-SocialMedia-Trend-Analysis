import tweepy
import yaml
import pandas as pd
import os

# Load Twitter API keys from config.yaml
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Authenticate with Twitter API
client = tweepy.Client(bearer_token=config["twitter"]["bearer_token"])

# Define search query
query = "AI -is:retweet lang:en"

# Fetch tweets
tweets = client.search_recent_tweets(query=query, max_results=20, tweet_fields=["created_at", "text"])

# Ensure 'data/' directory exists
data_folder = "data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Process tweets
if tweets.data:
    tweet_list = [[tweet.id, tweet.created_at, tweet.text] for tweet in tweets.data]
    df = pd.DataFrame(tweet_list, columns=["Tweet_ID", "Timestamp", "Text"])
    
    # Save tweets to CSV
    df.to_csv(os.path.join(data_folder, "real_tweets.csv"), index=False)
    print("✅ Fetched and saved real tweets to 'data/real_tweets.csv'!")
else:
    print("❌ No tweets found. Try again later.")
