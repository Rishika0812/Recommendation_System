from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from models.user import User
from services.investment_recommendation import InvestmentRecommendationService
from services.market_data import MarketDataService
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

investment_service = InvestmentRecommendationService()
market_service = MarketDataService()

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f"Login attempt for username: {username}")  # Debug print
        
        user = User.get_user_by_username(username)
        if user:
            print(f"User found: {user.username}")  # Debug print
            print(f"Stored password hash: {user.password_hash}")  # Debug print
            print(f"Attempting to verify password")  # Debug print
            try:
                if User.verify_password(password, user.password_hash):
                    print("Password verified successfully")  # Debug print
                    session['username'] = username
                    return redirect(url_for('dashboard'))
                else:
                    print("Password verification failed")  # Debug print
            except Exception as e:
                print(f"Error during password verification: {e}")  # Debug print
        else:
            print("User not found")  # Debug print
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            # Get form data with default values
            password = request.form.get('password')
            if not password:
                return render_template('signup.html', error='Password is required')

            user_data = {
                'username': request.form.get('username'),
                'password_hash': User.hash_password(password),
                'email': request.form.get('email'),
                'name': request.form.get('name'),
                'age': int(request.form.get('age', 0)),
                'occupation': request.form.get('occupation', ''),
                'marital_status': request.form.get('marital_status', ''),
                'dependents': int(request.form.get('dependents', 0)),
                'monthly_income': float(request.form.get('monthly_income', 0)),
                'monthly_expenses': float(request.form.get('monthly_expenses', 0)),
                'risk_tolerance': request.form.get('risk_tolerance', 'Moderate'),
                'investment_horizon': request.form.get('investment_horizon', 'Medium Term'),
                'investment_knowledge': request.form.get('investment_knowledge', 'Basic'),
                'existing_savings': float(request.form.get('existing_savings', 0)),
                'existing_investments': request.form.get('existing_investments', ''),
                'emergency_fund_amount': float(request.form.get('emergency_fund_amount', 0)),
                'loan_details': request.form.get('loan_details', ''),
                'monthly_emi': float(request.form.get('monthly_emi', 0)),
                'credit_score': int(request.form.get('credit_score', 0)),
                'investment_goals': request.form.get('investment_goals', ''),
                'target_amounts': json.loads(request.form.get('target_amounts', '{}')),
                'investment_timeframes': json.loads(request.form.get('investment_timeframes', '{}')),
                'tax_bracket': request.form.get('tax_bracket', ''),
                'tax_saving_investments': request.form.get('tax_saving_investments', ''),
                'insurance_coverage': request.form.get('insurance_coverage', ''),
                'preferred_investment_types': request.form.get('preferred_investment_types', ''),
                'investment_frequency': request.form.get('investment_frequency', 'Monthly'),
                'market_experience': request.form.get('market_experience', ''),
                'risk_capacity': request.form.get('risk_capacity', ''),
                'loss_tolerance': request.form.get('loss_tolerance', ''),
                'market_crash_reaction': request.form.get('market_crash_reaction', ''),
                'preferred_sectors': request.form.get('preferred_sectors', ''),
                'esg_preference': request.form.get('esg_preference') == 'True',
                'dividend_preference': request.form.get('dividend_preference') == 'True',
                'portfolio_preference': request.form.get('portfolio_preference', ''),
                'risk_preference': float(request.form.get('risk_preference', 5.0))
            }
            
            # Validate required fields
            required_fields = ['username', 'email', 'name', 'age', 'monthly_income']
            for field in required_fields:
                if not user_data.get(field):
                    return render_template('signup.html', error=f'{field} is required')
            
            user = User(**user_data)
            if user.save():
                session['username'] = user.username
                return redirect(url_for('dashboard'))
            
            return render_template('signup.html', error='Registration failed')
            
        except Exception as e:
            print(f"Error during signup: {e}")
            return render_template('signup.html', error='An error occurred during registration')
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = User.get_user_by_username(session['username'])
    portfolio = investment_service.generate_portfolio_recommendation(user)
    market_data = market_service.get_market_indices()
    
    return render_template('dashboard.html', 
                         user=user,
                         portfolio=portfolio,
                         market_data=market_data)

@app.route('/api/market-data')
def get_market_data():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    market_data = market_service.get_market_indices()
    sector_performance = market_service.get_sector_performance()
    market_heatmap = market_service.get_market_heatmap()
    
    return jsonify({
        'market_data': market_data,
        'sector_performance': sector_performance,
        'market_heatmap': market_heatmap
    })

@app.route('/api/portfolio-recommendation')
def get_portfolio_recommendation():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.get_user_by_username(session['username'])
    portfolio = investment_service.generate_portfolio_recommendation(user)
    
    return jsonify(portfolio)

@app.route('/api/stock-analysis/<symbol>')
def get_stock_analysis(symbol):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    stock_data = market_service.get_stock_data(symbol)
    technical_indicators = market_service.calculate_technical_indicators(stock_data)
    
    return jsonify({
        'stock_data': stock_data.to_dict() if stock_data is not None else None,
        'technical_indicators': technical_indicators.to_dict() if technical_indicators is not None else None
    })

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) 