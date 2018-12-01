from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from argparse import ArgumentParser
from datetime import datetime
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

def dates_and_average_sentiment(df):

    time_sentiment_dict = {}
    years = list(set(df['year'].tolist()))
    for year in years:
        year_df = df[df['year'] == year]
        months = list(set(year_df['month'].tolist()))
        for month in months:
            month_df = year_df[year_df['month'] == month]
            days = list(set(month_df['day'].tolist()))
            for day in days:
                sentiments = month_df[month_df['day'] == day]['sentiment'].tolist()
                average_sentiment = np.mean(sentiments)
                month_day_string = year + '-' + month + '-' + day
                time_sentiment_dict[month_day_string] = average_sentiment
    date_key = lambda x: datetime.strptime(x[0], '%Y-%m-%d')
    ordered_dict = dict(sorted(time_sentiment_dict.items(), key=date_key))
    return ordered_dict

def add_daily_average_sentiment(df, dates_sentiments):

    df['day_timestamp'] = df['timestamp'].apply(lambda x: x.split(' ')[0])
    df['day_average_sentiment'] = df['day_timestamp'].apply(lambda x: dates_sentiments[x])
    return df

def clean_and_sort_df(df, sort_col='timestamp'):

    cols = ['tweet-id','user','fullname','text','timestamp','day_timestamp','sentiment','day_average_sentiment','likes','replies','retweets']
    df = df[cols]
    df = df.sort_values(by=sort_col)
    df['day_timestamp'] = pd.to_datetime(df.day_timestamp)
    return df

def plot_dates_sentiments(df, plot_title_text):

    timestamps = df['day_timestamp'].tolist()
    average_sentiments = df['day_average_sentiment'].tolist()
    plt.bar(timestamps, average_sentiments, label='Daily Average Sentiment', color = 'c')
    plt.xlabel('Day in 2018')
    plt.ylabel('Daily Average Sentiment')
    plt.title('Daily Average Sentiment for Tweets from Advanced Query: \"{}\"'.format(plot_title_text))
    plt.show()

def main():

    parser = ArgumentParser()
    parser.add_argument("--text", help="text string from twitter to analyze", required=True)
    parser.add_argument("--user", help="limit to tweets from specified user", default='empty')
    args = parser.parse_args()
    text = args.text
    user = args.user

    if user == 'empty':
        file_path = 'scrape_archive/' + text.replace(' ', '_') + '.csv'
        plot_title_text = text
    else:
        text_with_user = text + ' from:{}'.format(user)
        file_path = 'scrape_archive/' + text_with_user.replace(' ', '_') + '.csv'
        plot_title_text = text_with_user

    df = pd.read_csv(file_path)
    num_tweets = df.shape[0]
    print('Classifying dataset of {} tweets.'.format(num_tweets))

    df['day'] = df['timestamp'].apply(get_day)
    df['month'] = df['timestamp'].apply(get_month)
    df['year'] = df['timestamp'].apply(get_year)
    df['sentiment'] = df['text'].apply(classify_sentiment)

    dates_sentiments = dates_and_average_sentiment(df)
    df = add_daily_average_sentiment(df, dates_sentiments)
    df = clean_and_sort_df(df)

    save_text = plot_title_text.replace(' ', '_')
    df.to_csv('dashboard_archive/{}.csv'.format(save_text), index=False)
    plot_dates_sentiments(df, plot_title_text)

if __name__ == '__main__':

    main()
