from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 50)

def isNaN(num):
    return num != num

def a(user):
	if isNaN(user):
		return float('NaN')
	else:
		return user_retweet_dict[user]

def d(row):
	user = row['user']
	retweets = row['retweets']
	if isNaN(user):
		return float('NaN')
	else:
		user_average = user_retweet_dict[user]
		return retweets - user_average

single_accounts = ['_from:elonmusk'] + ['_from:realDonaldTrump']
economy_tweets_news_accounts = ['economy_from:' + x for x in ['FoxNews', 'CNN', 'WSJ', 'cnbc']]

tweets = economy_tweets_news_accounts + single_accounts
tweet_dfs = [pd.read_csv('dashboard_archive/{}.csv'.format(source)) for source in tweets]
all_tweets = pd.concat(tweet_dfs, ignore_index=True)

stocks = ['^DJI', '^GSPC', 'AMZN', 'XOM', 'TSLA']
stock_dfs = []
for stock in stocks:
	df = pd.read_csv('stock_archive/{}.csv'.format(stock))
	df['Symbol'] = stock
	stock_dfs.append(df)

all_stocks = pd.concat(stock_dfs, ignore_index=True)
all_stocks = all_stocks.drop_duplicates()

all_stocks = all_stocks[['Date', 'Open', 'Close', 'Volume', 'Symbol']]
all_stocks = all_stocks.rename(index=str, columns={"Date": "day_timestamp"})

standard_scaler = StandardScaler()
minmax_scaler = MinMaxScaler(feature_range=(-1, 1))
close_prices = all_stocks['Close'].values.reshape(-1, 1)
all_stocks['standard_scaled_close'] = standard_scaler.fit_transform(close_prices)
all_stocks['minmax_scaled_close'] = minmax_scaler.fit_transform(close_prices)

df = pd.merge(all_stocks, all_tweets, on='day_timestamp', how='left')

mean_df = df.groupby('user', as_index=False)['retweets'].mean()
user_retweet_dict = dict(zip(mean_df['user'].tolist(), mean_df['retweets'].tolist()))

df['average'] = df['user'].apply(a)
df['difference'] = df.apply(d, axis=1)

df.to_csv('final_datasets/tableau_input4.csv', index=False)
print(df.sample(100).head(100))
