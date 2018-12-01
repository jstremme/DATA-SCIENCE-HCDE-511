import pandas as pd
                      
                      
stock_data = pd.read_csv('/Users/Arjun_Singh/Documents/MS_DataScience/HCDE511/DATA-SCIENCE-HCDE-511/stock_archive/^GSPC.csv')
sentiment_data = pd.read_csv('/Users/Arjun_Singh/Documents/MS_DataScience/HCDE511/DATA-SCIENCE-HCDE-511/dashboard_archive/economy_from_FoxNews.csv')

sd = sentiment_data.drop_duplicates(subset=['day_timestamp','day_average_sentiment'])
sd = sd[['day_timestamp','day_average_sentiment']]

ad = stock_data[['Date','Close']]
ad = ad.rename(index=str, columns={"Date": "day_timestamp"})

res = pd.merge(ad, sd, on='day_timestamp',how='left')
res.to_csv('foxNewsTweetsVs SMP500.csv')

x = pd.to_datetime(res['day_timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
y1 = res['Close']
y2 = res['day_average_sentiment']


ax = res[['day_timestamp', 'Close']].plot(x='day_timestamp',)
ax.locator_params(axis='x', nbins=10)
#ax.xaxis.set_major_locator(plt.MaxNLocator(10))
res[['day_timestamp', 'day_average_sentiment']].plot(x='day_timestamp', kind='bar',ax=ax, secondary_y=True,color = 'tab:red')
ax.locator_params(axis='x', nbins=10)


