import pandas as pd
pd.set_option('display.max_columns', 50)

tweets = ['economy_from:' + x for x in ['FoxNews', 'MSNBC', 'CNN', 'realDonaldTrump']]
tweet_dfs = []
for tweet_source in tweets:
	df = pd.read_csv('dashboard_archive/{}.csv'.format(tweet_source))
	tweet_dfs.append(df)

all_tweets = pd.concat(tweet_dfs, ignore_index=True)
all_tweets = all_tweets.drop_duplicates(subset=['text'])

stocks = ['^DJI', '^GSPC', 'AMZN', 'XOM']
stock_dfs = []
for stock in stocks:
	df = pd.read_csv('stock_archive/{}.csv'.format(stock))
	df['Index'] = stock
	stock_dfs.append(df)

all_stocks = pd.concat(stock_dfs, ignore_index=True)
all_stocks = all_stocks.drop_duplicates()

all_stocks = all_stocks[['Date', 'Open', 'Close', 'Index']]
all_stocks = all_stocks.rename(index=str, columns={"Date": "day_timestamp"})

final_df = pd.merge(all_stocks, all_tweets, on='day_timestamp', how='left')
final_df.to_csv('final_datasets/tableau_input1.csv', index=False)
