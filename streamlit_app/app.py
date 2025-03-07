import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import tweepy
import yaml
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from wordcloud import WordCloud
from transformers import pipeline

# Load API keys from config.yaml
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
        tweets = client.search_recent_tweets(
            query=query, max_results=10, tweet_fields=["created_at", "text", "geo"]
        )

        if tweets.data:
            # Analyze Sentiment with BERT
            df = pd.DataFrame(
                [[tweet.text, sentiment_model(tweet.text)[0]["label"]] for tweet in tweets.data], 
                columns=["Text", "Sentiment"]
            )

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

            # Generate Word Cloud
            st.subheader("☁️ Word Cloud of AI Tweets")
            all_words = " ".join(df["Text"])
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_words)
            st.image(wordcloud.to_array(), use_column_width=True)

            # AI Sentiment Map
            st.subheader("🌎 AI Sentiment by Location")

            # Initialize Map
            map = folium.Map(location=[20, 0], zoom_start=2)  # Centered globally
            geolocator = Nominatim(user_agent="geoapiExercises")

            # Try to extract location and plot on map
            for text in df["Text"]:
                try:
                    location = geolocator.geocode(text)  # Convert tweet text into location
                    if location:
                        sentiment_color = "green" if "POSITIVE" in text else "red" if "NEGATIVE" in text else "gray"
                        folium.Marker(
                            [location.latitude, location.longitude],
                            popup=text,
                            icon=folium.Icon(color=sentiment_color),
                        ).add_to(map)
                except:
                    pass  # Ignore errors if location is missing

            # Display the Map
            folium_static(map)

        else:
            st.warning("No tweets found! Try a different keyword.")
