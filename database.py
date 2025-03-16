import sqlite3

def create_table():
    conn = sqlite3.connect("grademanagement.db")
    cursor = conn.cursor()
    cursor.execute("""create table if not exists products (
        first_name text primary key,
        last_name text unique not null,
        class text not null,
        average real not null,
        nbr_absences integer not null,
        attendance_rate real not null
    )""")
    conn.commit()
    conn.close()
