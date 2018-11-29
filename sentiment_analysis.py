from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def classify_sentiment(text):
    analyser = SentimentIntensityAnalyzer()
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

def main():
    parser = ArgumentParser()
    parser.add_argument("--text", help="text string from twitter to analyze", required=True)
    parser.add_argument("--user", help="limit to tweets from specified user", default='empty')
    args = parser.parse_args()
    text = args.text
    user = args.user

    if user == 'empty':
        file_path = 'archive/' + text.replace(' ', '_') + '.csv'
        plot_title_text = text
    else:
        text_with_user = text + ' from:{}'.format(user)
        file_path = 'archive/' + text_with_user.replace(' ', '_') + '.csv'
        plot_title_text = text_with_user

    df = pd.read_csv(file_path)
    num_tweets = df.shape[0]
    print('Classifying dataset of {} tweets.'.format(num_tweets))

    df['day'] = df['timestamp'].apply(get_day)
    df['month'] = df['timestamp'].apply(get_month)
    df['year'] = df['timestamp'].apply(get_year)
    df['sentiment'] = df['text'].apply(classify_sentiment)

    pd.set_option('display.max_columns', 500)
    print(df.head())

    # the following assumes we only have a month of data

    days = list(set(df['day'].tolist()))
    average_sentiments = []

    for day in days:
        sentiments = df[df['day'] == day]['sentiment'].tolist()
        average_sentiment = np.mean(sentiments)
        average_sentiments.append(average_sentiment)

    plt.bar([int(day) for day in days], average_sentiments, label='Daily Average Sentiment', color = 'c')
    plt.xlabel('Day in November 2018')
    plt.ylabel('Daily Average Sentiment')
    plt.title('Daily Average Sentiment for Tweets from Advanced Query: \"{}\"'.format(plot_title_text))
    plt.show()

if __name__ == '__main__':
    main()
