"""
Export manager for generating reports and sharing data.
Supports multiple formats and delivery methods.
"""

import logging
from typing import Dict, List, Optional, Any, Union
import pandas as pd
from datetime import datetime, timedelta
import io
import base64
from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import plotly.graph_objects as go
import plotly.express as px
from jinja2 import Template

logger = logging.getLogger(__name__)

class ExportManager:
    """Comprehensive export and reporting manager."""
    
    def __init__(self):
        self.export_formats = {
            'csv': self._export_csv,
            'excel': self._export_excel,
            'json': self._export_json,
            'pdf': self._export_pdf,
            'html': self._export_html,
            'parquet': self._export_parquet
        }
        
    def export_data(self, data: pd.DataFrame, format_type: str, 
                   output_path: str, **kwargs) -> str:
        """Export data in specified format."""
        if format_type not in self.export_formats:
            raise ValueError(f"Unsupported export format: {format_type}")
            
        try:
            return self.export_formats[format_type](data, output_path, **kwargs)
        except Exception as e:
            logger.error(f"Export failed for format {format_type}: {e}")
            raise
    
    def _export_csv(self, data: pd.DataFrame, output_path: str, **kwargs) -> str:
        """Export to CSV format."""
        data.to_csv(output_path, index=False, **kwargs)
        logger.info(f"Data exported to CSV: {output_path}")
        return output_path
    
    def _export_excel(self, data: pd.DataFrame, output_path: str, **kwargs) -> str:
        """Export to Excel format with multiple sheets."""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            if isinstance(data, dict):
                # Multiple sheets
                for sheet_name, df in data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                # Single sheet
                data.to_excel(writer, sheet_name='Data', index=False)
                
        logger.info(f"Data exported to Excel: {output_path}")
        return output_path
    
    def _export_json(self, data: pd.DataFrame, output_path: str, **kwargs) -> str:
        """Export to JSON format."""
        orient = kwargs.get('orient', 'records')
        data.to_json(output_path, orient=orient, **kwargs)
        logger.info(f"Data exported to JSON: {output_path}")
        return output_path
    
    def _export_parquet(self, data: pd.DataFrame, output_path: str, **kwargs) -> str:
        """Export to Parquet format."""
        data.to_parquet(output_path, **kwargs)
        logger.info(f"Data exported to Parquet: {output_path}")
        return output_path
    
    def _export_pdf(self, data: pd.DataFrame, output_path: str, **kwargs) -> str:
        """Export to PDF report format."""
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title = kwargs.get('title', 'Data Analysis Report')
        story.append(Paragraph(title, styles['Title']))
        story.append(Spacer(1, 12))
        
        # Summary statistics
        if not data.empty:
            story.append(Paragraph('Summary Statistics', styles['Heading2']))
            
            # Create summary table
            summary_data = data.describe()
            table_data = [['Metric'] + list(summary_data.columns)]
            
            for index, row in summary_data.iterrows():
                table_data.append([index] + [f"{val:.2f}" if isinstance(val, (int, float)) else str(val) 
                                           for val in row])
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            story.append(Spacer(1, 12))
        
        # Data preview
        story.append(Paragraph('Data Preview', styles['Heading2']))
        preview_data = data.head(10)
        
        if not preview_data.empty:
            table_data = [list(preview_data.columns)]
            for _, row in preview_data.iterrows():
                table_data.append([str(val) for val in row])
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
        
        doc.build(story)
        logger.info(f"Data exported to PDF: {output_path}")
        return output_path
    
    def _export_html(self, data: pd.DataFrame, output_path: str, **kwargs) -> str:
        """Export to HTML format with styling."""
        title = kwargs.get('title', 'Data Analysis Report')
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{ title }}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #333; border-bottom: 2px solid #333; }
                h2 { color: #666; margin-top: 30px; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; font-weight: bold; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .summary { background-color: #e8f4fd; padding: 15px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>{{ title }}</h1>
            <div class="summary">
                <h2>Dataset Summary</h2>
                <p><strong>Total Records:</strong> {{ total_records }}</p>
                <p><strong>Total Columns:</strong> {{ total_columns }}</p>
                <p><strong>Generated:</strong> {{ timestamp }}</p>
            </div>
            
            <h2>Data Preview</h2>
            {{ data_table }}
            
            {% if summary_stats %}
            <h2>Summary Statistics</h2>
            {{ summary_table }}
            {% endif %}
        </body>
        </html>
        """
        
        template = Template(html_template)
        
        # Generate summary statistics if numeric columns exist
        summary_stats = None
        summary_table = ""
        
        numeric_columns = data.select_dtypes(include=['number']).columns
        if len(numeric_columns) > 0:
            summary_stats = data[numeric_columns].describe()
            summary_table = summary_stats.to_html(classes='summary-table')
        
        html_content = template.render(
            title=title,
            total_records=len(data),
            total_columns=len(data.columns),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            data_table=data.head(20).to_html(classes='data-table'),
            summary_stats=summary_stats is not None,
            summary_table=summary_table
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        logger.info(f"Data exported to HTML: {output_path}")
        return output_path

class ReportGenerator:
    """Advanced report generation with visualizations."""
    
    def __init__(self, export_manager: ExportManager):
        self.export_manager = export_manager
        
    def generate_dashboard_report(self, data: Dict[str, pd.DataFrame], 
                                output_path: str, format_type: str = 'pdf') -> str:
        """Generate comprehensive dashboard report."""
        
        if format_type == 'html':
            return self._generate_html_dashboard(data, output_path)
        elif format_type == 'pdf':
            return self._generate_pdf_dashboard(data, output_path)
        else:
            raise ValueError(f"Unsupported dashboard format: {format_type}")
    
    def _generate_html_dashboard(self, data: Dict[str, pd.DataFrame], output_path: str) -> str:
        """Generate HTML dashboard with interactive charts."""
        
        dashboard_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Business Analytics Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
                .metric-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
                .chart-container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 30px; }
                .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
                .metric-value { font-size: 2em; font-weight: bold; color: #333; }
                .metric-label { color: #666; margin-top: 5px; }
                h1 { margin: 0; font-size: 2.5em; }
                h2 { color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Business Analytics Dashboard</h1>
                    <p>Generated on {{ timestamp }}</p>
                </div>
                
                <div class="metrics-grid">
                    {% for metric in key_metrics %}
                    <div class="metric-card">
                        <div class="metric-value">{{ metric.value }}</div>
                        <div class="metric-label">{{ metric.label }}</div>
                    </div>
                    {% endfor %}
                </div>
                
                {% for chart in charts %}
                <div class="chart-container">
                    <h2>{{ chart.title }}</h2>
                    <div id="{{ chart.id }}"></div>
                </div>
                {% endfor %}
            </div>
            
            <script>
                {% for chart in charts %}
                Plotly.newPlot('{{ chart.id }}', {{ chart.data }}, {{ chart.layout }});
                {% endfor %}
            </script>
        </body>
        </html>
        """
        
        # Generate key metrics
        key_metrics = []
        charts = []
        
        if 'transactions' in data:
            df = data['transactions']
            key_metrics.extend([
                {'value': f"${df['total_amount'].sum():,.2f}", 'label': 'Total Revenue'},
                {'value': f"{len(df):,}", 'label': 'Total Transactions'},
                {'value': f"${df['total_amount'].mean():.2f}", 'label': 'Average Order Value'},
                {'value': f"{df['customer_id'].nunique():,}", 'label': 'Unique Customers'}
            ])
            
            # Revenue trend chart
            daily_revenue = df.groupby(df['transaction_date'].dt.date)['total_amount'].sum().reset_index()
            
            fig = px.line(daily_revenue, x='transaction_date', y='total_amount', 
                         title='Daily Revenue Trend')
            
            charts.append({
                'id': 'revenue-trend',
                'title': 'Revenue Trend Over Time',
                'data': fig.to_json(),
                'layout': fig.layout.to_plotly_json()
            })
        
        template = Template(dashboard_template)
        html_content = template.render(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            key_metrics=key_metrics,
            charts=charts
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        logger.info(f"HTML dashboard generated: {output_path}")
        return output_path
    
    def _generate_pdf_dashboard(self, data: Dict[str, pd.DataFrame], output_path: str) -> str:
        """Generate PDF dashboard report."""
        # Implementation for PDF dashboard
        # This would create charts using matplotlib and combine them in PDF
        logger.info(f"PDF dashboard generated: {output_path}")
        return output_path

class EmailReporter:
    """Email reporting and delivery system."""
    
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        
    def send_report(self, recipients: List[str], subject: str, 
                   body: str, attachments: List[str] = None):
        """Send email report with attachments."""
        
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'html'))
        
        # Add attachments
        if attachments:
            for file_path in attachments:
                with open(file_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {Path(file_path).name}'
                )
                msg.attach(part)
        
        # Send email
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Report sent to {len(recipients)} recipients")
            
        except Exception as e:
            logger.error(f"Failed to send email report: {e}")
            raise

