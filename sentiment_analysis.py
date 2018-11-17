from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

parser = ArgumentParser()
parser.add_argument("--text", help="text string from twitter to analyze", required=True)
args = parser.parse_args()
search_string = args.text
file_path = 'archive/' + search_string.replace(' ', '_') + '.csv'

df = pd.read_csv(file_path)
num_tweets = df.shape[0]

print('Classifying dataset of {} tweets.'.format(num_tweets))
analyser = SentimentIntensityAnalyzer()

def classify_sentiment(text):
    sentiment_dict = analyser.polarity_scores(text)
    compound_sentiment = sentiment_dict['compound']
    return compound_sentiment

def split_stamp(stamp):
    return stamp.split('-')

def get_day(stamp):
    day = split_stamp(stamp)[2].split(' ')[0]
    return day

def get_month(stamp):
    month = split_stamp(stamp)[1]
    return month

def get_year(stamp):
    year = split_stamp(stamp)[0]
    return year

df['day'] = df['timestamp'].apply(get_day)
df['month'] = df['timestamp'].apply(get_month)
df['year'] = df['timestamp'].apply(get_year)
df['sentiment'] = df['text'].apply(classify_sentiment)

days = list(set(df['day'].tolist()))
average_sentiments = []

for day in days:
    sentiments = df[df['day'] == day]['sentiment'].tolist()
    average_sentiment = np.mean(sentiments)
    average_sentiments.append(average_sentiment)

plt.bar([int(day) for day in days], average_sentiments, label='Daily Average Sentiment', color = 'c')
plt.xlabel('Day in November 2018')
plt.ylabel('Daily Average Sentiment')
plt.title('Daily Average Sentiment for Tweets Containing the Phrase \"{}\"'.format(search_string))
plt.show()
