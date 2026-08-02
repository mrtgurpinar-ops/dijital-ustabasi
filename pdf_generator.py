import os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Font Resolution for Turkish Character Support
DEFAULT_FONT = "Helvetica"
DEFAULT_FONT_BOLD = "Helvetica-Bold"

def register_turkish_fonts():
    global DEFAULT_FONT, DEFAULT_FONT_BOLD
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_paths = [
        # Bundled Fonts (Priority)
        (os.path.join(base_dir, "static", "fonts", "Arial.ttf"), os.path.join(base_dir, "static", "fonts", "Arial-Bold.ttf"), "Arial", "Arial-Bold"),
        # Windows
        ("C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\arialbd.ttf", "Arial", "Arial-Bold"),
        ("C:\\Windows\\Fonts\\tahoma.ttf", "C:\\Windows\\Fonts\\tahomabd.ttf", "Tahoma", "Tahoma-Bold"),
        # Linux
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVuSans", "DejaVuSans-Bold"),
        ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", "LiberationSans", "LiberationSans-Bold"),
        # macOS
        ("/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf", "Arial", "Arial-Bold"),
    ]
    
    for reg_path, bold_path, name, bold_name in font_paths:
        if os.path.exists(reg_path):
            try:
                pdfmetrics.registerFont(TTFont(name, reg_path))
                if os.path.exists(bold_path):
                    pdfmetrics.registerFont(TTFont(bold_name, bold_path))
                    DEFAULT_FONT_BOLD = bold_name
                else:
                    DEFAULT_FONT_BOLD = name
                DEFAULT_FONT = name
                print(f"[Info] Registered font {name} for Turkish support.")
                return True
            except Exception as e:
                print(f"[Warning] Failed to register font {name}: {e}")
    print("[Warning] No system font found for Turkish support. Falling back to Helvetica.")
    return False


# Register fonts on import
register_turkish_fonts()

