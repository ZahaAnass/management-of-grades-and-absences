import csv
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def calculate_average(notes):
    if not notes:
        return None
    return round(sum(notes) / len(notes), 2)

def attendance_rate(total_days, absences):
    if total_days == 0:
        return 100.0
    attended = total_days - absences
    return round((attended / total_days) * 100, 2)

# def filter_students(students, query=None, classe=None):
#     filtered = students
#     if query:
#         filtered = [s for s in filtered if query.lower() in (s['nom'] + ' ' + s['prenom']).lower()]
#     if classe:
#         filtered = [s for s in filtered if s['classe'] == classe]
#     return filtered

def export_csv(data, filename):
    if not data or not isinstance(data, list) or not isinstance(data[0], dict):
        return False    
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    return True

def export_pdf(data, filename, title="Exported Data"):
    if not data:
        return False

    headers = list(data[0].keys()) # To Get Titles of Heading of TreeView
    rows = [headers] + [list(row.values()) for row in data] # To Get Values of TreeView 

    pdf = SimpleDocTemplate(filename, pagesize=landscape(letter))
    table = Table(rows)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12), # Add bottom padding to header row (12 points)
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph(title, styles['Title']))
    elements.append(Spacer(1, 12)) # Add a spacer (12 points high) after the title
    elements.append(table)
    pdf.build(elements)
    return True