import csv
import bcrypt
from datetime import datetime
import json

class User:
    def __init__(self, username, password_hash, email, name, age, occupation, 
                 marital_status, dependents, monthly_income, monthly_expenses,
                 risk_tolerance, investment_horizon, investment_knowledge,
                 existing_savings, existing_investments, emergency_fund_amount,
                 loan_details, monthly_emi, credit_score, investment_goals,
                 target_amounts, investment_timeframes, tax_bracket,
                 tax_saving_investments, insurance_coverage,
                 preferred_investment_types, investment_frequency,
                 market_experience, risk_capacity, loss_tolerance,
                 market_crash_reaction, preferred_sectors, esg_preference,
                 dividend_preference, portfolio_preference, risk_preference,
                 created_at=None):
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.name = name
        self.age = age
        self.occupation = occupation
        self.marital_status = marital_status
        self.dependents = dependents
        self.monthly_income = monthly_income
        self.monthly_expenses = monthly_expenses
        self.risk_tolerance = risk_tolerance
        self.investment_horizon = investment_horizon
        self.investment_knowledge = investment_knowledge
        self.existing_savings = existing_savings
        self.existing_investments = existing_investments
        self.emergency_fund_amount = emergency_fund_amount
        self.loan_details = loan_details
        self.monthly_emi = monthly_emi
        self.credit_score = credit_score
        self.investment_goals = investment_goals
        self.target_amounts = target_amounts
        self.investment_timeframes = investment_timeframes
        self.tax_bracket = tax_bracket
        self.tax_saving_investments = tax_saving_investments
        self.insurance_coverage = insurance_coverage
        self.preferred_investment_types = preferred_investment_types
        self.investment_frequency = investment_frequency
        self.market_experience = market_experience
        self.risk_capacity = risk_capacity
        self.loss_tolerance = loss_tolerance
        self.market_crash_reaction = market_crash_reaction
        self.preferred_sectors = preferred_sectors
        self.esg_preference = esg_preference
        self.dividend_preference = dividend_preference
        self.portfolio_preference = portfolio_preference
        self.risk_preference = risk_preference
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def hash_password(password):
        try:
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        except Exception as e:
            print(f"Error hashing password: {e}")
            return None

    @staticmethod
    def verify_password(password, password_hash):
        try:
            if not password or not password_hash:
                print("Password or hash is empty")
                return False
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False

    @staticmethod
    def get_user_by_username(username):
        try:
            with open('users.csv', 'r', newline='') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if row[0] == username:
                        return User(
                            username=row[0],
                            password_hash=row[1],
                            email=row[2],
                            created_at=row[3],
                            name=row[4],
                            age=int(row[5]),
                            occupation=row[6],
                            marital_status=row[7],
                            dependents=int(row[8]),
                            monthly_income=float(row[9]),
                            monthly_expenses=float(row[10]),
                            risk_tolerance=row[11],
                            investment_horizon=row[12],
                            investment_knowledge=row[13],
                            existing_savings=float(row[14] or 0),
                            existing_investments=row[15],
                            emergency_fund_amount=float(row[16]),
                            loan_details=row[17],
                            monthly_emi=float(row[18]),
                            credit_score=int(row[19]),
                            investment_goals=row[20],
                            target_amounts=json.loads(row[21]),
                            investment_timeframes=json.loads(row[22]),
                            tax_bracket=row[23],
                            tax_saving_investments=row[24],
                            insurance_coverage=row[25],
                            preferred_investment_types=row[26],
                            investment_frequency=row[27],
                            market_experience=row[28],
                            risk_capacity=row[29],
                            loss_tolerance=row[30],
                            market_crash_reaction=row[31],
                            preferred_sectors=row[32],
                            esg_preference=row[33] == 'True',
                            dividend_preference=row[34] == 'True',
                            portfolio_preference=row[35],
                            risk_preference=float(row[36] or 0)
                        )
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
        return None

    def save(self):
        try:
            with open('users.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    self.username, self.password_hash, self.email, self.created_at,
                    self.name, self.age, self.occupation, self.marital_status,
                    self.dependents, self.monthly_income, self.monthly_expenses,
                    self.risk_tolerance, self.investment_horizon, self.investment_knowledge,
                    self.existing_savings, self.existing_investments, self.emergency_fund_amount,
                    self.loan_details, self.monthly_emi, self.credit_score,
                    self.investment_goals, json.dumps(self.target_amounts),
                    json.dumps(self.investment_timeframes), self.tax_bracket,
                    self.tax_saving_investments, self.insurance_coverage,
                    self.preferred_investment_types, self.investment_frequency,
                    self.market_experience, self.risk_capacity, self.loss_tolerance,
                    self.market_crash_reaction, self.preferred_sectors,
                    self.esg_preference, self.dividend_preference,
                    self.portfolio_preference, self.risk_preference
                ])
            return True
        except Exception as e:
            print(f"Error saving user: {e}")
            return False

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')} 