from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 50)

single_accounts = ['_from:elonmusk']
economy_tweets_news_accounts = ['economy_from:' + x for x in ['FoxNews', 'MSNBC', 'CNN', 'WSJ', 'cnbc']]

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

final_df = pd.merge(all_stocks, all_tweets, on='day_timestamp', how='left')
final_df.to_csv('final_datasets/tableau_input3.csv', index=False)
print(final_df.sample(100).head(100))
