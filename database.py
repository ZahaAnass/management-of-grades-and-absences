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
                        ROUND(100.0 * (200 - IFNULL((SELECT sum(nb_jours) FROM absences WHERE eleve_id = e.id), 0)) / 200, 2) as taux_assiduite
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

def add_note(eleve_id, matiere, note):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (eleve_id, matiere, note) VALUES (?, ?, ?)", (eleve_id, matiere, note))
    conn.commit()
    conn.close()

def get_notes(eleve_id):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT matiere, note, date_note FROM notes WHERE eleve_id=? ORDER BY date_note DESC", (eleve_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def update_note(note_id, note):
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET note=? WHERE id=?", (note, note_id))
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
    cursor.execute("SELECT date_absence, nb_jours FROM absences WHERE eleve_id=? ORDER BY date_absence DESC", (eleve_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def init_sample_data():
    if not get_eleves():
        add_eleve("Dupont", "Alice", "6A")
        add_eleve("Martin", "Lucas", "5B")
        add_note(1, "Maths", 17)
        add_note(1, "Français", 14)
        add_note(2, "Maths", 13)
        add_absence(1, "2024-04-08", 1)
        add_absence(2, "2024-04-15", 2)

create_table()
init_sample_data()