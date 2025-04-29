import sqlite3

def create_table():
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("""create table if not exists eleves (
        id integer primary key autoincrement,
        nom text not null,
        prenom text not null,
        classe text not null
    )""")
    cursor.execute("""create table if not exists notes (
        id integer primary key autoincrement,
        eleve_id integer not null,
        matiere text not null,
        note real not null,
        date_note date default current_date,
        foreign key (eleve_id) references eleves (id)
    )""")
    cursor.execute("""create table if not exists absences (
        id integer primary key autoincrement,
        eleve_id integer not null,
        date_absence date not null,
        nb_jours integer not null,
        foreign key (eleve_id) references eleves (id)
    )""")
    conn.commit()
    conn.close()

def show_table():
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT
                        e.id,
                        e.nom,
                        e.prenom,
                        e.classe,
                        (SELECT avg(note) FROM notes WHERE eleve_id = e.id) as moyenne,
                        (SELECT sum(nb_jours) FROM absences WHERE eleve_id = e.id) as absences,
                        ROUND(100.0 * (30 - IFNULL((SELECT sum(nb_jours) FROM absences WHERE eleve_id = e.id), 0)) / 30, 2) as taux_assiduite
                    FROM eleves as e
                """)
    data = cursor.fetchall()
    conn.close()
    return data

def add_eleve(nom, prenom, classe):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO eleves (nom, prenom, classe) VALUES (?, ?, ?)", (nom, prenom, classe))
    conn.commit()
    conn.close()

def update_eleve(eleve_id, nom, prenom, classe):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE eleves SET nom=?, prenom=?, classe=? WHERE id=?", (nom, prenom, classe, eleve_id))
    conn.commit()
    conn.close()

def delete_eleve(eleve_id):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM eleves WHERE id=?", (eleve_id,))
    conn.commit()
    conn.close()

def get_eleves():
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, prenom, classe FROM eleves")
    data = cursor.fetchall()
    conn.close()
    return data

def add_notes(eleve_id, matiere, note):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (eleve_id, matiere, note) VALUES (?, ?, ?)", (eleve_id, matiere, note))
    conn.commit()
    conn.close()

def get_notes(eleve_id):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id ,matiere, note, date_note FROM notes WHERE eleve_id=? ORDER BY date_note DESC", (eleve_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def get_note_by_id(note_id):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id=?", (note_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def update_note(note_id, eleve_id, note):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET note=?, eleve_id=? WHERE id=?", (note, eleve_id, note_id))
    conn.commit()
    conn.close()

def delete_note(note_id):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

def add_absence(eleve_id, date_absence, nb_jours):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO absences (eleve_id, date_absence, nb_jours) VALUES (?, ?, ?)", (eleve_id, date_absence, nb_jours))
    conn.commit()
    conn.close()

def get_absences(eleve_id):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT id, nb_jours, date_absence FROM absences WHERE eleve_id=? ORDER BY date_absence DESC""", (eleve_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def get_absence_by_id(absence_id):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT eleve_id, date_absence, nb_jours FROM absences WHERE id=?", (absence_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def delete_absence(absence_id):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM absences WHERE id=?", (absence_id,))
    conn.commit()
    conn.close()

def modify_absence(absence_id, date_absence, nb_jours):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE absences SET date_absence=?, nb_jours=? WHERE id=?", (date_absence, nb_jours, absence_id))
    conn.commit()
    conn.close()

def get_classes():
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT classe FROM eleves")
    data = cursor.fetchall()
    conn.close()
    return [row[0] for row in data] # Cause this data is an tuple We Need To Get The Value At Index 0

def init_sample_data():
    import random
    from datetime import datetime, timedelta
    if not get_eleves():
        first_names = ["Alice", "Lucas", "Emma", "Hugo", "Léa", "Louis", "Chloé", "Gabriel", "Manon", "Nathan"]
        last_names = ["Dupont", "Martin", "Bernard", "Petit", "Durand", "Leroy", "Moreau", "Simon", "Laurent", "Lefebvre"]
        classes = ["6A", "6B", "5A", "5B", "4A", "4B", "3A", "3B"]
        subjects = ["Maths", "Français", "Anglais", "Histoire", "SVT", "Physique"]
        # Insert 50 students
        for _ in range(50):
            nom = random.choice(last_names)
            prenom = random.choice(first_names)
            classe = random.choice(classes)
            add_eleve(nom, prenom, classe)
        eleves = get_eleves()
        for eleve in eleves:
            eleve_id = eleve[0] if isinstance(eleve, (list, tuple)) and len(eleve) > 0 else eleve
            # Add 3-5 notes per student
            for _ in range(random.randint(3, 5)):
                matiere = random.choice(subjects)
                note = round(random.uniform(8, 20), 2)
                add_notes(eleve_id, matiere, note)
            # Add 0-2 absences per student
            for _ in range(random.randint(0, 2)):
                days_ago = random.randint(1, 60)
                date_absence = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
                nb_jours = random.randint(1, 3)
                add_absence(eleve_id, date_absence, nb_jours)
        print('50 record added')

create_table()
init_sample_data()