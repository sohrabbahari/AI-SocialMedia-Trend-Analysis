import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load sentiment analysis results
data_file = "data/sentiment_analysis_results.csv"

st.title("📊 AI Twitter Sentiment Analysis Dashboard")
st.write("This dashboard shows sentiment analysis of real-time tweets about AI.")

# Check if the sentiment analysis file exists
try:
    df = pd.read_csv(data_file)

    # Rename columns if necessary
    df = df.rename(columns={"Tweet": "Text"})  # Fix column name

    # Show raw tweet data
    st.subheader("🔹 Raw Tweets")
    st.dataframe(df[["Text", "Sentiment"]])

    # Count sentiment types
    sentiment_counts = df["Sentiment"].value_counts()

    # Create a bar chart
    st.subheader("📊 Sentiment Distribution")
    fig, ax = plt.subplots()
    sentiment_counts.plot(kind="bar", color=["green", "gray", "red"], ax=ax)
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Tweets")
    plt.xticks(rotation=0)
    st.pyplot(fig)

except FileNotFoundError:
    st.error("❌ No sentiment analysis results found! Run `sentiment_analysis.py` first.")

except KeyError:
    st.error("❌ The CSV file structure is incorrect. Check column names in `sentiment_analysis_results.csv`.")
    st.write("Detected columns:", df.columns.tolist())  # Debugging output
