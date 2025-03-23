import pandas as pd
import numpy as np
from config import Config
from services.market_data import MarketDataService

class InvestmentRecommendationService:
    def __init__(self):
        self.config = Config()
        self.market_data_service = MarketDataService()

    def generate_portfolio_recommendation(self, user):
        """Generate personalized portfolio recommendation based on user profile"""
        # Get base allocation based on risk tolerance
        base_allocation = self.config.PORTFOLIO_ALLOCATION.get(
            user.risk_tolerance,
            self.config.PORTFOLIO_ALLOCATION['Moderate']
        )

        # Adjust allocation based on investment horizon
        horizon_multiplier = self._get_horizon_multiplier(user.investment_horizon)
        adjusted_allocation = {
            k: v * horizon_multiplier for k, v in base_allocation.items()
        }

        # Get specific investment recommendations
        recommendations = self.market_data_service.get_stock_recommendations(
            user.risk_tolerance,
            user.investment_horizon
        )

        # Calculate investment amounts based on monthly income
        monthly_investment = self._calculate_monthly_investment(user)
        
        # Generate detailed portfolio recommendation
        portfolio = {
            'allocation': adjusted_allocation,
            'recommendations': recommendations,
            'monthly_investment': monthly_investment,
            'risk_metrics': self._calculate_risk_metrics(user),
            'investment_strategy': self._generate_investment_strategy(user)
        }

        return portfolio

    def _get_horizon_multiplier(self, investment_horizon):
        """Calculate allocation multiplier based on investment horizon"""
        multipliers = {
            'Short Term': 0.8,
            'Medium Term': 1.0,
            'Long Term': 1.2
        }
        return multipliers.get(investment_horizon, 1.0)

    def _calculate_monthly_investment(self, user):
        """Calculate recommended monthly investment amount"""
        # Basic rule: 20% of monthly income for investment
        base_investment = user.monthly_income * 0.20
        
        # Adjust based on expenses and emergency fund
        if user.monthly_expenses > user.monthly_income * 0.7:
            base_investment *= 0.8  # Reduce investment if expenses are high
        
        # Ensure minimum investment amount
        return max(base_investment, 5000)

    def _calculate_risk_metrics(self, user):
        """Calculate risk metrics for the portfolio"""
        return {
            'risk_score': self._calculate_risk_score(user),
            'volatility': self._estimate_volatility(user.risk_tolerance),
            'max_drawdown': self._estimate_max_drawdown(user.risk_tolerance)
        }

    def _calculate_risk_score(self, user):
        """Calculate overall risk score based on user profile"""
        risk_factors = {
            'age': 1 if user.age < 30 else (0.8 if user.age < 50 else 0.6),
            'income': 1 if user.monthly_income > 50000 else 0.8,
            'dependents': 0.9 if user.dependents > 0 else 1,
            'emergency_fund': 1 if user.emergency_fund_amount > user.monthly_expenses * 3 else 0.8
        }
        
        return sum(risk_factors.values()) / len(risk_factors)

    def _estimate_volatility(self, risk_tolerance):
        """Estimate portfolio volatility based on risk tolerance"""
        volatility_map = {
            'Conservative': 0.08,
            'Moderate': 0.12,
            'Aggressive': 0.18
        }
        return volatility_map.get(risk_tolerance, 0.12)

    def _estimate_max_drawdown(self, risk_tolerance):
        """Estimate maximum drawdown based on risk tolerance"""
        drawdown_map = {
            'Conservative': 0.15,
            'Moderate': 0.25,
            'Aggressive': 0.35
        }
        return drawdown_map.get(risk_tolerance, 0.25)

    def _generate_investment_strategy(self, user):
        """Generate investment strategy based on user profile"""
        strategy = {
            'approach': self._determine_investment_approach(user),
            'rebalancing_frequency': self._determine_rebalancing_frequency(user),
            'tax_optimization': self._generate_tax_strategy(user),
            'risk_management': self._generate_risk_management_strategy(user)
        }
        return strategy

    def _determine_investment_approach(self, user):
        """Determine investment approach based on user profile"""
        if user.investment_knowledge == 'Basic':
            return 'Systematic Investment Plan (SIP)'
        elif user.investment_knowledge == 'Intermediate':
            return 'Combination of SIP and Direct Stock Investment'
        else:
            return 'Active Portfolio Management'

    def _determine_rebalancing_frequency(self, user):
        """Determine portfolio rebalancing frequency"""
        if user.risk_tolerance == 'Conservative':
            return 'Quarterly'
        elif user.risk_tolerance == 'Moderate':
            return 'Bi-annual'
        else:
            return 'Annual'

    def _generate_tax_strategy(self, user):
        """Generate tax optimization strategy"""
        return {
            'tax_saving_investments': user.tax_saving_investments,
            'recommended_schemes': ['ELSS', 'PPF', 'NPS'],
            'holding_period': 'Long-term for tax benefits'
        }

    def _generate_risk_management_strategy(self, user):
        """Generate risk management strategy"""
        return {
            'stop_loss': '5% for individual stocks',
            'portfolio_stop_loss': '15% overall',
            'diversification': 'Across sectors and market caps',
            'hedging': 'Consider index options for hedging'
        } 