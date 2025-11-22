"""
Main Streamlit application for AI-Driven Investment Advisor
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import json

# Import custom modules
from financial_analyzer import FinancialAnalyzer
from visualizations import InvestmentVisualizer
from auth_manager import login_page, logout, AuthManager
from pdf_generator import PDFGenerator
import config

# Page configuration
st.set_page_config(
    page_title="AI Investment Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}
if 'analysis_result' not in st.session_state:
    st.session_state['analysis_result'] = {}
if 'allocation_data' not in st.session_state:
    st.session_state['allocation_data'] = {}

def main():
    """Main application function"""
    if not st.session_state['authenticated']:
        login_page()
        return
    
    # Sidebar
    with st.sidebar:
        st.title("💰 AI Investment Advisor")
        st.markdown("---")
        
        # User info
        st.write(f"Welcome, {st.session_state.get('username', 'User')}!")
        
        # Navigation
        page = st.selectbox(
            "Navigate",
            ["📊 Dashboard", "📝 Input Data", "📈 Analysis", "📋 Reports", "⚙️ Settings"]
        )
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout"):
            logout()
    
    # Main content area
    if page == "📊 Dashboard":
        dashboard_page()
    elif page == "📝 Input Data":
        input_data_page()
    elif page == "📈 Analysis":
        analysis_page()
    elif page == "📋 Reports":
        reports_page()
    elif page == "⚙️ Settings":
        settings_page()

def dashboard_page():
    """Main dashboard page"""
    st.title("📊 Investment Dashboard")
    
    if not st.session_state.get('user_data'):
        st.warning("Please input your financial data first in the 'Input Data' section.")
        return
    
    # Initialize components
    analyzer = FinancialAnalyzer()
    visualizer = InvestmentVisualizer()
    
    # Get user data and analysis
    user_data = st.session_state['user_data']
    analysis_result = st.session_state.get('analysis_result', {})
    allocation_data = st.session_state.get('allocation_data', {})
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Risk Score",
            f"{analysis_result.get('risk_score', 0):.2f}",
            delta=f"{analysis_result.get('risk_category', 'N/A').title()}"
        )
    
    with col2:
        st.metric(
            "Expected Return",
            f"{analysis_result.get('expected_return', 0):.1%}",
            delta="Annual"
        )
    
    with col3:
        st.metric(
            "Investable Amount",
            f"${user_data.get('savings', 0) * 0.8:,.0f}",
            delta="80% of savings"
        )
    
    with col4:
        st.metric(
            "Age",
            f"{user_data.get('age', 0)}",
            delta="Years"
        )
    
    st.markdown("---")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Investment Allocation")
        if allocation_data and len(allocation_data) > 0:
            fig = visualizer.create_pie_chart(allocation_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Complete the analysis to see investment allocation")
            fig = visualizer.create_pie_chart({})
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Risk vs Return Analysis")
        if analysis_result and analysis_result.get('risk_score') is not None:
            fig = visualizer.create_risk_return_scatter(user_data, analysis_result)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Complete the analysis to see risk assessment")
    
    # Market overview
    st.subheader("Market Overview")
    
    # Popular symbols for market data
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'BTC-USD', 'ETH-USD']
    
    try:
        market_data = analyzer.get_market_data(symbols)
        
        if market_data:
            # Create market table
            market_df = pd.DataFrame(market_data).T
            market_df = market_df.reset_index()
            market_df.columns = ['Symbol', 'Price', 'Change %', 'Volume', '52W High', '52W Low']
            
            st.dataframe(market_df, use_container_width=True)
            
            # Market trends chart
            fig = visualizer.create_market_trends(market_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Unable to fetch market data. Please check your internet connection.")
    
    except Exception as e:
        st.error(f"Error fetching market data: {str(e)}")

def input_data_page():
    """User input data page"""
    st.title("📝 Financial Data Input")
    
    # Initialize goals in session state if not exists
    if 'goals' not in st.session_state:
        st.session_state['goals'] = []
    
    # Financial Goals Section (Outside of form)
    st.subheader("Financial Goals (Optional)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        goal_description = st.text_input("Goal Description", key="goal_desc")
    with col2:
        goal_amount = st.number_input("Target Amount ($)", min_value=0, value=0, step=1000, key="goal_amount")
    with col3:
        goal_timeframe = st.number_input("Timeframe (years)", min_value=1, max_value=50, value=5, key="goal_timeframe")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Add Goal"):
            if goal_description and goal_amount > 0:
                st.session_state['goals'].append({
                    "description": goal_description,
                    "amount": goal_amount,
                    "timeframe": goal_timeframe
                })
                st.success(f"Added goal: {goal_description}")
                st.rerun()
            else:
                st.warning("Please enter both description and amount")
    
    # Display current goals
    if st.session_state['goals']:
        st.write("**Current Goals:**")
        for i, goal in enumerate(st.session_state['goals']):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{i+1}. {goal['description']} - ${goal['amount']:,} in {goal['timeframe']} years")
            with col2:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state['goals'].pop(i)
                    st.rerun()
    
    st.markdown("---")
    
    # Main form for financial data
    with st.form("financial_data_form"):
        st.subheader("Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            income = st.number_input("Annual Income ($)", min_value=0, value=50000, step=1000)
        
        with col2:
            expenses = st.number_input("Annual Expenses ($)", min_value=0, value=30000, step=1000)
            savings = st.number_input("Current Savings ($)", min_value=0, value=10000, step=1000)
        
        st.subheader("Risk Assessment")
        
        risk_tolerance = st.select_slider(
            "Risk Tolerance",
            options=["Conservative", "Moderate", "Aggressive"],
            value="Moderate"
        )
        
        submitted = st.form_submit_button("Analyze My Profile")
        
        if submitted:
            # Convert risk tolerance to numeric
            risk_mapping = {"Conservative": 0.2, "Moderate": 0.5, "Aggressive": 0.8}
            risk_score = risk_mapping[risk_tolerance]
            
            # Store user data
            user_data = {
                'age': age,
                'income': income,
                'expenses': expenses,
                'savings': savings,
                'risk_tolerance': risk_score,
                'goals': st.session_state['goals']
            }
            
            st.session_state['user_data'] = user_data
            
            # Perform analysis
            analyzer = FinancialAnalyzer()
            analysis_result = analyzer.analyze_user_profile(user_data)
            allocation_data = analyzer.calculate_investment_allocation(user_data, analysis_result)
            advice_data = analyzer.generate_advice_report(user_data, analysis_result, allocation_data, {})
            
            # Store results
            st.session_state['analysis_result'] = analysis_result
            st.session_state['allocation_data'] = allocation_data
            st.session_state['advice_data'] = advice_data
            
            st.success("Analysis complete! Check the 'Analysis' tab for detailed results.")
            st.rerun()

def analysis_page():
    """Analysis and recommendations page"""
    st.title("📈 Investment Analysis")
    
    if not st.session_state.get('user_data'):
        st.warning("Please input your financial data first.")
        return
    
    user_data = st.session_state['user_data']
    analysis_result = st.session_state.get('analysis_result', {})
    allocation_data = st.session_state.get('allocation_data', {})
    advice_data = st.session_state.get('advice_data', {})
    
    # Initialize visualizer
    visualizer = InvestmentVisualizer()
    
    # Analysis summary
    st.subheader("Analysis Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Risk Category:** {analysis_result.get('risk_category', 'N/A').title()}")
        st.info(f"**Risk Score:** {analysis_result.get('risk_score', 0):.2f}")
    
    with col2:
        st.success(f"**Expected Return:** {analysis_result.get('expected_return', 0):.1%}")
        st.success(f"**Investable Amount:** ${user_data.get('savings', 0) * 0.8:,.0f}")
    
    st.markdown("---")
    
    # Investment allocation
    st.subheader("Recommended Investment Allocation")
    
    if allocation_data and len(allocation_data) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = visualizer.create_pie_chart(allocation_data)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Allocation table
            try:
                allocation_df = pd.DataFrame([
                    {
                        'Category': category.replace('_', ' ').title(),
                        'Percentage': f"{data['percentage']:.1f}%",
                        'Amount': f"${data['amount']:,.0f}",
                        'Description': data.get('description', 'N/A')
                    }
                    for category, data in allocation_data.items()
                    if isinstance(data, dict) and data.get('percentage', 0) > 0
                ])
                
                if not allocation_df.empty:
                    st.dataframe(allocation_df, use_container_width=True)
                else:
                    st.info("No allocation data available. Please complete the analysis first.")
            except Exception as e:
                st.error(f"Error displaying allocation data: {str(e)}")
                st.info("Please complete the analysis in the 'Input Data' tab first.")
    else:
        st.info("No allocation data available. Please complete the analysis in the 'Input Data' tab first.")
        # Show empty pie chart
        fig = visualizer.create_pie_chart({})
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    if advice_data:
        st.subheader("Personalized Recommendations")
        
        st.write(advice_data.get('summary', 'No summary available.'))
        
        st.write("**Key Recommendations:**")
        for i, recommendation in enumerate(advice_data.get('recommendations', []), 1):
            st.write(f"{i}. {recommendation}")
    
    # Additional visualizations
    st.subheader("Additional Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = visualizer.create_age_risk_analysis(user_data, analysis_result)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = visualizer.create_income_allocation_chart(user_data, allocation_data)
        st.plotly_chart(fig, use_container_width=True)
    
    # Goals timeline
    if user_data.get('goals'):
        st.subheader("Goal Achievement Timeline")
        fig = visualizer.create_goal_timeline(user_data, analysis_result)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

def reports_page():
    """Reports and export page"""
    st.title("📋 Reports & Export")
    
    if not st.session_state.get('user_data'):
        st.warning("Please complete the analysis first.")
        return
    
    user_data = st.session_state['user_data']
    analysis_result = st.session_state.get('analysis_result', {})
    allocation_data = st.session_state.get('allocation_data', {})
    advice_data = st.session_state.get('advice_data', {})
    
    # Generate market data for report
    analyzer = FinancialAnalyzer()
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'BTC-USD', 'ETH-USD']
    
    try:
        market_data = analyzer.get_market_data(symbols)
    except:
        market_data = {}
    
    # PDF Generation
    st.subheader("Export Reports")
    
    pdf_generator = PDFGenerator()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Generate Full Report (PDF)"):
            try:
                pdf_content = pdf_generator.generate_investment_report(
                    user_data, analysis_result, allocation_data, advice_data, market_data
                )
                
                st.download_button(
                    label="Download Full Report",
                    data=pdf_content,
                    file_name=f"investment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
                st.success("Full report generated successfully!")
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
    
    with col2:
        if st.button("📋 Generate Quick Summary (PDF)"):
            try:
                pdf_content = pdf_generator.generate_simple_report(
                    user_data, analysis_result, allocation_data
                )
                
                st.download_button(
                    label="Download Quick Summary",
                    data=pdf_content,
                    file_name=f"quick_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
                st.success("Quick summary generated successfully!")
            except Exception as e:
                st.error(f"Error generating summary: {str(e)}")
    
    # Session management
    st.subheader("Session Management")
    
    auth_manager = AuthManager()
    user_id = st.session_state.get('user_id')
    
    if user_id:
        # Save current session
        if st.button("💾 Save Current Session"):
            session_data = {
                'user_data': user_data,
                'analysis_result': analysis_result,
                'allocation_data': allocation_data,
                'advice_data': advice_data,
                'timestamp': datetime.now().isoformat()
            }
            
            if auth_manager.save_session(user_id, session_data):
                st.success("Session saved successfully!")
            else:
                st.error("Failed to save session.")
        
        # Load previous sessions
        st.write("**Previous Sessions:**")
        sessions = auth_manager.get_user_sessions(user_id)
        
        if sessions:
            for session in sessions[:5]:  # Show last 5 sessions
                session_data = session[1]
                timestamp = session[2]
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"Session from {timestamp}")
                
                with col2:
                    if st.button(f"Load", key=f"load_{session[0]}"):
                        try:
                            data = json.loads(session_data)
                            st.session_state['user_data'] = data.get('user_data', {})
                            st.session_state['analysis_result'] = data.get('analysis_result', {})
                            st.session_state['allocation_data'] = data.get('allocation_data', {})
                            st.session_state['advice_data'] = data.get('advice_data', {})
                            st.success("Session loaded!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to load session: {str(e)}")
                
                with col3:
                    if st.button(f"Delete", key=f"delete_{session[0]}"):
                        if auth_manager.delete_session(session[0]):
                            st.success("Session deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete session.")
        else:
            st.write("No previous sessions found.")

def settings_page():
    """Settings and configuration page"""
    st.title("⚙️ Settings")
    
    st.subheader("User Preferences")
    
    # Theme selection
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    
    # Notification preferences
    st.subheader("Notifications")
    email_notifications = st.checkbox("Email notifications", value=True)
    market_alerts = st.checkbox("Market alerts", value=False)
    
    # Data preferences
    st.subheader("Data Preferences")
    auto_refresh = st.checkbox("Auto-refresh market data", value=True)
    refresh_interval = st.slider("Refresh interval (minutes)", 1, 60, 5)
    
    # Save settings
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
    
    st.markdown("---")
    
    # About section
    st.subheader("About")
    st.write("**AI-Driven Investment Advisor v1.0**")
    st.write("Built with Python, Streamlit, and Machine Learning")
    st.write("For educational and informational purposes only.")
    
    # Disclaimer
    st.subheader("Disclaimer")
    st.warning("""
    This application is for educational purposes only and should not be considered as professional financial advice. 
    Always consult with qualified financial advisors before making investment decisions.
    """)

if __name__ == "__main__":
    main()
