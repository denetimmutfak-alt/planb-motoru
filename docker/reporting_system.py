#!/usr/bin/env python3
"""
PlanB Motoru - Advanced Reporting System
Günlük PDF raporları, Excel vergi raporları, performans analitiği
"""

import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
import json
from pathlib import Path

# Report generation libraries
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.linecharts import HorizontalLineChart
    from reportlab.graphics.charts.piecharts import Pie
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("WARNING: ReportLab not available. PDF reports disabled")

# Database connection
import psycopg2
from psycopg2.extras import RealDictCursor

# Email sending (optional)
try:
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseReporter:
    """Database query helper for reporting"""
    
    def __init__(self, db_url: str):
        self.db_url = db_url
    
    def get_daily_summary(self, date: datetime.date) -> Dict:
        """Günlük özet verileri"""
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Signal summary
                    cur.execute("""
                        SELECT 
                            COUNT(*) as total_signals,
                            COUNT(CASE WHEN approval_status = 'APPROVED' THEN 1 END) as approved,
                            COUNT(CASE WHEN approval_status = 'REJECTED' THEN 1 END) as rejected,
                            COUNT(CASE WHEN approval_status = 'EXPIRED' THEN 1 END) as expired,
                            ROUND(AVG(confidence_score), 2) as avg_confidence,
                            signal,
                            COUNT(*) as signal_count
                        FROM signal_notifications 
                        WHERE DATE(timestamp) = %s
                        GROUP BY signal
                    """, [date])
                    
                    signal_data = cur.fetchall()
                    
                    # Trading performance
                    cur.execute("""
                        SELECT 
                            COUNT(*) as total_trades,
                            SUM(CASE WHEN profit_loss > 0 THEN 1 ELSE 0 END) as winning_trades,
                            SUM(profit_loss) as total_profit_loss,
                            AVG(profit_loss) as avg_profit_loss,
                            MAX(profit_loss) as max_profit,
                            MIN(profit_loss) as max_loss
                        FROM trading_performance 
                        WHERE DATE(entry_timestamp) = %s
                    """, [date])
                    
                    trading_data = cur.fetchone()
                    
                    # Model performance
                    cur.execute("""
                        SELECT 
                            module_name,
                            COUNT(*) as predictions,
                            AVG(confidence_score) as avg_confidence,
                            COUNT(CASE WHEN confidence_score >= 70 THEN 1 END) as high_confidence
                        FROM expert_results 
                        WHERE DATE(timestamp) = %s
                        GROUP BY module_name
                        ORDER BY avg_confidence DESC
                    """, [date])
                    
                    model_data = cur.fetchall()
                    
                    return {
                        'date': date,
                        'signals': signal_data,
                        'trading': trading_data,
                        'models': model_data
                    }
                    
        except Exception as e:
            logger.error(f"Database query error: {e}")
            return {}
    
    def get_user_decision_analysis(self, start_date: datetime.date, end_date: datetime.date) -> Dict:
        """Kullanıcı karar analizi"""
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        SELECT 
                            user_decision,
                            COUNT(*) as decision_count,
                            AVG(original_confidence) as avg_original_confidence,
                            AVG(decision_time_seconds) as avg_decision_time
                        FROM user_decisions 
                        WHERE DATE(timestamp) BETWEEN %s AND %s
                        GROUP BY user_decision
                    """, [start_date, end_date])
                    
                    decision_data = cur.fetchall()
                    
                    # Model vs User performance comparison
                    cur.execute("""
                        WITH model_signals AS (
                            SELECT symbol, final_signal, confidence_score, timestamp
                            FROM ensemble_results 
                            WHERE DATE(timestamp) BETWEEN %s AND %s
                            AND confidence_score >= 70
                        ),
                        user_decisions AS (
                            SELECT sn.symbol, sn.signal, ud.user_decision, sn.timestamp
                            FROM signal_notifications sn
                            JOIN user_decisions ud ON sn.id = ud.notification_id
                            WHERE DATE(sn.timestamp) BETWEEN %s AND %s
                        )
                        SELECT 
                            COUNT(ms.*) as total_model_signals,
                            COUNT(ud.*) as total_user_decisions,
                            COUNT(CASE WHEN ud.user_decision = 'APPROVED' THEN 1 END) as user_approved
                        FROM model_signals ms
                        LEFT JOIN user_decisions ud ON ms.symbol = ud.symbol 
                        AND ABS(EXTRACT(EPOCH FROM (ms.timestamp - ud.timestamp))) < 300
                    """, [start_date, end_date, start_date, end_date])
                    
                    comparison_data = cur.fetchone()
                    
                    return {
                        'decisions': decision_data,
                        'comparison': comparison_data
                    }
                    
        except Exception as e:
            logger.error(f"User decision analysis error: {e}")
            return {}

class PDFReportGenerator:
    """PDF rapor oluşturucu"""
    
    def __init__(self, output_dir: str = "/app/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.styles = getSampleStyleSheet() if REPORTLAB_AVAILABLE else None
    
    def generate_daily_report(self, report_data: Dict) -> Optional[str]:
        """Günlük PDF raporu oluştur"""
        if not REPORTLAB_AVAILABLE:
            logger.warning("ReportLab not available, skipping PDF generation")
            return None
            
        try:
            date = report_data.get('date', datetime.now().date())
            filename = f"planb_daily_report_{date.strftime('%Y%m%d')}.pdf"
            filepath = self.output_dir / filename
            
            doc = SimpleDocTemplate(str(filepath), pagesize=A4)
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.darkblue
            )
            
            story.append(Paragraph(f"PlanB Motoru Günlük Rapor", title_style))
            story.append(Paragraph(f"Tarih: {date.strftime('%d.%m.%Y')}", self.styles['Heading2']))
            story.append(Spacer(1, 20))
            
            # Signal Summary
            story.append(Paragraph("Sinyal Özeti", self.styles['Heading2']))
            
            if report_data.get('signals'):
                signal_data = []
                signal_data.append(['Sinyal', 'Sayı', 'Onay Oranı'])
                
                for signal in report_data['signals']:
                    approval_rate = 0
                    if signal.get('total_signals', 0) > 0:
                        approval_rate = (signal.get('approved', 0) / signal['total_signals']) * 100
                    
                    signal_data.append([
                        signal.get('signal', 'N/A'),
                        str(signal.get('signal_count', 0)),
                        f"{approval_rate:.1f}%"
                    ])
                
                signal_table = Table(signal_data)
                signal_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(signal_table)
                story.append(Spacer(1, 20))
            
            # Trading Performance
            if report_data.get('trading'):
                trading = report_data['trading']
                story.append(Paragraph("İşlem Performansı", self.styles['Heading2']))
                
                trading_data = [
                    ['Metrik', 'Değer'],
                    ['Toplam İşlem', str(trading.get('total_trades', 0))],
                    ['Kazançlı İşlem', str(trading.get('winning_trades', 0))],
                    ['Toplam P&L', f"{trading.get('total_profit_loss', 0):.2f} TL"],
                    ['Ortalama P&L', f"{trading.get('avg_profit_loss', 0):.2f} TL"],
                    ['En Yüksek Kazanç', f"{trading.get('max_profit', 0):.2f} TL"],
                    ['En Yüksek Kayıp', f"{trading.get('max_loss', 0):.2f} TL"]
                ]
                
                trading_table = Table(trading_data)
                trading_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(trading_table)
                story.append(Spacer(1, 20))
            
            # Model Performance
            if report_data.get('models'):
                story.append(Paragraph("Modül Performansları", self.styles['Heading2']))
                
                model_data = [['Modül', 'Tahmin Sayısı', 'Ortalama Güven', 'Yüksek Güven Sayısı']]
                
                for model in report_data['models']:
                    model_data.append([
                        model.get('module_name', 'N/A'),
                        str(model.get('predictions', 0)),
                        f"{model.get('avg_confidence', 0):.1f}%",
                        str(model.get('high_confidence', 0))
                    ])
                
                model_table = Table(model_data)
                model_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(model_table)
            
            # Footer
            story.append(Spacer(1, 30))
            footer_text = f"Rapor oluşturulma zamanı: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
            story.append(Paragraph(footer_text, self.styles['Normal']))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"Daily PDF report generated: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"PDF generation error: {e}")
            return None

class ExcelTaxReporter:
    """Excel vergi raporu oluşturucu"""
    
    def __init__(self, output_dir: str = "/app/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_tax_report(self, start_date: datetime.date, end_date: datetime.date) -> Optional[str]:
        """Vergi raporu Excel dosyası oluştur"""
        try:
            # Database'den işlem verilerini al
            db_url = os.getenv('DATABASE_URL')
            
            with psycopg2.connect(db_url) as conn:
                # Trading performance data
                df_trades = pd.read_sql("""
                    SELECT 
                        entry_timestamp::date as trade_date,
                        symbol,
                        entry_price,
                        exit_price,
                        quantity,
                        profit_loss,
                        profit_loss_percentage,
                        commission,
                        entry_signal,
                        exit_signal
                    FROM trading_performance 
                    WHERE entry_timestamp::date BETWEEN %s AND %s
                    AND exit_timestamp IS NOT NULL
                    ORDER BY entry_timestamp
                """, conn, params=[start_date, end_date])
                
                if df_trades.empty:
                    logger.warning("No trading data found for tax report")
                    return None
                
                # Calculate tax fields
                df_trades['gross_profit'] = df_trades['profit_loss'] + df_trades['commission']
                df_trades['net_profit'] = df_trades['profit_loss']
                df_trades['is_profit'] = df_trades['net_profit'] > 0
                df_trades['is_loss'] = df_trades['net_profit'] < 0
                
                # Summary calculations
                total_trades = len(df_trades)
                total_profit = df_trades[df_trades['is_profit']]['net_profit'].sum()
                total_loss = abs(df_trades[df_trades['is_loss']]['net_profit'].sum())
                net_result = total_profit - total_loss
                total_commission = df_trades['commission'].sum()
                
                # Create Excel file
                filename = f"planb_tax_report_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.xlsx"
                filepath = self.output_dir / filename
                
                with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                    # Trade details sheet
                    df_trades.to_excel(writer, sheet_name='İşlem Detayları', index=False)
                    
                    # Summary sheet
                    summary_data = {
                        'Metrik': [
                            'Dönem',
                            'Toplam İşlem Sayısı',
                            'Kazançlı İşlem Sayısı',
                            'Zararlı İşlem Sayısı',
                            'Toplam Kazanç (TL)',
                            'Toplam Zarar (TL)',
                            'Net Sonuç (TL)',
                            'Toplam Komisyon (TL)',
                            'Vergi Matrahı (TL)',
                            'Tahmini Vergi (%10)',
                            'Net Kazanç (Vergi Sonrası)'
                        ],
                        'Değer': [
                            f"{start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}",
                            total_trades,
                            len(df_trades[df_trades['is_profit']]),
                            len(df_trades[df_trades['is_loss']]),
                            f"{total_profit:.2f}",
                            f"{total_loss:.2f}",
                            f"{net_result:.2f}",
                            f"{total_commission:.2f}",
                            f"{max(net_result, 0):.2f}",
                            f"{max(net_result, 0) * 0.10:.2f}",
                            f"{net_result - max(net_result, 0) * 0.10:.2f}"
                        ]
                    }
                    
                    df_summary = pd.DataFrame(summary_data)
                    df_summary.to_excel(writer, sheet_name='Özet', index=False)
                    
                    # Monthly breakdown
                    df_trades['month'] = pd.to_datetime(df_trades['trade_date']).dt.to_period('M')
                    monthly_summary = df_trades.groupby('month').agg({
                        'symbol': 'count',
                        'profit_loss': ['sum', 'mean'],
                        'commission': 'sum'
                    }).round(2)
                    
                    monthly_summary.columns = ['İşlem Sayısı', 'Toplam P&L', 'Ortalama P&L', 'Toplam Komisyon']
                    monthly_summary.to_excel(writer, sheet_name='Aylık Özet')
                
                logger.info(f"Tax report generated: {filepath}")
                return str(filepath)
                
        except Exception as e:
            logger.error(f"Excel tax report generation error: {e}")
            return None

class ReportScheduler:
    """Rapor zamanlayıcısı"""
    
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL')
        self.db_reporter = DatabaseReporter(self.db_url) if self.db_url else None
        self.pdf_generator = PDFReportGenerator()
        self.excel_reporter = ExcelTaxReporter()
    
    async def generate_daily_report(self, target_date: datetime.date = None):
        """Günlük rapor oluştur"""
        if not self.db_reporter:
            logger.error("Database connection not available")
            return
            
        if target_date is None:
            target_date = datetime.now().date() - timedelta(days=1)  # Yesterday
        
        try:
            logger.info(f"Generating daily report for {target_date}")
            
            # Get report data
            report_data = self.db_reporter.get_daily_summary(target_date)
            
            if not report_data:
                logger.warning(f"No data found for {target_date}")
                return
            
            # Generate PDF report
            pdf_path = self.pdf_generator.generate_daily_report(report_data)
            
            if pdf_path:
                logger.info(f"Daily report generated successfully: {pdf_path}")
            else:
                logger.warning("Daily report generation failed")
                
        except Exception as e:
            logger.error(f"Daily report generation error: {e}")
    
    async def generate_weekly_report(self):
        """Haftalık rapor oluştur"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        try:
            logger.info(f"Generating weekly report for {start_date} to {end_date}")
            
            # User decision analysis
            decision_data = self.db_reporter.get_user_decision_analysis(start_date, end_date)
            
            # Generate tax report (Excel)
            excel_path = self.excel_reporter.generate_tax_report(start_date, end_date)
            
            if excel_path:
                logger.info(f"Weekly Excel report generated: {excel_path}")
            
        except Exception as e:
            logger.error(f"Weekly report generation error: {e}")
    
    async def generate_monthly_report(self):
        """Aylık vergi raporu oluştur"""
        now = datetime.now()
        # Previous month
        if now.month == 1:
            start_date = datetime(now.year - 1, 12, 1).date()
            end_date = datetime(now.year, 1, 1).date() - timedelta(days=1)
        else:
            start_date = datetime(now.year, now.month - 1, 1).date()
            end_date = datetime(now.year, now.month, 1).date() - timedelta(days=1)
        
        try:
            logger.info(f"Generating monthly tax report for {start_date} to {end_date}")
            
            excel_path = self.excel_reporter.generate_tax_report(start_date, end_date)
            
            if excel_path:
                logger.info(f"Monthly tax report generated: {excel_path}")
                
        except Exception as e:
            logger.error(f"Monthly report generation error: {e}")

async def main():
    """Main reporting function"""
    scheduler = ReportScheduler()
    
    # Command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "daily":
            await scheduler.generate_daily_report()
        elif command == "weekly":
            await scheduler.generate_weekly_report()
        elif command == "monthly":
            await scheduler.generate_monthly_report()
        elif command == "test":
            # Test report with current date
            await scheduler.generate_daily_report(datetime.now().date())
        else:
            print("Usage: python reporting_system.py [daily|weekly|monthly|test]")
    else:
        # Default: generate daily report
        await scheduler.generate_daily_report()

if __name__ == "__main__":
    asyncio.run(main())
