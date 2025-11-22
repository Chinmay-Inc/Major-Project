"""
Simple test script to verify the application components
"""
import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import sklearn
        print("✅ Scikit-learn imported successfully")
    except ImportError as e:
        print(f"❌ Scikit-learn import failed: {e}")
        return False
    
    try:
        import tensorflow as tf
        print("✅ TensorFlow imported successfully")
    except ImportError as e:
        print(f"❌ TensorFlow import failed: {e}")
        return False
    
    try:
        import yfinance as yf
        print("✅ yfinance imported successfully")
    except ImportError as e:
        print(f"❌ yfinance import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ Matplotlib imported successfully")
    except ImportError as e:
        print(f"❌ Matplotlib import failed: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        import seaborn as sns
        print("✅ Seaborn imported successfully")
    except ImportError as e:
        print(f"❌ Seaborn import failed: {e}")
        return False
    
    try:
        from reportlab.lib.pagesizes import letter
        print("✅ ReportLab imported successfully")
    except ImportError as e:
        print(f"❌ ReportLab import failed: {e}")
        return False
    
    return True

def test_custom_modules():
    """Test if custom modules can be imported"""
    print("\n🔍 Testing custom modules...")
    
    try:
        from financial_analyzer import FinancialAnalyzer
        print("✅ FinancialAnalyzer imported successfully")
    except ImportError as e:
        print(f"❌ FinancialAnalyzer import failed: {e}")
        return False
    
    try:
        from visualizations import InvestmentVisualizer
        print("✅ InvestmentVisualizer imported successfully")
    except ImportError as e:
        print(f"❌ InvestmentVisualizer import failed: {e}")
        return False
    
    try:
        from auth_manager import AuthManager
        print("✅ AuthManager imported successfully")
    except ImportError as e:
        print(f"❌ AuthManager import failed: {e}")
        return False
    
    try:
        from pdf_generator import PDFGenerator
        print("✅ PDFGenerator imported successfully")
    except ImportError as e:
        print(f"❌ PDFGenerator import failed: {e}")
        return False
    
    return True

def test_functionality():
    """Test basic functionality of the modules"""
    print("\n🔍 Testing functionality...")
    
    try:
        from financial_analyzer import FinancialAnalyzer
        analyzer = FinancialAnalyzer()
        print("✅ FinancialAnalyzer initialized successfully")
        
        # Test with sample data
        sample_data = {
            'age': 30,
            'income': 50000,
            'expenses': 30000,
            'savings': 10000,
            'risk_tolerance': 0.5
        }
        
        analysis = analyzer.analyze_user_profile(sample_data)
        print("✅ User profile analysis completed")
        
        allocation = analyzer.calculate_investment_allocation(sample_data, analysis)
        print("✅ Investment allocation calculated")
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        traceback.print_exc()
        return False
    
    try:
        from visualizations import InvestmentVisualizer
        visualizer = InvestmentVisualizer()
        print("✅ InvestmentVisualizer initialized successfully")
        
        # Test pie chart creation
        test_allocation = {
            'stocks': {'percentage': 40, 'amount': 4000, 'description': 'Individual stocks'},
            'bonds': {'percentage': 30, 'amount': 3000, 'description': 'Government bonds'},
            'cash': {'percentage': 30, 'amount': 3000, 'description': 'Cash and equivalents'}
        }
        
        fig = visualizer.create_pie_chart(test_allocation)
        print("✅ Pie chart created successfully")
        
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        traceback.print_exc()
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 AI Investment Advisor - Test Suite")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install missing packages.")
        return False
    
    # Test custom modules
    if not test_custom_modules():
        print("\n❌ Custom module tests failed. Please check file structure.")
        return False
    
    # Test functionality
    if not test_functionality():
        print("\n❌ Functionality tests failed. Please check implementation.")
        return False
    
    print("\n🎉 All tests passed! The application is ready to run.")
    print("To start the application, run: streamlit run app.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
