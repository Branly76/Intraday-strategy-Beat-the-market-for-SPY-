
from utils.download_data import fetch_alpaca_data, fetch_alpaca_dividends
import pandas as pd

symbol = 'SPY'
start_date     = '2021-01-01'
end_date       = '2024-12-31'   
spy_intra_data = fetch_alpaca_data(symbol, '1Min', start_date, end_date)
spy_daily_data = fetch_alpaca_data(symbol, '1D', start_date, end_date)
dividends      = fetch_alpaca_dividends(symbol,start_date,end_date)

df = pd.DataFrame(spy_intra_data)
df.to_csv('./data/spy_intra_data.csv', index=False)

df = pd.DataFrame(spy_daily_data)
df.to_csv('./data/spy_daily_data.csv', index=False)

df = pd.DataFrame(dividends)
df.to_csv('./data/dividends.csv', index=False)



