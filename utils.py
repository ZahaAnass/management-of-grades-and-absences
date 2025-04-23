# utils.py
# Utility functions for Gestion des Notes et Absences Scolaires (UI-only)

def calculate_average(notes):
    """
    notes: list of floats or ints
    Returns the average or None if empty.
    """
    if not notes:
        return None
    return round(sum(notes) / len(notes), 2)

def attendance_rate(total_days, absences):
    """
    Returns the attendance rate as a percentage (0-100).
    """
    if total_days == 0:
        return 100.0
    attended = total_days - absences
    return round((attended / total_days) * 100, 2)

def filter_students(students, query=None, classe=None):
    """
    Filter students by name or class.
    students: list of dicts with keys 'nom', 'prenom', 'classe'
    """
    filtered = students
    if query:
        filtered = [s for s in filtered if query.lower() in (s['nom'] + ' ' + s['prenom']).lower()]
    if classe:
        filtered = [s for s in filtered if s['classe'] == classe]
    return filtered

def export_csv(data, filename):
    """
    Export data (list of dicts) to CSV file.
    """
    import csv
    if not data:
        return False
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    return True

# PDF export stub (can be implemented with reportlab, left as a stub)
def export_pdf(data, filename):
    # Stub: Not implemented
    return False