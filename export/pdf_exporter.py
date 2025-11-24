import logging
from datetime import datetime
from io import BytesIO
from typing import Dict

logger = logging.getLogger(__name__)


class PDFExporter:
    def __init__(self):
        self.reportlab_available = False
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            self.reportlab_available = True
            logger.info("ReportLab available for PDF export")
        except ImportError:
            logger.warning("ReportLab not available")
    
    def export(self, plan: Dict, filename: str = None) -> BytesIO:
        if not self.reportlab_available:
            logger.error("ReportLab not installed")
            raise ImportError("ReportLab required for PDF export")
        
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        
        buffer = BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        
        story = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('
            spaceAfter=30,
            alignment=TA_CENTER,
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('
            spaceAfter=12,
            spaceBefore=12,
        )
        
        company_name = plan['metadata']['company_name']
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph("ACCOUNT PLAN", title_style))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(company_name, title_style))
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            styles['Normal']
        ))
        story.append(PageBreak())
        
        for section_name, section in plan['sections'].items():
            story.append(Paragraph(section['title'], heading_style))
            story.append(Spacer(1, 0.2*inch))
            
            content = section['content']
            if isinstance(content, dict):
                for key, value in content.items():
                    key_formatted = key.replace('_', ' ').title()
                    story.append(Paragraph(f"<b>{key_formatted}:</b>", styles['Normal']))
                    
                    if isinstance(value, list):
                        for item in value:
                            story.append(Paragraph(f"• {item}", styles['Normal']))
                    else:
                        story.append(Paragraph(str(value), styles['Normal']))
                    
                    story.append(Spacer(1, 0.1*inch))
            
            story.append(Spacer(1, 0.3*inch))
        
        doc.build(story)
        buffer.seek(0)
        
        return buffer
