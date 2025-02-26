import tweepy
import yaml
import time  # Import time module for delay

# Load API keys from config.yaml
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Authenticate with Twitter API
client = tweepy.Client(bearer_token=config["twitter"]["bearer_token"])

# Define search query
query = "AI -is:retweet lang:en"

# Add delay to avoid hitting rate limits
time.sleep(5)  # Wait 5 seconds before requesting

# Fetch recent tweets
tweets = client.search_recent_tweets(query=query, max_results=10)

# Print fetched tweets
if tweets.data:
    for tweet in tweets.data:
        print(tweet.text)
else:
    print("No tweets found.")
