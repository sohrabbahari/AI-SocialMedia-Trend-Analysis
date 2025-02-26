import os  # ✅ Import the missing module
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download NLTK resources
nltk.download("vader_lexicon")

# Ensure 'data/' directory exists before saving the file
data_folder = "data"  # Change path to match project structure
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Sample tweets (Replace with real Twitter data)
tweets = [
    "AI is changing the world in amazing ways! 🚀",
    "This AI model is the worst thing I have ever seen 😡",
    "I'm not sure about AI, it seems useful but also risky.",
]

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Analyze sentiment of each tweet
results = []
for tweet in tweets:
    sentiment_score = sia.polarity_scores(tweet)["compound"]
    sentiment = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
    results.append([tweet, sentiment_score, sentiment])

# Convert to DataFrame
df = pd.DataFrame(results, columns=["Tweet", "Sentiment Score", "Sentiment"])

# Print results
print(df)

# Save results to CSV
df.to_csv(os.path.join(data_folder, "sentiment_analysis_results.csv"), index=False)
print("✅ Sentiment analysis results saved in 'data/sentiment_analysis_results.csv'!")
