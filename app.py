from tkinter import *
from view import GradeManagement
import database

# Initialisation de la base de données
database.create_table()

# Start the app
if __name__ == "__main__":
    window = Tk()
    my_app = GradeManagement(window)
    window.mainloop()