class ScheduledReporter:
    """Scheduled reporting system."""
    
    def __init__(self, export_manager: ExportManager, email_reporter: EmailReporter = None):
        self.export_manager = export_manager
        self.email_reporter = email_reporter
        self.scheduled_reports = {}
        
    def schedule_report(self, name: str, data_source: Callable, 
                       schedule: str, format_type: str, recipients: List[str] = None):
        """Schedule a recurring report."""
        self.scheduled_reports[name] = {
            'data_source': data_source,
            'schedule': schedule,  # cron-like format
            'format_type': format_type,
            'recipients': recipients or [],
            'last_run': None
        }
        
        logger.info(f"Scheduled report: {name} ({schedule})")
    
    def run_scheduled_reports(self):
        """Run all scheduled reports that are due."""
        current_time = datetime.now()
        
        for name, config in self.scheduled_reports.items():
            if self._should_run_report(config, current_time):
                try:
                    self._execute_scheduled_report(name, config)
                    config['last_run'] = current_time
                except Exception as e:
                    logger.error(f"Failed to run scheduled report {name}: {e}")
    
    def _should_run_report(self, config: Dict, current_time: datetime) -> bool:
        """Check if report should run based on schedule."""
        # Simplified scheduling logic
        # In production, use a proper cron parser
        if config['last_run'] is None:
            return True
            
        schedule = config['schedule']
        last_run = config['last_run']
        
        if schedule == 'daily':
            return (current_time - last_run).days >= 1
        elif schedule == 'weekly':
            return (current_time - last_run).days >= 7
        elif schedule == 'monthly':
            return (current_time - last_run).days >= 30
            
        return False
    
    def _execute_scheduled_report(self, name: str, config: Dict):
        """Execute a scheduled report."""
        # Get data from source
        data = config['data_source']()
        
        # Generate report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"reports/{name}_{timestamp}.{config['format_type']}"
        
        self.export_manager.export_data(data, config['format_type'], output_path)
        
        # Send via email if configured
        if self.email_reporter and config['recipients']:
            subject = f"Scheduled Report: {name}"
            body = f"""
            <h2>Scheduled Report: {name}</h2>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Please find the attached report.</p>
            """
            
            self.email_reporter.send_report(
                config['recipients'],
                subject,
                body,
                [output_path]
            )
        
        logger.info(f"Executed scheduled report: {name}")