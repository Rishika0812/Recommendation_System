import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
    RAPID_API_KEY = os.getenv('RAPID_API_KEY')
    
    # Database configuration
    USERS_CSV = 'users.csv'
    
    # API endpoints
    ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co/query'
    RAPID_API_BASE_URL = 'https://real-time-finance-data.p.rapidapi.com'
    
    # Market data symbols
    MARKET_INDICES = {
        'NIFTY50': '^NSEI',
        'SENSEX': '^BSESN',
        'NIFTYBANK': '^NSEBANK',
        'NIFTYIT': 'NIFTYIT.NS'
    }
    
    # Risk-based portfolio allocation
    PORTFOLIO_ALLOCATION = {
        'Conservative': {
            'Large Cap': 0.30,
            'Government Bonds': 0.40,
            'Fixed Deposits': 0.20,
            'Liquid Funds': 0.10
        },
        'Moderate': {
            'Large Cap': 0.40,
            'Mid Cap': 0.20,
            'Corporate Bonds': 0.25,
            'Liquid Funds': 0.15
        },
        'Aggressive': {
            'Large Cap': 0.35,
            'Mid Cap': 0.30,
            'Small Cap': 0.25,
            'Liquid Funds': 0.10
        }
    } 