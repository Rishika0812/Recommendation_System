import yfinance as yf
import pandas as pd
import numpy as np
from config import Config
import requests
from datetime import datetime, timedelta

class MarketDataService:
    def __init__(self):
        self.config = Config()

    def get_market_indices(self):
        """Fetch current market indices data"""
        indices_data = {}
        for name, symbol in self.config.MARKET_INDICES.items():
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                indices_data[name] = {
                    'current_price': info.get('regularMarketPrice', 0),
                    'change': info.get('regularMarketChange', 0),
                    'change_percent': info.get('regularMarketChangePercent', 0),
                    'volume': info.get('regularMarketVolume', 0)
                }
            except Exception as e:
                print(f"Error fetching {name}: {e}")
        return indices_data

    def get_stock_data(self, symbol, period='1y'):
        """Fetch historical stock data"""
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            return df
        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {e}")
            return None

    def calculate_technical_indicators(self, df):
        """Calculate technical indicators for a given stock"""
        if df is None or df.empty:
            return None

        # Calculate 20-day and 50-day moving averages
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()

        # Calculate RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        return df

    def get_sector_performance(self):
        """Fetch sector-wise performance data"""
        try:
            headers = {
                'X-RapidAPI-Key': self.config.RAPID_API_KEY,
                'X-RapidAPI-Host': 'real-time-finance-data.p.rapidapi.com'
            }
            response = requests.get(
                f"{self.config.RAPID_API_BASE_URL}/stock-sectors",
                headers=headers
            )
            return response.json()
        except Exception as e:
            print(f"Error fetching sector performance: {e}")
            return None

    def get_market_heatmap(self):
        """Generate market heatmap data"""
        try:
            # Fetch top stocks from different sectors
            sectors = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Consumer']
            heatmap_data = {}
            
            for sector in sectors:
                headers = {
                    'X-RapidAPI-Key': self.config.RAPID_API_KEY,
                    'X-RapidAPI-Host': 'real-time-finance-data.p.rapidapi.com'
                }
                response = requests.get(
                    f"{self.config.RAPID_API_BASE_URL}/stock-sectors/{sector}",
                    headers=headers
                )
                heatmap_data[sector] = response.json()
            
            return heatmap_data
        except Exception as e:
            print(f"Error generating market heatmap: {e}")
            return None

    def get_stock_recommendations(self, risk_tolerance, investment_horizon):
        """Generate stock recommendations based on risk tolerance and investment horizon"""
        recommendations = {
            'Conservative': {
                'Large Cap': ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS'],
                'Government Bonds': ['GSEC10.NS'],
                'Fixed Deposits': ['SBIN.NS'],
                'Liquid Funds': ['HDFCLIQUID.NS']
            },
            'Moderate': {
                'Large Cap': ['INFY.NS', 'ICICIBANK.NS', 'HDFC.NS'],
                'Mid Cap': ['TATAMOTORS.NS', 'ADANIENT.NS', 'BAJFINANCE.NS'],
                'Corporate Bonds': ['ICICIGI.NS'],
                'Liquid Funds': ['HDFCLIQUID.NS']
            },
            'Aggressive': {
                'Large Cap': ['WIPRO.NS', 'AXISBANK.NS', 'KOTAKBANK.NS'],
                'Mid Cap': ['ZOMATO.NS', 'PAYTM.NS', 'POLICYBZR.NS'],
                'Small Cap': ['IRFC.NS', 'RVNL.NS', 'IRCON.NS'],
                'Liquid Funds': ['HDFCLIQUID.NS']
            }
        }
        
        return recommendations.get(risk_tolerance, recommendations['Moderate']) 