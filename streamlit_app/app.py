import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import tweepy
import yaml
from transformers import pipeline

# Load Twitter API keys from config.yaml
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Authenticate with Twitter API
client = tweepy.Client(bearer_token=config["twitter"]["bearer_token"])

# Load BERT Sentiment Analysis Model
sentiment_model = pipeline("sentiment-analysis")

# Streamlit UI - Title & Description
st.title("📊 AI Twitter Sentiment Analysis Dashboard")
st.write("Analyze live Twitter data with AI-powered sentiment analysis!")

# Dark Mode Styling
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stButton button {
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# User input for tweet search
query = st.text_input("🔍 Enter a search keyword for Twitter (e.g., 'AI')", "AI")

# Fetch Tweets Button
if st.button("Fetch Tweets"):
    with st.spinner("Fetching tweets..."):
        tweets = client.search_recent_tweets(query=query, max_results=10, tweet_fields=["created_at", "text"])

        if tweets.data:
            # Analyze Sentiment with BERT
            df = pd.DataFrame([[tweet.text, sentiment_model(tweet.text)[0]["label"]] for tweet in tweets.data], 
                              columns=["Text", "Sentiment"])

            # Display raw tweets
            st.subheader("🔹 Raw Tweets")
            st.dataframe(df)

            # Sentiment distribution
            sentiment_counts = df["Sentiment"].value_counts()
            fig, ax = plt.subplots()
            sentiment_counts.plot(kind="bar", color=["green", "gray", "red"], ax=ax)
            plt.xlabel("Sentiment")
            plt.ylabel("Number of Tweets")
            plt.xticks(rotation=0)
            st.subheader("📊 Sentiment Distribution")
            st.pyplot(fig)

            # Show Sentiment Insights
            positive_percent = (df["Sentiment"] == "POSITIVE").sum() / len(df) * 100
            negative_percent = (df["Sentiment"] == "NEGATIVE").sum() / len(df) * 100
            st.metric(label="😊 Positive Sentiment", value=f"{positive_percent:.2f}%")
            st.metric(label="😡 Negative Sentiment", value=f"{negative_percent:.2f}%")

        else:
            st.warning("No tweets found! Try a different keyword.")