def generate_quote_pdf(shop_name, phone_number, plaka, vehicle, items, output_path, validity_days=7, custom_note=None):
    """
    Generates a premium corporate Quote PDF with ReportLab.
    """
    # Initialize document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    story = []
    
    # Setup Styles
    styles = getSampleStyleSheet()
    
    # Custom Styles using registered font
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName=DEFAULT_FONT_BOLD,
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1a365d"),
        spaceAfter=5
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName=DEFAULT_FONT,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4a5568"),
        spaceAfter=15
    )
    
    section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName=DEFAULT_FONT_BOLD,
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2b6cb0"),
        spaceAfter=8,
        spaceBefore=10
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName=DEFAULT_FONT,
        fontSize=9,
        textColor=colors.HexColor("#2d3748"),
        leading=13
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName=DEFAULT_FONT_BOLD
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName=DEFAULT_FONT_BOLD,
        fontSize=9,
        textColor=colors.white,
        alignment=0 # Left
    )

    table_header_right = ParagraphStyle(
        'TableHeaderRight',
        parent=table_header_style,
        alignment=2 # Right
    )

    table_body_style = ParagraphStyle(
        'TableBody',
        parent=body_style,
        fontSize=9
    )

    table_body_right = ParagraphStyle(
        'TableBodyRight',
        parent=body_style,
        fontSize=9,
        alignment=2 # Right
    )

    # 1. Header (Shop Name and Doc Type)
    header_data = [
        [
            Paragraph(shop_name.upper(), title_style),
            Paragraph("FİYAT TEKLİFİ", ParagraphStyle('RightTitle', parent=title_style, alignment=2))
        ],
        [
            Paragraph(f"Telefon: {phone_number} | Bulut Depolama Arayüzü", subtitle_style),
            Paragraph(f"Tarih: {datetime.now().strftime('%d.%m.%Y')} | No: {datetime.now().strftime('%y%m%d%H%M')}", ParagraphStyle('RightSub', parent=subtitle_style, alignment=2))
        ]
    ]
    header_table = Table(header_data, colWidths=[250, 260])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    
    # Divider Line
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2b6cb0"), spaceAfter=15, spaceBefore=5))
    
    # 2. Vehicle & Quote Info Block
    info_data = [
        [
            Paragraph("<b>ARAÇ BİLGİLERİ</b>", body_bold),
            Paragraph("<b>TEKLİF BİLGİLERİ</b>", body_bold)
        ],
        [
            Paragraph(f"Plaka: <b>{plaka.upper()}</b>", body_style),
            Paragraph(f"Geçerlilik Süresi: <b>{validity_days} Gün</b>", body_style)
        ],
        [
            Paragraph(f"Araç: <b>{vehicle}</b>", body_style),
            Paragraph(f"Geçerlilik Tarihi: <b>{(datetime.now() + timedelta(days=validity_days)).strftime('%d.%m.%Y')}</b>", body_style)
        ]
    ]
    info_table = Table(info_data, colWidths=[255, 255])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#ebf8ff")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 15))
    
    # 3. Repair/Part Details Table
    table_data = [
        [
            Paragraph("Sıra", table_header_style), 
            Paragraph("Yapılan İşlem / Değişen Parça", table_header_style), 
            Paragraph("Fiyat (KDV Hariç)", table_header_right)
        ]
    ]
    
    subtotal = 0.0
    for idx, item in enumerate(items, 1):
        price = float(item.get("price", 0))
        subtotal += price
        table_data.append([
            Paragraph(str(idx), table_body_style),
            Paragraph(item.get("description", "Tamir/Parça Hizmeti"), table_body_style),
            Paragraph(f"{price:,.2f} TL", table_body_right)
        ])
        
    details_table = Table(table_data, colWidths=[40, 350, 120])
    details_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2b6cb0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f7fafc")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e0")),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 15))
    
    # 4. Totals Block (Subtotal, VAT, Credit Card Total, Cash Discounted Total)
    vat_rate = 0.20 # %20 KDV
    vat_val = subtotal * vat_rate
    total_val = subtotal + vat_val
    discount_rate = 0.10 # %10 Cash Discount
    discount_val = total_val * discount_rate
    cash_total_val = total_val - discount_val
    
    totals_data = [
        [
            Paragraph("", body_style),
            Paragraph("Ara Toplam (KDV Hariç):", body_style),
            Paragraph(f"{subtotal:,.2f} TL", ParagraphStyle('SubR', parent=body_style, alignment=2))
        ],
        [
            Paragraph("", body_style),
            Paragraph("KDV (%20):", body_style),
            Paragraph(f"{vat_val:,.2f} TL", ParagraphStyle('VatR', parent=body_style, alignment=2))
        ],
        [
            Paragraph("", body_style),
            Paragraph("<b>Genel Toplam (Kredi Kartı):</b>", body_bold),
            Paragraph(f"<b>{total_val:,.2f} TL</b>", ParagraphStyle('TotR', parent=body_bold, alignment=2))
        ],
        [
            Paragraph("", body_style),
            Paragraph("<font color='#2f855a'><b>Nakit Ödeme İndirimi (%10):</b></font>", body_style),
            Paragraph(f"<font color='#2f855a'>-{discount_val:,.2f} TL</font>", ParagraphStyle('DiscR', parent=body_style, alignment=2))
        ],
        [
            Paragraph("", body_style),
            Paragraph("<font color='#2f855a'><b>Nakit Ödemede Toplam Tutar:</b></font>", ParagraphStyle('CashBold', parent=body_bold, textColor=colors.HexColor("#2f855a"))),
            Paragraph(f"<b>{cash_total_val:,.2f} TL</b>", ParagraphStyle('CashTotR', parent=body_bold, alignment=2, textColor=colors.HexColor("#2f855a")))
        ]
    ]
    
    totals_table = Table(totals_data, colWidths=[260, 130, 120])
    totals_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (1,0), (2,0), 0.5, colors.HexColor("#cbd5e0")),
        ('LINEBELOW', (1,1), (2,1), 0.5, colors.HexColor("#cbd5e0")),
        ('LINEBELOW', (1,2), (2,2), 1, colors.HexColor("#1a365d")),
        ('BACKGROUND', (1,4), (2,4), colors.HexColor("#f0fff4")), # Light green background for cash total
        ('BOX', (1,4), (2,4), 1, colors.HexColor("#c6f6d5")),
        ('TOPPADDING', (1,4), (2,4), 6),
        ('BOTTOMPADDING', (1,4), (2,4), 6),
    ]))
    story.append(totals_table)
    story.append(Spacer(1, 20))
    
    # 5. Terms & Usta Note Block
    terms_text = f"• Bu teklif, teklif tarihinden itibaren <b>{validity_days} gün</b> geçerlidir."
    if custom_note:
        note_content = f"• <b>Usta Notu:</b> {custom_note}"
    else:
        note_content = "• <b>Usta Notu:</b> Yedek parça fiyatları kur kaynaklı değişkenlik gösterebilir. Lütfen onay veriniz."
        
    terms_data = [
        [Paragraph("<b>AÇIKLAMALAR & NOTLAR</b>", body_bold)],
        [Paragraph(terms_text, body_style)],
        [Paragraph(note_content, body_style)],
        [Paragraph("• Nakit ödemelerde KDV sonrası %10 indirim uygulanmaktadır.", ParagraphStyle('CashNote', parent=body_style, textColor=colors.HexColor("#2f855a")))]
    ]
    terms_table = Table(terms_data, colWidths=[510])
    terms_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(terms_table)
    
    # Footer disclaimer
    story.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontName=DEFAULT_FONT,
        fontSize=8,
        textColor=colors.HexColor("#a0aec0"),
        alignment=1 # Center
    )
    story.append(Paragraph("Bu belge Dijital Ustabaşı Bulut Platformu tarafından otomatik oluşturulmuştur.", footer_style))
    
    # Build Document
    doc.build(story)
    
    return subtotal, vat_val, total_val, cash_total_val
