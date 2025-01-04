import requests
import pandas as pd
from   datetime import datetime, timedelta,time
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from   matplotlib.ticker import FuncFormatter
import statsmodels.api as sm
import pytz


API_KEY_ID     = "KEY"
API_SECRET_KEY = "SECRET"
#rMSa7gZ510pIaKtkFoabdDxT3WmfSVW9gZ


def fetch_alpaca_data(symbol, timeframe, start_date, end_date) -> pd.DataFrame:
    
    """
    Fetch stock bars data from Alpaca Markets based on the given timeframe.
    """
    
    url = 'https://data.alpaca.markets/v2/stocks/bars'
    headers = {
        'APCA-API-KEY-ID': API_KEY_ID,
        'APCA-API-SECRET-KEY': API_SECRET_KEY
    }
    
    params = {
        'symbols': symbol,
        'timeframe': timeframe,
        'start': datetime.strptime(start_date, "%Y-%m-%d").isoformat() + 'Z',
        'end': datetime.strptime(end_date, "%Y-%m-%d").isoformat() + 'Z',
        'limit': 10000,
        'adjustment': 'raw',
        'feed': 'sip'
    }

    data_list = []
    eastern = pytz.timezone('America/New_York')  
    utc = pytz.utc  

    market_open  = time(9, 30)  # Market opens at 9:30 AM
    market_close = time(15, 59)  # Market closes just before 4:00 PM

    print("Starting data fetch...")
    while True:
        print(f"Fetching data for symbols: {symbol} from {start_date} to {end_date}")
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching data with status code {response.status_code}: {response.text}")
            break

        data = response.json()

        bars = data.get('bars')

        for symbol, entries in bars.items():
            print(f"Processing {len(entries)} entries for symbol: {symbol}")
            for entry in entries:
                try:
                    utc_time = datetime.fromisoformat(entry['t'].rstrip('Z')).replace(tzinfo=utc)
                    eastern_time = utc_time.astimezone(eastern)

                    # Apply market hours filter for '1Min' timeframe
                    if timeframe == '1Min' and not (market_open <= eastern_time.time() <= market_close):
                        continue  # Skip entries outside market hours

                    data_entry = {
                        'volume': entry['v'],
                        'open': entry['o'],
                        'high': entry['h'],
                        'low': entry['l'],
                        'close': entry['c'],
                        'caldt': eastern_time  
                    }
                    data_list.append(data_entry)
                    print(f"Appended data for {symbol} at {eastern_time}")
                except Exception as e:
                    print(f"Error processing entry: {entry}, {e}")
                    continue

        if 'next_page_token' in data and data['next_page_token']:
            params['page_token'] = data['next_page_token']
            print("Fetching next page...")
        else:
            print("No more pages to fetch.")
            break

    df = pd.DataFrame(data_list)
    print("Data fetching complete.")
    return df

def fetch_alpaca_dividends(symbol, start_date, end_date)-> pd.DataFrame:
    
    """
    Fetch dividend announcements from Alpaca for a specified symbol between two dates.
    This function splits the request into manageable 90-day segments to comply with API constraints.
    """

    url_base = "https://paper-api.alpaca.markets/v2/corporate_actions/announcements"
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": API_KEY_ID,
        "APCA-API-SECRET-KEY": API_SECRET_KEY
    }

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    dividends_list = []
    current_start = start_date

    while current_start < end_date:
 

        current_end = min(current_start + timedelta(days=89), end_date)
                
        url = f"{url_base}?ca_types=Dividend&since={current_start}&until={current_end}&symbol={symbol}"
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                dividends_list.append({
                    'caldt': datetime.strptime(entry['ex_date'], '%Y-%m-%d'),
                    'dividend': float(entry['cash'])
                })
        else:
            print(f"Failed to fetch data for period {current_start} to {current_end}: {response.text}")
        
        current_start = current_end + timedelta(days=1)

    return pd.DataFrame(dividends_list)
