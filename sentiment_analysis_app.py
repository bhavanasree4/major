import streamlit as st
from googleapiclient.discovery import build
import tweepy
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import emoji

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()
def get_youtube_comments(video_id, api_key, max_results=50):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results
    )
    response = request.execute()
    
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    
    return comments
def get_twitter_tweets(query, api_key, api_secret, access_token, access_token_secret, max_tweets=50):
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    tweets = []
    for tweet in tweepy.Cursor(api.search_tweets, q=query, lang="en").items(max_tweets):
        tweets.append(tweet.text)
    
    return tweets
def analyze_sentiment(text):
    sentiment = sia.polarity_scores(text)
    
    if sentiment['compound'] >= 0.05:
        return "Positive 😀"
    elif sentiment['compound'] <= -0.05:
        return "Negative 😡"
    else:
        return "Neutral 😐"
emoji_sentiment = {
    "😀": "Positive", "😂": "Positive", "😍": "Positive", 
    "😢": "Negative", "😡": "Negative", "😐": "Neutral"
}

def extract_emoji_sentiment(text):
    emojis = [char for char in text if char in emoji.UNICODE_EMOJI['en']]
    sentiments = [emoji_sentiment.get(e, "Unknown") for e in emojis]
    return emojis, sentiments
st.title("📊 Social Media Sentiment Analysis")

# YouTube Section
st.header("🎥 Analyze YouTube Comments")
video_id = st.text_input("Enter YouTube Video ID")
youtube_api_key = "YOUR_YOUTUBE_API_KEY"  # Replace with your real API key

if st.button("Get YouTube Comments"):
    comments = get_youtube_comments(video_id, youtube_api_key)
    for comment in comments:
        sentiment = analyze_sentiment(comment)
        emojis, emoji_sentiments = extract_emoji_sentiment(comment)
        st.write(f"**Comment:** {comment}")
        st.write(f"**Sentiment:** {sentiment}")
        if emojis:
            st.write(f"**Emojis:** {''.join(emojis)} - Sentiment: {emoji_sentiments}")

# Twitter Section
st.header("🐦 Analyze Twitter Tweets")
tweet_query = st.text_input("Enter a hashtag or keyword")
twitter_api_key = "YOUR_TWITTER_API_KEY"
twitter_api_secret = "YOUR_TWITTER_API_SECRET"
twitter_access_token = "YOUR_TWITTER_ACCESS_TOKEN"
twitter_access_secret = "YOUR_TWITTER_ACCESS_SECRET"

if st.button("Get Twitter Tweets"):
    tweets = get_twitter_tweets(tweet_query, twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_secret)
    for tweet in tweets:
        sentiment = analyze_sentiment(tweet)
        emojis, emoji_sentiments = extract_emoji_sentiment(tweet)
        st.write(f"**Tweet:** {tweet}")
        st.write(f"**Sentiment:** {sentiment}")
        if emojis:
            st.write(f"**Emojis:** {''.join(emojis)} - Sentiment: {emoji_sentiments}")
