"""
PDF report generation module
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkgreen
        ))
        
        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_LEFT
        ))
        
        # Risk style
        self.styles.add(ParagraphStyle(
            name='RiskStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            textColor=colors.red,
            alignment=TA_LEFT
        ))
    
    def generate_investment_report(self, user_data, analysis_result, allocation_data, advice_data, market_data=None):
        """Generate comprehensive investment report PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # Build the content
        story = []
        
        # Title
        story.append(Paragraph("AI-Driven Investment Advisor Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Date
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", self.styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # User Profile Section
        story.append(Paragraph("Personal Financial Profile", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 12))
        
        profile_data = [
            ['Age', str(user_data.get('age', 'N/A'))],
            ['Annual Income', f"${user_data.get('income', 0):,.2f}"],
            ['Annual Expenses', f"${user_data.get('expenses', 0):,.2f}"],
            ['Current Savings', f"${user_data.get('savings', 0):,.2f}"],
            ['Risk Tolerance', analysis_result.get('risk_category', 'N/A').title()],
            ['Risk Score', f"{analysis_result.get('risk_score', 0):.2f}"],
            ['Expected Return', f"{analysis_result.get('expected_return', 0):.1%}"]
        ]
        
        profile_table = Table(profile_data, colWidths=[2*inch, 2*inch])
        profile_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(profile_table)
        story.append(Spacer(1, 20))
        
        # Investment Allocation Section
        story.append(Paragraph("Recommended Investment Allocation", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 12))
        
        allocation_data_table = []
        allocation_data_table.append(['Investment Category', 'Percentage', 'Amount', 'Description'])
        
        for category, data in allocation_data.items():
            allocation_data_table.append([
                category.replace('_', ' ').title(),
                f"{data['percentage']:.1f}%",
                f"${data['amount']:,.2f}",
                data.get('description', 'N/A')
            ])
        
        allocation_table = Table(allocation_data_table, colWidths=[1.5*inch, 1*inch, 1.5*inch, 2*inch])
        allocation_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(allocation_table)
        story.append(Spacer(1, 20))
        
        # Recommendations Section
        story.append(Paragraph("Personalized Recommendations", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 12))
        
        # Summary
        story.append(Paragraph(f"<b>Summary:</b> {advice_data.get('summary', 'No summary available.')}", self.styles['CustomBody']))
        story.append(Spacer(1, 12))
        
        # Recommendations
        story.append(Paragraph("<b>Key Recommendations:</b>", self.styles['CustomBody']))
        story.append(Spacer(1, 6))
        
        for i, recommendation in enumerate(advice_data.get('recommendations', []), 1):
            story.append(Paragraph(f"{i}. {recommendation}", self.styles['CustomBody']))
        
        story.append(Spacer(1, 20))
        
        # Market Data Section (if available)
        if market_data:
            story.append(Paragraph("Current Market Overview", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 12))
            
            market_table_data = [['Symbol', 'Current Price', 'Daily Change', 'Volume']]
            
            for symbol, data in market_data.items():
                market_table_data.append([
                    symbol,
                    f"${data.get('current_price', 0):.2f}",
                    f"{data.get('change_percent', 0):.2f}%",
                    f"{data.get('volume', 0):,}"
                ])
            
            market_table = Table(market_table_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            market_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(market_table)
            story.append(Spacer(1, 20))
        
        # Disclaimer
        story.append(PageBreak())
        story.append(Paragraph("Important Disclaimer", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 12))
        
        disclaimer_text = """
        This report is generated by an AI-driven investment advisor and is for informational purposes only. 
        It should not be considered as professional financial advice. Investment decisions should be made 
        after consulting with qualified financial advisors and considering your personal circumstances. 
        Past performance does not guarantee future results. All investments carry risk, and you may lose 
        some or all of your invested capital.
        """
        
        story.append(Paragraph(disclaimer_text, self.styles['CustomBody']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    def generate_simple_report(self, user_data, analysis_result, allocation_data):
        """Generate a simplified report for quick reference"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        story.append(Paragraph("Quick Investment Summary", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Key metrics
        story.append(Paragraph(f"Risk Profile: {analysis_result.get('risk_category', 'N/A').title()}", self.styles['RiskStyle']))
        story.append(Paragraph(f"Expected Return: {analysis_result.get('expected_return', 0):.1%}", self.styles['CustomBody']))
        story.append(Spacer(1, 12))
        
        # Top 3 allocations
        story.append(Paragraph("Top Investment Recommendations:", self.styles['CustomSubtitle']))
        
        sorted_allocations = sorted(allocation_data.items(), key=lambda x: x[1]['percentage'], reverse=True)
        
        for i, (category, data) in enumerate(sorted_allocations[:3], 1):
            story.append(Paragraph(
                f"{i}. {category.replace('_', ' ').title()}: {data['percentage']:.1f}% (${data['amount']:,.2f})",
                self.styles['CustomBody']
            ))
        
        doc.build(story)
        buffer.seek(0)
        
        return buffer.getvalue()
