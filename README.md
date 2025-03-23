# Investment Recommendation System

A comprehensive investment recommendation and tracking system that provides personalized investment advice, real-time market analysis, and secure investment execution.

## Features

### User Management
- Secure user registration and authentication
- Personalized user profiles with investment preferences
- Risk assessment and profile management

### Market Analysis
- Real-time market indices tracking (Nifty 50, Sensex, Nifty Bank, Nifty IT)
- Sector-wise performance analysis
- Market heatmap visualization
- Technical analysis indicators (Moving averages, RSI)

### Investment Recommendations
- Personalized portfolio allocation based on risk tolerance
- Investment strategy recommendations
- Tax optimization suggestions
- Risk management guidelines

### Portfolio Management
- Portfolio tracking and analysis
- Asset allocation visualization
- Performance monitoring
- Investment execution workflow

## Tech Stack

- **Backend**: Python/Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Data Visualization**: Chart.js
- **Market Data**: yfinance, Alpha Vantage API
- **Database**: CSV-based storage (users.csv)
- **Authentication**: bcrypt password hashing

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd investment-recommendation-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
RAPID_API_KEY=your_rapid_api_key
```

5. Run the application:
```bash
python app.py
```

6. Access the application:
Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
investment-recommendation-system/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── users.csv            # User data storage
├── .env                 # Environment variables
├── models/
│   └── user.py         # User model and authentication
├── services/
│   ├── market_data.py  # Market data service
│   └── investment_recommendation.py  # Investment recommendation service
└── templates/
    ├── base.html       # Base template
    ├── login.html      # Login page
    ├── signup.html     # Registration page
    └── dashboard.html  # Main dashboard
```

## API Endpoints

- `GET /`: Home page
- `GET /login`: Login page
- `POST /login`: User login
- `GET /signup`: Registration page
- `POST /signup`: User registration
- `GET /dashboard`: User dashboard
- `GET /api/market-data`: Real-time market data
- `GET /api/portfolio-recommendation`: Personalized portfolio recommendations
- `GET /api/stock-analysis/<symbol>`: Detailed stock analysis
- `GET /logout`: User logout

## Security Features

- Password hashing using bcrypt
- Secure session management
- API key protection
- Input validation and sanitization
- CSRF protection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Bootstrap 5 for UI components
- Chart.js for data visualization
- yfinance for market data
- Alpha Vantage for financial data API 