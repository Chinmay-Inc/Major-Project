"""
Configuration file for the AI Investment Advisor
"""
import os

# Database configuration
DATABASE_PATH = "user_data.db"

# API Keys (add your own keys here)
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")

# Investment categories and their risk levels
INVESTMENT_CATEGORIES = {
    "low_risk": {
        "fixed_deposits": {"min_allocation": 0.1, "max_allocation": 0.4},
        "government_bonds": {"min_allocation": 0.1, "max_allocation": 0.3},
        "money_market_funds": {"min_allocation": 0.05, "max_allocation": 0.2}
    },
    "medium_risk": {
        "mutual_funds": {"min_allocation": 0.2, "max_allocation": 0.6},
        "etfs": {"min_allocation": 0.1, "max_allocation": 0.4},
        "corporate_bonds": {"min_allocation": 0.1, "max_allocation": 0.3}
    },
    "high_risk": {
        "stocks": {"min_allocation": 0.1, "max_allocation": 0.5},
        "crypto": {"min_allocation": 0.05, "max_allocation": 0.2},
        "commodities": {"min_allocation": 0.05, "max_allocation": 0.15}
    }
}

# Risk tolerance mapping
RISK_TOLERANCE_MAPPING = {
    "conservative": 0.2,
    "moderate": 0.5,
    "aggressive": 0.8
}

# Age-based investment adjustments
AGE_ADJUSTMENTS = {
    "young": {"age_range": (18, 35), "risk_multiplier": 1.2},
    "middle": {"age_range": (36, 50), "risk_multiplier": 1.0},
    "senior": {"age_range": (51, 65), "risk_multiplier": 0.8},
    "retired": {"age_range": (66, 100), "risk_multiplier": 0.6}
}
