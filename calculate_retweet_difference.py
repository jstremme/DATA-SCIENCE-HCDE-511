import pandas as pd 
import numpy as np
import math

pd.set_option('display.max_columns', 50)

df = pd.read_excel('final_viz/tableau_input3.xlsx')

mean_df = df.groupby('user', as_index=False)['retweets'].mean()
user_retweet_dict = dict(zip(mean_df['user'].tolist(), mean_df['retweets'].tolist()))

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

df['average'] = df['user'].apply(a)
df['difference'] = df.apply(d, axis=1)

df.to_excel('final_datasets/tableau_input3.xlsx', index=False)