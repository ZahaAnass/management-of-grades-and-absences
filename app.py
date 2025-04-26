from tkinter import *
from view import GestionNotesAbsencesApp
import database

# Initialisation de la base de données
database.create_table()

# Start the app
if __name__ == "__main__":
    my_app = GestionNotesAbsencesApp()
    my_app.mainloop()
