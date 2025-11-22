"""
Core financial analysis module with machine learning models
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class FinancialAnalyzer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.risk_model = None
        self.return_model = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize ML models for risk and return prediction"""
        # Create synthetic training data for demonstration
        np.random.seed(42)
        n_samples = 1000
        
        # Features: age, income, expenses, savings, risk_tolerance
        X = np.random.rand(n_samples, 5)
        X[:, 0] = np.random.randint(18, 70, n_samples)  # age
        X[:, 1] = np.random.uniform(30000, 200000, n_samples)  # income
        X[:, 2] = np.random.uniform(20000, 150000, n_samples)  # expenses
        X[:, 3] = np.random.uniform(5000, 100000, n_samples)  # savings
        X[:, 4] = np.random.uniform(0, 1, n_samples)  # risk_tolerance
        
        # Generate correlated target variables
        # Normalize features for calculation
        norm_age = (X[:, 0] - 18) / (70 - 18)
        norm_income = (X[:, 1] - 30000) / (200000 - 30000)
        norm_savings = (X[:, 3] - 5000) / (100000 - 5000)
        risk_tol = X[:, 4]
        
        # Calculate base risk score with weights
        # 50% risk tolerance, 30% age factor (younger = higher), 20% financial cushion
        base_risk = (risk_tol * 0.5) + ((1 - norm_age) * 0.3) + ((norm_income + norm_savings)/2 * 0.2)
        
        # Add some random noise and clip to 0-1
        y_risk = np.clip(base_risk + np.random.normal(0, 0.05, n_samples), 0, 1)
        
        # Expected return depends heavily on risk score (Risk-Return Tradeoff)
        # Base risk-free rate ~3%, max return ~15%
        y_return = 0.03 + (y_risk * 0.12) + np.random.normal(0, 0.01, n_samples)
        
        # Train models
        self.risk_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.return_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        self.risk_model.fit(X, y_risk)
        self.return_model.fit(X, y_return)
    
    def analyze_user_profile(self, user_data):
        """
        Analyze user financial profile and return risk assessment
        """
        # Extract features
        features = np.array([[
            user_data['age'],
            user_data['income'],
            user_data['expenses'],
            user_data['savings'],
            user_data['risk_tolerance']
        ]])
        
        # Predict risk and return
        risk_score = self.risk_model.predict(features)[0]
        expected_return = self.return_model.predict(features)[0]
        
        # Determine risk category
        if risk_score < 0.33:
            risk_category = "low"
        elif risk_score < 0.66:
            risk_category = "medium"
        else:
            risk_category = "high"
        
        return {
            'risk_score': risk_score,
            'risk_category': risk_category,
            'expected_return': expected_return,
            'features': features[0]
        }
    
    def calculate_investment_allocation(self, user_data, analysis_result):
        """
        Calculate optimal investment allocation based on user profile
        """
        risk_category = analysis_result['risk_category']
        age = user_data['age']
        income = user_data['income']
        savings = user_data['savings']
        
        # Base allocation based on risk category
        if risk_category == "low":
            allocation = {
                'fixed_deposits': 0.4,
                'government_bonds': 0.3,
                'money_market_funds': 0.2,
                'mutual_funds': 0.1,
                'stocks': 0.0,
                'crypto': 0.0
            }
        elif risk_category == "medium":
            allocation = {
                'fixed_deposits': 0.2,
                'government_bonds': 0.2,
                'money_market_funds': 0.1,
                'mutual_funds': 0.3,
                'etfs': 0.15,
                'stocks': 0.05,
                'crypto': 0.0
            }
        else:  # high risk
            allocation = {
                'fixed_deposits': 0.1,
                'government_bonds': 0.1,
                'money_market_funds': 0.05,
                'mutual_funds': 0.25,
                'etfs': 0.2,
                'stocks': 0.25,
                'crypto': 0.05
            }
        
        # Adjust based on age
        if age < 35:
            # Younger investors can take more risk
            allocation['stocks'] = min(allocation['stocks'] + 0.1, 0.4)
            allocation['crypto'] = min(allocation['crypto'] + 0.05, 0.15)
        elif age > 60:
            # Older investors should be more conservative
            allocation['fixed_deposits'] = min(allocation['fixed_deposits'] + 0.2, 0.6)
            allocation['government_bonds'] = min(allocation['government_bonds'] + 0.1, 0.4)
            allocation['stocks'] = max(allocation['stocks'] - 0.1, 0.0)
        
        # Normalize allocation to ensure it sums to 1
        total = sum(allocation.values())
        allocation = {k: v/total for k, v in allocation.items()}
        
        return allocation
    
    def get_market_data(self, symbols, period="1mo"):
        """
        Fetch real-time market data for given symbols
        """
        market_data = {}
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=period)
                
                if not hist.empty and len(hist) > 0:
                    current_price = hist['Close'].iloc[-1]
                    change = hist['Close'].pct_change().iloc[-1] * 100 if len(hist) > 1 else 0
                    
                    market_data[symbol] = {
                        'current_price': round(float(current_price), 2),
                        'change_percent': round(float(change), 2),
                        'volume': int(hist['Volume'].iloc[-1]) if not pd.isna(hist['Volume'].iloc[-1]) else 0,
                        'high_52w': round(float(hist['Close'].max()), 2),
                        'low_52w': round(float(hist['Close'].min()), 2)
                    }
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                market_data[symbol] = {
                    'current_price': 0,
                    'change_percent': 0,
                    'volume': 0,
                    'high_52w': 0,
                    'low_52w': 0
                }
        
        return market_data
    
    def generate_advice_report(self, user_data, analysis_result, allocation, market_data):
        """
        Generate personalized financial advice report
        """
        risk_category = analysis_result['risk_category']
        expected_return = analysis_result['expected_return']
        
        # Calculate investment amounts
        investable_amount = user_data['savings'] * 0.8  # Use 80% of savings for investment
        
        advice = {
            'summary': f"Based on your profile, you have a {risk_category} risk tolerance with an expected annual return of {expected_return:.1%}.",
            'recommendations': [],
            'investment_breakdown': {},
            'market_insights': market_data
        }
        
        # Generate specific recommendations
        if risk_category == "low":
            advice['recommendations'].append("Focus on capital preservation with fixed deposits and government bonds.")
            advice['recommendations'].append("Consider a small allocation to mutual funds for growth.")
        elif risk_category == "medium":
            advice['recommendations'].append("Balance between growth and stability with mutual funds and ETFs.")
            advice['recommendations'].append("Include some individual stocks for potential higher returns.")
        else:
            advice['recommendations'].append("Embrace growth opportunities with higher stock allocation.")
            advice['recommendations'].append("Consider crypto for diversification, but limit exposure.")
        
        # Calculate investment amounts
        for category, percentage in allocation.items():
            if percentage > 0:
                amount = investable_amount * percentage
                advice['investment_breakdown'][category] = {
                    'percentage': percentage * 100,
                    'amount': amount,
                    'description': self._get_category_description(category)
                }
        
        return advice
    
    def _get_category_description(self, category):
        """Get description for investment category"""
        descriptions = {
            'fixed_deposits': 'Low-risk, guaranteed returns from banks',
            'government_bonds': 'Very safe, backed by government',
            'money_market_funds': 'Short-term, low-risk investments',
            'mutual_funds': 'Diversified portfolio managed by professionals',
            'etfs': 'Exchange-traded funds tracking market indices',
            'stocks': 'Individual company shares with higher volatility',
            'crypto': 'Cryptocurrency investments with high volatility'
        }
        return descriptions.get(category, 'Investment category')
