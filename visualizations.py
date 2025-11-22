"""
Data visualization module for investment advisor
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class InvestmentVisualizer:
    def __init__(self):
        self.colors = {
            'low_risk': '#2E8B57',      # Sea Green
            'medium_risk': '#FF8C00',    # Dark Orange
            'high_risk': '#DC143C',      # Crimson
            'fixed_deposits': '#4169E1', # Royal Blue
            'government_bonds': '#32CD32', # Lime Green
            'money_market_funds': '#20B2AA', # Light Sea Green
            'mutual_funds': '#FF6347',   # Tomato
            'etfs': '#9370DB',          # Medium Purple
            'stocks': '#FF1493',        # Deep Pink
            'crypto': '#FFD700'         # Gold
        }
    
    def create_pie_chart(self, allocation_data, title="Investment Allocation"):
        """Create pie chart for investment allocation"""
        # Check if allocation_data is empty or None
        if not allocation_data or len(allocation_data) == 0:
            # Return empty chart with message
            fig = go.Figure()
            fig.add_annotation(
                text="No allocation data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="gray")
            )
            fig.update_layout(
                title=title,
                title_x=0.5,
                height=500,
                showlegend=False,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
            return fig
        
        # Validate data structure
        try:
            categories = []
            percentages = []
            colors = []
            
            for category, data in allocation_data.items():
                if isinstance(data, dict) and 'percentage' in data:
                    if data['percentage'] > 0:  # Only include non-zero allocations
                        categories.append(category.replace('_', ' ').title())
                        percentages.append(data['percentage'])
                        colors.append(self.colors.get(category, '#808080'))
                elif isinstance(data, (int, float)) and data > 0:
                    # Handle simple numeric data
                    categories.append(category.replace('_', ' ').title())
                    percentages.append(data)
                    colors.append(self.colors.get(category, '#808080'))
            
            if not categories:
                # Return empty chart if no valid data
                fig = go.Figure()
                fig.add_annotation(
                    text="No valid allocation data",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=16, color="gray")
                )
                fig.update_layout(
                    title=title,
                    title_x=0.5,
                    height=500,
                    showlegend=False,
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                )
                return fig
            
            fig = go.Figure(data=[go.Pie(
                labels=categories,
                values=percentages,
                hole=0.3,
                marker_colors=colors,
                textinfo='label+percent',
                textfont_size=12
            )])
            
            fig.update_layout(
                title=title,
                title_x=0.5,
                font=dict(size=14),
                showlegend=True,
                height=500
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating pie chart: {e}")
            # Return error chart
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error creating chart: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14, color="red")
            )
            fig.update_layout(
                title=title,
                title_x=0.5,
                height=500,
                showlegend=False,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
            return fig
    
    def create_risk_return_scatter(self, user_data, analysis_result):
        """Create risk-return scatter plot"""
        risk_score = analysis_result['risk_score']
        expected_return = analysis_result['expected_return']
        
        # Create sample data for context
        np.random.seed(42)
        n_points = 100
        sample_risks = np.random.uniform(0, 1, n_points)
        sample_returns = np.random.uniform(0.02, 0.18, n_points)
        
        fig = go.Figure()
        
        # Add sample data
        fig.add_trace(go.Scatter(
            x=sample_risks,
            y=sample_returns,
            mode='markers',
            marker=dict(
                size=8,
                color=sample_returns,
                colorscale='Viridis',
                opacity=0.6,
                showscale=True,
                colorbar=dict(title="Expected Return")
            ),
            name='Market Portfolio',
            text=[f'Risk: {r:.2f}<br>Return: {ret:.2%}' for r, ret in zip(sample_risks, sample_returns)],
            hovertemplate='%{text}<extra></extra>'
        ))
        
        # Add user's point
        fig.add_trace(go.Scatter(
            x=[risk_score],
            y=[expected_return],
            mode='markers',
            marker=dict(
                size=15,
                color='red',
                symbol='star',
                line=dict(width=2, color='black')
            ),
            name='Your Profile',
            text=[f'Your Risk: {risk_score:.2f}<br>Your Expected Return: {expected_return:.2%}'],
            hovertemplate='%{text}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Risk vs Return Analysis",
            xaxis_title="Risk Score",
            yaxis_title="Expected Return",
            height=500,
            showlegend=True
        )
        
        return fig
    
    def create_market_trends(self, market_data):
        """Create market trends visualization"""
        if not market_data:
            return None
        
        symbols = list(market_data.keys())
        prices = [data['current_price'] for data in market_data.values()]
        changes = [data['change_percent'] for data in market_data.values()]
        
        fig = go.Figure()
        
        # Add price bars
        fig.add_trace(go.Bar(
            x=symbols,
            y=prices,
            name='Current Price',
            marker_color='lightblue',
            yaxis='y'
        ))
        
        # Add change line
        fig.add_trace(go.Scatter(
            x=symbols,
            y=changes,
            mode='lines+markers',
            name='Daily Change %',
            line=dict(color='red', width=3),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Market Overview",
            xaxis_title="Symbols",
            yaxis=dict(title="Price ($)", side="left"),
            yaxis2=dict(title="Change (%)", side="right", overlaying="y"),
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_age_risk_analysis(self, user_data, analysis_result):
        """Create age-based risk analysis"""
        age = user_data['age']
        risk_score = analysis_result['risk_score']
        
        # Age ranges and typical risk scores
        age_ranges = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
        typical_risks = [0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
        
        fig = go.Figure()
        
        # Add typical risk line
        fig.add_trace(go.Scatter(
            x=age_ranges,
            y=typical_risks,
            mode='lines+markers',
            name='Typical Risk Profile',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))
        
        # Add user's point
        user_age_range = self._get_age_range(age)
        user_risk = risk_score
        
        fig.add_trace(go.Scatter(
            x=[user_age_range],
            y=[user_risk],
            mode='markers',
            name='Your Profile',
            marker=dict(
                size=15,
                color='red',
                symbol='star',
                line=dict(width=2, color='black')
            )
        ))
        
        fig.update_layout(
            title="Age vs Risk Tolerance Analysis",
            xaxis_title="Age Range",
            yaxis_title="Risk Score",
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_income_allocation_chart(self, user_data, allocation_data):
        """Create income allocation visualization"""
        income = user_data['income']
        expenses = user_data['expenses']
        savings = user_data['savings']
        
        # Calculate amounts
        investable = savings * 0.8
        emergency_fund = savings * 0.2
        
        categories = ['Monthly Income', 'Monthly Expenses', 'Savings', 'Emergency Fund', 'Investable Amount']
        amounts = [income, expenses, savings, emergency_fund, investable]
        colors = ['#2E8B57', '#DC143C', '#4169E1', '#FF8C00', '#9370DB']
        
        fig = go.Figure(data=[go.Bar(
            x=categories,
            y=amounts,
            marker_color=colors,
            text=[f'${amount:,.0f}' for amount in amounts],
            textposition='auto'
        )])
        
        fig.update_layout(
            title="Financial Overview",
            xaxis_title="Categories",
            yaxis_title="Amount ($)",
            height=400
        )
        
        return fig
    
    def create_goal_timeline(self, user_data, analysis_result):
        """Create goal achievement timeline"""
        if 'goals' not in user_data:
            return None
        
        goals = user_data['goals']
        expected_return = analysis_result['expected_return']
        
        # Calculate timeline for each goal
        timelines = []
        for goal in goals:
            if 'amount' in goal and 'timeframe' in goal:
                amount = goal['amount']
                timeframe = goal['timeframe']
                timelines.append({
                    'goal': goal.get('description', 'Financial Goal'),
                    'amount': amount,
                    'timeframe': timeframe,
                    'monthly_investment': self._calculate_monthly_investment(amount, timeframe, expected_return)
                })
        
        if not timelines:
            return None
        
        fig = go.Figure()
        
        for i, timeline in enumerate(timelines):
            fig.add_trace(go.Bar(
                x=[timeline['goal']],
                y=[timeline['monthly_investment']],
                name=f"Goal {i+1}",
                text=f"${timeline['monthly_investment']:,.0f}/month",
                textposition='auto'
            ))
        
        fig.update_layout(
            title="Monthly Investment Required for Goals",
            xaxis_title="Goals",
            yaxis_title="Monthly Investment ($)",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def _get_age_range(self, age):
        """Get age range string for given age"""
        if age <= 25:
            return '18-25'
        elif age <= 35:
            return '26-35'
        elif age <= 45:
            return '36-45'
        elif age <= 55:
            return '46-55'
        elif age <= 65:
            return '56-65'
        else:
            return '65+'
    
    def _calculate_monthly_investment(self, goal_amount, years, annual_return):
        """Calculate monthly investment needed for goal"""
        monthly_return = annual_return / 12
        months = years * 12
        
        if monthly_return == 0:
            return goal_amount / months
        
        monthly_investment = goal_amount * (monthly_return) / ((1 + monthly_return) ** months - 1)
        return monthly_investment
