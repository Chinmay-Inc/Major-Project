"""
Demo script to showcase AI Investment Advisor features
"""
import pandas as pd
import numpy as np
from financial_analyzer import FinancialAnalyzer
from visualizations import InvestmentVisualizer
import matplotlib.pyplot as plt

def run_demo():
    """Run a demonstration of the AI Investment Advisor"""
    print("🚀 AI Investment Advisor - Demo Mode")
    print("=" * 50)
    
    # Initialize components
    analyzer = FinancialAnalyzer()
    visualizer = InvestmentVisualizer()
    
    # Demo user data
    demo_users = [
        {
            'name': 'Young Professional',
            'data': {
                'age': 28,
                'income': 75000,
                'expenses': 45000,
                'savings': 25000,
                'risk_tolerance': 0.7
            }
        },
        {
            'name': 'Mid-Career Conservative',
            'data': {
                'age': 45,
                'income': 120000,
                'expenses': 80000,
                'savings': 150000,
                'risk_tolerance': 0.3
            }
        },
        {
            'name': 'Near Retirement',
            'data': {
                'age': 62,
                'income': 100000,
                'expenses': 70000,
                'savings': 500000,
                'risk_tolerance': 0.2
            }
        }
    ]
    
    print("📊 Analyzing different user profiles...\n")
    
    for user in demo_users:
        print(f"👤 {user['name']}")
        print("-" * 30)
        
        # Analyze user profile
        analysis = analyzer.analyze_user_profile(user['data'])
        allocation = analyzer.calculate_investment_allocation(user['data'], analysis)
        advice = analyzer.generate_advice_report(user['data'], analysis, allocation, {})
        
        # Display results
        print(f"Age: {user['data']['age']}")
        print(f"Income: ${user['data']['income']:,}")
        print(f"Savings: ${user['data']['savings']:,}")
        print(f"Risk Category: {analysis['risk_category'].title()}")
        print(f"Risk Score: {analysis['risk_score']:.2f}")
        print(f"Expected Return: {analysis['expected_return']:.1%}")
        
        print("\n📈 Investment Allocation:")
        for category, data in allocation.items():
            if data['percentage'] > 0:
                print(f"  {category.replace('_', ' ').title()}: {data['percentage']:.1f}% (${data['amount']:,.0f})")
        
        print(f"\n💡 Key Recommendation: {advice['recommendations'][0] if advice['recommendations'] else 'N/A'}")
        print("\n" + "="*50 + "\n")
    
    # Market data demo
    print("📈 Fetching market data...")
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
    
    try:
        market_data = analyzer.get_market_data(symbols)
        if market_data:
            print("✅ Market data retrieved successfully!")
            print("\nCurrent Market Prices:")
            for symbol, data in market_data.items():
                print(f"  {symbol}: ${data['current_price']:.2f} ({data['change_percent']:+.2f}%)")
        else:
            print("❌ Unable to fetch market data")
    except Exception as e:
        print(f"❌ Error fetching market data: {e}")
    
    print("\n🎯 Demo completed!")
    print("To run the full application, use: streamlit run app.py")

if __name__ == "__main__":
    run_demo()
