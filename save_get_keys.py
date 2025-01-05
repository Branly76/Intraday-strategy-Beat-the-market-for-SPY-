# Install python-dotenv first
# pip install python-dotenv

from dotenv import load_dotenv
import os

# Create .env file and load it
with open('.env', 'w') as f:
    f.write('ALPACA_API_KEY=api_key\n')
    f.write('ALPACA_API_SECRET=api_secret\n')


# Load the .env file
load_dotenv()

# Access the variables
api_key = os.getenv('ALPACA_API_KEY')
api_secret = os.getenv('ALPACA_API_SECRET')

print(os.getenv('ALPACA_API_KEY'))