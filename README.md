# AI-Driven Personalized Investment & Financial Advisor

A comprehensive Python-based application that uses machine learning to provide personalized investment advice and financial planning recommendations.

## 🚀 Features

### Core Features
- **Personalized Financial Analysis**: Collects user input including income, expenses, savings, age, and financial goals
- **Machine Learning Models**: Uses scikit-learn and TensorFlow for risk assessment and return prediction
- **Real-time Market Data**: Fetches live stock/ETF/crypto prices using yfinance
- **Risk Analysis**: Categorizes users into low, medium, and high risk profiles
- **Investment Recommendations**: Provides specific allocation percentages for different investment categories

### Technology Stack
- **Backend**: Python with pandas, numpy, scikit-learn, tensorflow, yfinance
- **Frontend**: Streamlit for interactive web UI
- **Visualization**: Matplotlib, Plotly, Seaborn for charts and graphs
- **Authentication**: Built-in user management with SQLite
- **Export**: PDF report generation with ReportLab

### Dashboard Features
- **Interactive Forms**: User-friendly input forms for financial data
- **Real-time Charts**: Dynamic visualizations of investment allocations and market trends
- **Risk Assessment**: Visual risk-return analysis and age-based recommendations
- **Market Overview**: Live market data with price trends and volume information
- **Session Management**: Save and load previous analysis sessions
- **PDF Export**: Generate comprehensive investment reports

## 📁 Project Structure

```
AI-Investment-Advisor/
├── app.py                      # Main Streamlit application
├── financial_analyzer.py       # Core ML models and analysis
├── visualizations.py          # Chart and graph generation
├── auth_manager.py            # User authentication and sessions
├── pdf_generator.py           # PDF report generation
├── config.py                  # Configuration and constants
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── user_data.db              # SQLite database (created on first run)
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd AI-Investment-Advisor
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - Register a new account or use existing credentials

## 🎯 Usage Guide

### 1. Getting Started
- **Register/Login**: Create an account or login with existing credentials
- **Input Data**: Navigate to "Input Data" tab and fill in your financial information
- **Analysis**: Click "Analyze My Profile" to generate personalized recommendations

### 2. Dashboard Overview
- **Key Metrics**: View your risk score, expected return, and investable amount
- **Investment Allocation**: Interactive pie chart showing recommended portfolio
- **Market Data**: Real-time stock and crypto prices
- **Risk Analysis**: Visual representation of your risk-return profile

### 3. Detailed Analysis
- **Investment Breakdown**: Detailed table with specific investment categories
- **Recommendations**: Personalized advice based on your profile
- **Visualizations**: Age-risk analysis and income allocation charts
- **Goal Timeline**: Track progress towards your financial goals

### 4. Reports & Export
- **PDF Reports**: Generate comprehensive investment reports
- **Session Management**: Save and load previous analyses
- **Quick Summary**: Generate simplified reports for quick reference

## 🔧 Configuration

### API Keys
The application uses yfinance for market data, which doesn't require an API key. For enhanced features, you can add API keys in `config.py`:

```python
ALPHA_VANTAGE_API_KEY = "your_api_key_here"
```

### Investment Categories
Modify investment categories and risk levels in `config.py`:

```python
INVESTMENT_CATEGORIES = {
    "low_risk": {
        "fixed_deposits": {"min_allocation": 0.1, "max_allocation": 0.4},
        # ... other categories
    }
}
```

## 📊 Machine Learning Models

### Risk Assessment Model
- **Algorithm**: Random Forest Regressor
- **Features**: Age, income, expenses, savings, risk tolerance
- **Output**: Risk score (0-1) and risk category (low/medium/high)

### Return Prediction Model
- **Algorithm**: Random Forest Regressor
- **Features**: Same as risk assessment
- **Output**: Expected annual return percentage

### Model Training
The models are trained on synthetic data for demonstration. In a production environment, you would:
1. Collect real financial data
2. Train models on historical performance
3. Implement proper validation and testing
4. Update models regularly with new data

## 🎨 Customization

### Adding New Investment Categories
1. Update `INVESTMENT_CATEGORIES` in `config.py`
2. Add descriptions in `financial_analyzer.py`
3. Update visualization colors in `visualizations.py`

### Modifying Risk Assessment
1. Adjust `RISK_TOLERANCE_MAPPING` in `config.py`
2. Update age-based adjustments in `AGE_ADJUSTMENTS`
3. Modify the ML model training data

### UI Customization
- Modify `app.py` for layout changes
- Update `visualizations.py` for chart styling
- Customize colors and themes in the Streamlit configuration

## 🔒 Security & Privacy

### Data Storage
- User data is stored locally in SQLite database
- Passwords are hashed using SHA-256
- No data is sent to external servers (except market data)

### Authentication
- Simple username/password authentication
- Session management with SQLite
- No external authentication providers

### Privacy
- All data remains on your local machine
- No tracking or analytics
- Open source for transparency

## 🚨 Important Disclaimers

### Educational Purpose
This application is designed for educational and informational purposes only. It should not be considered as professional financial advice.

### Investment Risks
- All investments carry risk
- Past performance doesn't guarantee future results
- You may lose some or all of your invested capital
- Always consult with qualified financial advisors

### Data Accuracy
- Market data is provided by third-party APIs
- Analysis is based on simplified models
- Real-world financial planning is more complex

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

2. **Market Data Issues**
   - Check internet connection
   - Verify yfinance is working: `pip install --upgrade yfinance`

3. **Database Errors**
   - Delete `user_data.db` to reset the database
   - Check file permissions

4. **Memory Issues**
   - Reduce the number of market symbols
   - Close other applications

### Performance Optimization
- Use virtual environment
- Close unused browser tabs
- Restart the application periodically
- Clear browser cache if needed

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Include type hints where possible
- Write clear commit messages

## 📈 Future Enhancements

### Planned Features
- [ ] Real-time portfolio tracking
- [ ] Advanced ML models (LSTM, Transformer)
- [ ] Integration with brokerage APIs
- [ ] Mobile app version
- [ ] Social features and sharing
- [ ] Advanced backtesting
- [ ] Tax optimization
- [ ] Retirement planning tools

### Technical Improvements
- [ ] Docker containerization
- [ ] Cloud deployment options
- [ ] Database migration tools
- [ ] API endpoints
- [ ] Unit and integration tests
- [ ] CI/CD pipeline

## 📞 Support

### Getting Help
- Check the troubleshooting section
- Review the code comments
- Open an issue on GitHub
- Contact the development team

### Documentation
- Code is well-documented
- README provides comprehensive guide
- Inline comments explain complex logic
- Type hints improve code readability

## 📄 License

This project is open source and available under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit** for the amazing web framework
- **yfinance** for market data access
- **scikit-learn** and **TensorFlow** for ML capabilities
- **Plotly** for interactive visualizations
- **ReportLab** for PDF generation
- **Python community** for excellent libraries

---

**Remember**: This is an educational tool. Always consult with professional financial advisors before making investment decisions.

**Happy Investing! 🚀💰**
