import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.font as tkFont
import database as db
from utils import *

# Colors and styling constants for theme
COLORS = {
    'primary': '#3f51b5',     # Indigo
    'primary_light': '#757de8', # Lighter Indigo
    'primary_dark': '#002984', # Darker Indigo
    'secondary': '#ff4081',   # Pink
    'background': '#f5f5f5',  # Light grey
    'card': '#ffffff',        # White
    'text': '#212121',        # Dark text
    'text_secondary': '#757575', # Grey text
    'success': '#4caf50',     # Green
    'warning': '#ff9800',     # Orange
    'error': '#f44336',       # Red
    'button_text': '#ffffff'  # White
}

class EleveForm(tk.Toplevel):
    def __init__(self, parent, eleve_id=None):
        super().__init__(parent)
        self.parent = parent
        self.eleve_id = eleve_id
        self.title("Ajouter un élève" if eleve_id is None else "Modifier un élève")
        self.geometry("500x400")
        self.configure(bg=COLORS['background'])
        self.setup_fonts()
        self.setup_style()
        self.create_widgets()
        self.center_window()
        self.transient(parent)
        self.grab_set()
        
        # Load data if editing
        if eleve_id is not None:
            self.load_student_data()

    def setup_fonts(self):
        self.title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        self.normal_font = tkFont.Font(family="Helvetica", size=11)
        self.button_font = tkFont.Font(family="Helvetica", size=11, weight="bold")

    def setup_style(self):
        style = ttk.Style(self)
        style.configure('TFrame', background=COLORS['background'])
        style.configure('Card.TFrame', background=COLORS['card'])
        style.configure('TLabel', background=COLORS['card'], foreground=COLORS['text'], font=self.normal_font)
        style.configure('Title.TLabel', background=COLORS['card'], foreground=COLORS['primary'], font=self.title_font)
        style.configure('TEntry', font=self.normal_font)
        
        # Button styles
        style.configure('Primary.TButton', 
                        background=COLORS['primary'],
                        foreground=COLORS['button_text'],
                        font=self.button_font)
        style.map('Primary.TButton',
                background=[('active', COLORS['primary_light'])])
        
        style.configure('Secondary.TButton', 
                        background=COLORS['secondary'],
                        foreground=COLORS['button_text'],
                        font=self.button_font)
        style.map('Secondary.TButton',
                    background=[('active', COLORS['secondary'])])

    def create_widgets(self):
        main_frame = ttk.Frame(self, style='Card.TFrame', padding=20)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_text = "Ajouter un nouvel élève" if self.eleve_id is None else "Modifier les informations de l'élève"
        ttk.Label(main_frame, text=title_text, style='Title.TLabel').pack(pady=(0, 20))
        
        # Form fields
        form_frame = ttk.Frame(main_frame, style='Card.TFrame')
        form_frame.pack(fill='both', expand=True, pady=10)
        
        # Nom
        ttk.Label(form_frame, text="Nom:", style='TLabel').grid(row=0, column=0, sticky='w', padx=5, pady=10)
        self.nom_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.nom_var, width=30, font=self.normal_font).grid(row=0, column=1, padx=5, pady=10)
        
        # Prénom
        ttk.Label(form_frame, text="Prénom:", style='TLabel').grid(row=1, column=0, sticky='w', padx=5, pady=10)
        self.prenom_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.prenom_var, width=30, font=self.normal_font).grid(row=1, column=1, padx=5, pady=10)
        
        # Classe
        ttk.Label(form_frame, text="Classe:", style='TLabel').grid(row=2, column=0, sticky='w', padx=5, pady=10)
        self.classe_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.classe_var, width=30, font=self.normal_font).grid(row=2, column=1, padx=5, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(main_frame, style='Card.TFrame')
        button_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(button_frame, text="Annuler", command=self.destroy, style='Secondary.TButton').pack(side='right', padx=5)
        save_text = "Ajouter" if self.eleve_id is None else "Enregistrer"
        ttk.Button(button_frame, text=save_text, command=self.save_student, style='Primary.TButton').pack(side='right', padx=5)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def load_student_data(self):
        if self.eleve_id:
            eleves = db.get_eleves()
            for eleve in eleves:
                if eleve[0] == self.eleve_id:
                    self.nom_var.set(eleve[1])
                    self.prenom_var.set(eleve[2])
                    self.classe_var.set(eleve[3])
                    break

    def save_student(self):
        nom = self.nom_var.get()
        prenom = self.prenom_var.get()
        classe = self.classe_var.get()
        
        if not (nom and prenom and classe):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires", parent=self)
            return
        
        if self.eleve_id is None:
            db.add_eleve(nom, prenom, classe)
        else:
            db.update_eleve(self.eleve_id, nom, prenom, classe)

        self.parent.refresh_table()
        self.destroy()


class NoteForm(tk.Toplevel):
    def __init__(self, parent, note_id=None):
        super().__init__(parent)
        self.parent = parent
        self.note_id = note_id
        
        self.title("Ajouter une note" if note_id is None else "Modifier une note")
        self.geometry("500x400")
        self.configure(bg=COLORS['background'])
        self.setup_fonts()
        self.setup_style()
        self.create_widgets()
        self.center_window()
        self.transient(parent)
        self.grab_set()
        
        # Load data if editing mode
        if note_id is not None:
            self.load_note_data()

    def setup_fonts(self):
        self.title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        self.normal_font = tkFont.Font(family="Helvetica", size=11)
        self.button_font = tkFont.Font(family="Helvetica", size=11, weight="bold")

    def setup_style(self):
        style = ttk.Style(self)
        style.configure('TFrame', background=COLORS['background'])
        style.configure('Card.TFrame', background=COLORS['card'])
        style.configure('TLabel', background=COLORS['card'], foreground=COLORS['text'], font=self.normal_font)
        style.configure('Title.TLabel', background=COLORS['card'], foreground=COLORS['primary'], font=self.title_font)
        style.configure('TEntry', font=self.normal_font)
        style.configure('TCombobox', font=self.normal_font)
        
        # Button styles
        style.configure('Primary.TButton', 
                            background=COLORS['primary'],
                            foreground=COLORS['button_text'],
                            font=self.button_font)
        style.map('Primary.TButton',
                    background=[('active', COLORS['primary_light'])])
        
        style.configure('Secondary.TButton', 
                            background=COLORS['secondary'],
                            foreground=COLORS['button_text'],
                            font=self.button_font)
        style.map('Secondary.TButton',
                    background=[('active', COLORS['secondary'])])

    def create_widgets(self):
        main_frame = ttk.Frame(self, style='Card.TFrame', padding=20)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_text = "Ajouter une note" if self.note_id is None else "Modifier une note"
        ttk.Label(main_frame, text=title_text, style='Title.TLabel').pack(pady=(0, 20))
        
        # Form fields
        form_frame = ttk.Frame(main_frame, style='Card.TFrame')
        form_frame.pack(fill='both', expand=True, pady=10)
        
        # Élève selection
        ttk.Label(form_frame, text="Élève:", style='TLabel').grid(row=0, column=0, sticky='w', padx=5, pady=10)
        self.eleve_combobox = ttk.Combobox(form_frame, width=30, font=self.normal_font, state='readonly')
        self.eleve_combobox.grid(row=0, column=1, padx=5, pady=10)
        self.update_eleve_list()
        
        # Matière
        ttk.Label(form_frame, text="Matière:", style='TLabel').grid(row=1, column=0, sticky='w', padx=5, pady=10)
        self.matiere_var = tk.StringVar()
        self.matiere_entry = ttk.Entry(form_frame, textvariable=self.matiere_var, width=30, font=self.normal_font)
        self.matiere_entry.grid(row=1, column=1, padx=5, pady=10)
        
        # Note
        ttk.Label(form_frame, text="Note:", style='TLabel').grid(row=2, column=0, sticky='w', padx=5, pady=10)
        self.note_var = tk.StringVar()
        self.note_entry = ttk.Entry(form_frame, textvariable=self.note_var, width=10, font=self.normal_font)
        self.note_entry.grid(row=2, column=1, sticky='w', padx=5, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(main_frame, style='Card.TFrame')
        button_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(button_frame, text="Annuler", command=self.destroy, style='Secondary.TButton').pack(side='right', padx=5)
        save_text = "Ajouter" if self.note_id is None else "Modifier"
        ttk.Button(button_frame, text=save_text, command=self.save_note, style='Primary.TButton').pack(side='right', padx=5)

    def update_eleve_list(self):
        eleves = db.get_eleves()
        self.eleve_combobox['values'] = [f"{eleve[2]} {eleve[1]} (ID: {eleve[0]})" for eleve in eleves]

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def load_note_data(self):
        note_data = db.get_note_by_id(self.note_id)
        if note_data:
            eleve_id = note_data[1]
            eleves = db.get_eleves()
            for eleve in eleves:
                if eleve[0] == eleve_id:
                    self.eleve_combobox.set(f"{eleve[2]} {eleve[1]} (ID: {eleve[0]})")
                    self.eleve_combobox.config(state='disabled')
                    break
            self.matiere_var.set(note_data[2])
            self.note_var.set(note_data[3])
            # Make the fields readonly
            self.matiere_entry['state'] = 'readonly'
        else:
            messagebox.showerror("Erreur", "Note non trouvée", parent=self.parent)
            self.destroy()

    def save_note(self):
        if self.eleve_combobox.get() != "" and self.matiere_var.get() != "" and self.note_var.get() != "":
            eleve_id = int(self.eleve_combobox.get().split("(ID: ")[1].split(")")[0])
            matiere = self.matiere_var.get()
            note = self.note_var.get()
            
            if self.note_id is None:
                db.add_notes(eleve_id, matiere, note)
            else:
                db.update_note(self.note_id, eleve_id, note)
            
            self.parent.parent.refresh_table()
            self.destroy()
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs", parent=self)

class AbsenceForm(tk.Toplevel):
    def __init__(self, parent, eleve_id=None):
        super().__init__(parent)
        self.parent = parent
        self.eleve_id = eleve_id
        
        self.title("Enregistrer une absence")
        self.geometry("500x400")
        self.configure(bg=COLORS['background'])
        self.setup_fonts()
        self.setup_style()
        self.create_widgets()
        self.center_window()
        self.transient(parent)
        self.grab_set()

    def setup_fonts(self):
        self.title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        self.normal_font = tkFont.Font(family="Helvetica", size=11)
        self.button_font = tkFont.Font(family="Helvetica", size=11, weight="bold")

    def setup_style(self):
        style = ttk.Style(self)
        style.configure('TFrame', background=COLORS['background'])
        style.configure('Card.TFrame', background=COLORS['card'])
        style.configure('TLabel', background=COLORS['card'], foreground=COLORS['text'], font=self.normal_font)
        style.configure('Title.TLabel', background=COLORS['card'], foreground=COLORS['primary'], font=self.title_font)
        style.configure('TEntry', font=self.normal_font)
        style.configure('TCombobox', font=self.normal_font)
        
        # Button styles
        style.configure('Primary.TButton', 
                        background=COLORS['primary'],
                        foreground=COLORS['button_text'],
                        font=self.button_font)
        style.map('Primary.TButton',
                    background=[('active', COLORS['primary_light'])])
        
        style.configure('Secondary.TButton', 
                        background=COLORS['secondary'],
                        foreground=COLORS['button_text'],
                        font=self.button_font)
        style.map('Secondary.TButton',
                    background=[('active', COLORS['secondary'])])

    def create_widgets(self):
        main_frame = ttk.Frame(self, style='Card.TFrame', padding=20)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(main_frame, text="Enregistrer une absence", style='Title.TLabel').pack(pady=(0, 20))
        
        # Form fields
        form_frame = ttk.Frame(main_frame, style='Card.TFrame')
        form_frame.pack(fill='both', expand=True, pady=10)
        
        # Élève selection
        ttk.Label(form_frame, text="Élève:", style='TLabel').grid(row=0, column=0, sticky='w', padx=5, pady=10)
        self.eleve_combobox = ttk.Combobox(form_frame, width=30, font=self.normal_font, state='readonly')
        self.eleve_combobox.grid(row=0, column=1, padx=5, pady=10)
        self.update_eleve_list()
        
        # Date
        ttk.Label(form_frame, text="Date (YYYY-MM-DD):", style='TLabel').grid(row=1, column=0, sticky='w', padx=5, pady=10)
        self.date_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.date_var, width=15, font=self.normal_font).grid(row=1, column=1, sticky='w', padx=5, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(main_frame, style='Card.TFrame')
        button_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(button_frame, text="Annuler", command=self.destroy, style='Secondary.TButton').pack(side='right', padx=5)
        ttk.Button(button_frame, text="Enregistrer", command=self.save_absence, style='Primary.TButton').pack(side='right', padx=5)

    def update_eleve_list(self):
        # Placeholder for updating élève list
        pass

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def save_absence(self):
        # Placeholder for saving absence
        print("TODO: save_absence")
        self.destroy()


class GestionNotesAbsencesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des Notes et Absences Scolaires")
        self.geometry("1280x720")
        self.configure(bg=COLORS['background'])
        self.setup_fonts()
        self.setup_style()
        self.create_widgets()
        self.refresh_table()

    def setup_fonts(self):
        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.subtitle_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = tkFont.Font(family="Helvetica", size=11)
        self.button_font = tkFont.Font(family="Helvetica", size=11, weight="bold")

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        
        # Configure common styles
        style.configure('TFrame', background=COLORS['background'])
        style.configure('Card.TFrame', background=COLORS['card'], relief='raised')
        style.configure('TLabel', background=COLORS['card'], foreground=COLORS['text'], font=self.normal_font)
        style.configure('Title.TLabel', background=COLORS['card'], foreground=COLORS['primary'], font=self.title_font)
        style.configure('Subtitle.TLabel', background=COLORS['card'], foreground=COLORS['primary'], font=self.subtitle_font)
        style.configure('TEntry', font=self.normal_font)
        
        # Treeview style
        style.configure('Treeview', 
                        background=COLORS['card'],
                        foreground=COLORS['text'],
                        rowheight=30,
                        fieldbackground=COLORS['card'],
                        font=self.normal_font)
        style.configure('Treeview.Heading', 
                        font=self.subtitle_font,
                        background=COLORS['primary'],
                        foreground=COLORS['button_text'])
        style.map('Treeview.Heading',
                    background=[('active', COLORS['primary_light'])])
        style.map('Treeview',
                    background=[('selected', COLORS['primary_light'])],
                    foreground=[('selected', COLORS['text'])])
        
        # Button styles
        style.configure('Primary.TButton', 
                        background=COLORS['primary'],
                        foreground=COLORS['button_text'],
                        font=self.button_font)
        style.map('Primary.TButton',
                    background=[('active', COLORS['primary_light'])])
        
        style.configure('Secondary.TButton', 
                        background=COLORS['secondary'],
                        foreground=COLORS['button_text'],
                        font=self.button_font)
        style.map('Secondary.TButton',
                    background=[('active', COLORS['secondary'])])
        
        style.configure('Warning.TButton', 
                        background=COLORS['warning'],
                        foreground=COLORS['button_text'],
                        font=self.button_font)
        style.map('Warning.TButton',
                    background=[('active', COLORS['warning'])])
        
        style.configure('Danger.TButton', 
                        background=COLORS['error'],
                        foreground=COLORS['button_text'],
                        font=self.button_font)
        style.map('Danger.TButton',
                    background=[('active', COLORS['error'])])

    def create_widgets(self):
        # Main container with two columns
        main_container = ttk.Frame(self, style='TFrame')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left column for commands (1/3 width)
        self.command_frame = ttk.Frame(main_container, style='TFrame')
        self.command_frame.pack(side='left', fill='both', padx=5, pady=5, expand=False)
        
        # Right column for data display (2/3 width)
        self.display_frame = ttk.Frame(main_container, style='TFrame')
        self.display_frame.pack(side='right', fill='both', padx=5, pady=5, expand=True)
        
        # Create command panels
        self.create_command_panels()
        
        # Create display panels
        self.create_display_panels()

    def create_command_panels(self):
        # Élèves panel
        eleves_panel = ttk.Frame(self.command_frame, style='Card.TFrame')
        eleves_panel.pack(fill='x', padx=5, pady=5, ipady=10)
        
        ttk.Label(eleves_panel, text="Gestion des Élèves", style='Subtitle.TLabel').pack(pady=(10, 15), padx=10)
        
        ttk.Button(eleves_panel, text="Ajouter un élève", 
                    command=lambda: EleveForm(self), 
                    style='Primary.TButton').pack(fill='x', padx=10, pady=5)
        
        ttk.Button(eleves_panel, text="Modifier l'élève sélectionné", 
                  command=self.edit_selected_student, 
                  style='Secondary.TButton').pack(fill='x', padx=10, pady=5)
        
        ttk.Button(eleves_panel, text="Supprimer l'élève sélectionné", 
                  command=self.delete_selected_student, 
                  style='Danger.TButton').pack(fill='x', padx=10, pady=5)
        
        # Notes panel
        notes_panel = ttk.Frame(self.command_frame, style='Card.TFrame')
        notes_panel.pack(fill='x', padx=5, pady=10, ipady=10)
        
        ttk.Label(notes_panel, text="Gestion des Notes", style='Subtitle.TLabel').pack(pady=(10, 15), padx=10)
        
        ttk.Button(notes_panel, text="Ajouter une note", 
                  command=lambda: NoteForm(self), 
                  style='Primary.TButton').pack(fill='x', padx=10, pady=5)
        
        ttk.Button(notes_panel, text="Voir les notes de l'élève", 
                  command=self.view_student_notes, 
                  style='Secondary.TButton').pack(fill='x', padx=10, pady=5)
        
        # Absences panel
        absences_panel = ttk.Frame(self.command_frame, style='Card.TFrame')
        absences_panel.pack(fill='x', padx=5, pady=5, ipady=10)
        
        ttk.Label(absences_panel, text="Gestion des Absences", style='Subtitle.TLabel').pack(pady=(10, 15), padx=10)
        
        ttk.Button(absences_panel, text="Enregistrer une absence", 
                  command=lambda: AbsenceForm(self), 
                  style='Primary.TButton').pack(fill='x', padx=10, pady=5)
        
        ttk.Button(absences_panel, text="Voir les absences de l'élève", 
                  command=self.view_student_absences, 
                  style='Secondary.TButton').pack(fill='x', padx=10, pady=5)

    def create_display_panels(self):
        # Search and filter panel
        filter_panel = ttk.Frame(self.display_frame, style='Card.TFrame')
        filter_panel.pack(fill='x', padx=5, pady=5)
        
        # Top row with title and export buttons
        top_row = ttk.Frame(filter_panel, style='Card.TFrame')
        top_row.pack(fill='x', padx=10, pady=(10, 5))
        
        ttk.Label(top_row, text="Filtres et Recherche", style='Subtitle.TLabel').pack(side='left')
        
        ttk.Button(top_row, text="Exporter PDF", 
                  command=self.export_pdf_ui, 
                  style='Secondary.TButton').pack(side='right', padx=(5, 0))
                  
        ttk.Button(top_row, text="Exporter CSV", 
                  command=self.export_csv_ui, 
                  style='Secondary.TButton').pack(side='right', padx=5)
        
        # Search and filter controls
        controls_frame = ttk.Frame(filter_panel, style='Card.TFrame')
        controls_frame.pack(fill='x', padx=10, pady=(5, 10))
        
        ttk.Label(controls_frame, text="Classe:").pack(side='left', padx=(0, 5))
        self.classe_filter = ttk.Combobox(controls_frame, values=self.get_classes(), width=15, state='readonly')
        self.classe_filter.pack(side='left', padx=5)
        self.classe_filter.bind('<<ComboboxSelected>>', lambda e: self.refresh_table())
        
        ttk.Label(controls_frame, text="Recherche:").pack(side='left', padx=(20, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(controls_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_table())
        
        ttk.Button(controls_frame, text="Réinitialiser", 
                  command=self.reset_filters, 
                  style='Primary.TButton').pack(side='left', padx=20)
        
        # Table panel
        table_panel = ttk.Frame(self.display_frame, style='Card.TFrame')
        table_panel.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create table with scrollbars
        table_frame = ttk.Frame(table_panel, style='Card.TFrame')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame)
        y_scrollbar.pack(side='right', fill='y')
        
        x_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal')
        x_scrollbar.pack(side='bottom', fill='x')
        
        # Table
        columns = ("ID", "Nom", "Prénom", "Classe", "Moyenne", "Absences", "Taux d'Assiduité")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', 
                                yscrollcommand=y_scrollbar.set,
                                xscrollcommand=x_scrollbar.set)
        
        # Configure columns
        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Nom", width=150, anchor='w')
        self.tree.column("Prénom", width=150, anchor='w')
        self.tree.column("Classe", width=100, anchor='center')
        self.tree.column("Moyenne", width=80, anchor='center')
        self.tree.column("Absences", width=80, anchor='center')
        self.tree.column("Taux d'Assiduité", width=120, anchor='center')
        
        # Configure headings
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(self.tree, c, False))
        
        # Pack the table and configure scrollbars
        self.tree.pack(fill='both', expand=True)
        y_scrollbar.config(command=self.tree.yview)
        x_scrollbar.config(command=self.tree.xview)
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_tree_double_click)
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        # Status bar
        status_bar = ttk.Frame(self.display_frame, style='Card.TFrame')
        status_bar.pack(fill='x', padx=5, pady=(0, 5))
        
        self.status_label = ttk.Label(status_bar, text="Prêt", style='TLabel')
        self.status_label.pack(side='left', padx=10, pady=5)
        
        self.count_label = ttk.Label(status_bar, text="0 élèves", style='TLabel')
        self.count_label.pack(side='right', padx=10, pady=5)

    def get_classes(self):
        # Placeholder for getting classes
        return []

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        eleves = db.show_table()
        for eleve in eleves:
            eleve_list = list(eleve)
            if eleve_list:
                eleve_list[-1] = f"{eleve_list[-1]}%"
            self.tree.insert('', 'end', values=tuple(eleve_list))
        self.count_label.config(text=f"{len(eleves)} élèves")

    def reset_filters(self):
        self.classe_filter.set('')
        self.search_var.set('')
        self.refresh_table()

    def on_tree_select(self, event):
        # This is called when a row is selected
        selected = self.tree.selection()
        if selected:
            # Update status bar
            self.status_label.config(text=f"Élève sélectionné: ID {selected[0]}")

    def on_tree_double_click(self, event):
        # This is called when a row is double-clicked
        selected = self.tree.selection()
        if selected:
            self.edit_selected_student()

    def edit_selected_student(self):
        selected = self.tree.selection()
        if selected:
            eleve_id = self.tree.item(selected[0])['values'][0]
            EleveForm(self, eleve_id)

    def delete_selected_student(self):
        selected = self.tree.selection()
        if selected:
            eleve_id = self.tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Confirmation", "Supprimer cet élève?"):
                db.delete_eleve(eleve_id)
                self.refresh_table()

    def view_student_notes(self):
        selected = self.tree.selection()
        if selected:
            eleve_id = self.tree.item(selected[0])['values'][0]
            notes = db.get_notes(eleve_id)
            student_data = {
                'id': eleve_id,
                'nom': self.tree.item(selected[0])['values'][1],
                'prenom': self.tree.item(selected[0])['values'][2],
                'classe': self.tree.item(selected[0])['values'][3]
            }
            NotesViewDialog(self, student_data, notes)

    def view_student_absences(self):
        selected = self.tree.selection()
        if selected:
            eleve_id = self.tree.item(selected[0])['values'][0]
            absences = db.get_absences(eleve_id)
            student_data = {
                'id': eleve_id,
                'nom': self.tree.item(selected[0])['values'][1],
                'prenom': self.tree.item(selected[0])['values'][2],
                'classe': self.tree.item(selected[0])['values'][3]
            }
            AbsencesViewDialog(self, student_data, absences)

    def export_csv_ui(self):
        # Placeholder for exporting CSV
        print("TODO: export_csv_ui")

    def export_pdf_ui(self):
        # Placeholder for exporting PDF
        print("TODO: export_pdf_ui")

    def sort_treeview(self, tree, col, reverse):
        """Sort treeview content by column"""
        data = [(tree.set(item, col), item) for item in tree.get_children('')]
        
        # Convert numeric values for proper sorting
        if col in ["ID", "Moyenne", "Absences"]:
            # Convert to numbers (with error handling)
            temp_data = []
            for item in data:
                try:
                    if col == "Moyenne" and item[0] == '-':
                        key = 0
                    else:
                        key = float(item[0])
                except ValueError:
                    key = 0
                temp_data.append((key, item[1]))
            data = temp_data
            
        # Sort data
        data.sort(reverse=reverse)
        
        # Rearrange items in sorted order
        for index, (_, item) in enumerate(data):
            tree.move(item, '', index)
            
        # Reverse sort next time
        tree.heading(col, command=lambda: self.sort_treeview(tree, col, not reverse))


class NotesViewDialog(tk.Toplevel):
    def __init__(self, parent, student, student_notes):
        super().__init__(parent)
        self.parent = parent
        self.student = student
        self.student_notes = student_notes
        
        self.title(f"Notes de {student['prenom']} {student['nom']}")
        self.geometry("600x500")
        self.configure(bg=COLORS['background'])
        self.setup_fonts()
        self.setup_style()
        self.create_widgets()
        self.center_window()
        self.transient(parent)
        self.grab_set()

    def setup_fonts(self):
        self.title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        self.normal_font = tkFont.Font(family="Helvetica", size=11)
        self.button_font = tkFont.Font(family="Helvetica", size=11, weight="bold")

    def setup_style(self):
        style = ttk.Style(self)
        style.configure('TFrame', background=COLORS['background'])
        style.configure('Card.TFrame', background=COLORS['card'])
        style.configure('TLabel', background=COLORS['card'], foreground=COLORS['text'], font=self.normal_font)
        style.configure('Title.TLabel', background=COLORS['card'], foreground=COLORS['primary'], font=self.title_font)
        
        # Table style
        style.configure('Treeview', 
                        background=COLORS['card'],
                        foreground=COLORS['text'],
                        rowheight=30,
                        fieldbackground=COLORS['card'],
                        font=self.normal_font)
        style.configure('Treeview.Heading', 
                        font=self.normal_font,
                        background=COLORS['primary'],
                        foreground=COLORS['button_text'])
                        
        # Button styles
        style.configure('Primary.TButton', 
                        background=COLORS['primary'],
                        foreground=COLORS['button_text'],
                        font=self.button_font)
        style.map('Primary.TButton',
                    background=[('active', COLORS['primary_light'])])

    def create_widgets(self):
        main_frame = ttk.Frame(self, style='Card.TFrame', padding=20)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Student info
        info_frame = ttk.Frame(main_frame, style='Card.TFrame')
        info_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(info_frame, text=f"Notes de {self.student['prenom']} {self.student['nom']}", 
                    style='Title.TLabel').pack(pady=(0, 10))

        ttk.Label(info_frame, text=f"Classe: {self.student['classe']} | ID: {self.student['id']}",
                    style='TLabel').pack()
        
        # Calculate average
        notes_values = [note[2] for note in self.student_notes]
        avg = calculate_average(notes_values)
        # :.2f is a format specifier that formats a float to 2 decimal places
        avg_text = f"{avg:.2f}" if avg is not None else "Aucune note"
        
        ttk.Label(info_frame, text=f"Moyenne générale: {avg_text}",
                    style='TLabel').pack(pady=(5, 0))
        
        # Notes table
        table_frame = ttk.Frame(main_frame, style='Card.TFrame')
        table_frame.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Table
        columns = ("ID", "Matière", "Note", "Date")
        self.notes_tree = ttk.Treeview(table_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        
        self.notes_tree.column("ID", width=80, anchor='center')
        self.notes_tree.column("Matière", width=180, anchor='w')
        self.notes_tree.column("Note", width=80, anchor='center')
        self.notes_tree.column("Date", width=120, anchor='center')

        self.notes_tree.heading("ID", text="ID")
        self.notes_tree.heading("Matière", text="Matière")
        self.notes_tree.heading("Note", text="Note")
        self.notes_tree.heading("Date", text="Date")
        
        self.notes_tree.pack(fill='both', expand=True)
        scrollbar.config(command=self.notes_tree.yview)
        
        # Fill table
        for note in self.student_notes:
            self.notes_tree.insert('', 'end', values=(note[0], note[1], note[2], note[3]))
        
        # Buttons
        button_frame = ttk.Frame(main_frame, style='Card.TFrame')
        button_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(button_frame, text="Modifier la note selectionnée",
                    command=self.update_note, 
                    style='Primary.TButton').pack(side='left', padx=5)

        ttk.Button(button_frame, text="Supprimer la note sélectionnée", 
                    command=self.delete_selected_note, 
                    style='Primary.TButton').pack(side='left', padx=5)

        ttk.Button(button_frame, text="Fermer", 
                    command=self.destroy, 
                    style='Primary.TButton').pack(side='right', padx=5)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width + 200, height + 70, x - 100, y - 50))

    def update_note(self):
        selected_note = self.notes_tree.selection()
        if not selected_note:
            messagebox.showerror("Erreur", "Aucune note sélectionnée", parent=self)
            return
        note_id = self.notes_tree.item(selected_note[0])['values'][0]
        
        # Open the NoteForm properly and wait
        form = NoteForm(self, note_id)
        self.wait_window(form)  # <<<<<< Wait until the NoteForm is closed
        
        self.parent.refresh_table()
        self.destroy()

    def delete_selected_note(self):
        selected_note = self.notes_tree.selection()
        if not selected_note:
            messagebox.showerror("Erreur", "Aucune note sélectionnée", parent=self)
            return
        note_id = self.notes_tree.item(selected_note[0])['values'][0]
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette note ?", parent=self):
            db.delete_note(note_id)
            self.notes_tree.delete(selected_note[0])
            self.parent.refresh_table()
            self.destroy()
            messagebox.showinfo("Succès", "Note supprimée avec succès")


class AbsencesViewDialog(tk.Toplevel):
    def __init__(self, parent, student, student_absences):
        super().__init__(parent)
        self.parent = parent
        self.student = student
        self.student_absences = student_absences
        
        self.title(f"Absences de {student['prenom']} {student['nom']}")
        self.geometry("600x500")
        self.configure(bg=COLORS['background'])
        self.setup_fonts()
        self.setup_style()
        self.create_widgets()
        self.center_window()
        self.transient(parent)
        self.grab_set()

    def setup_fonts(self):
        self.title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        self.normal_font = tkFont.Font(family="Helvetica", size=11)
        self.button_font = tkFont.Font(family="Helvetica", size=11, weight="bold")

    def setup_style(self):
        style = ttk.Style(self)
        style.configure('TFrame', background=COLORS['background'])
        style.configure('Card.TFrame', background=COLORS['card'])
        style.configure('TLabel', background=COLORS['card'], foreground=COLORS['text'], font=self.normal_font)
        style.configure('Title.TLabel', background=COLORS['card'], foreground=COLORS['primary'], font=self.title_font)
        
        # Table style
        style.configure('Treeview', 
                        background=COLORS['card'],
                        foreground=COLORS['text'],
                        rowheight=30,
                        fieldbackground=COLORS['card'],
                        font=self.normal_font)
        style.configure('Treeview.Heading', 
                        font=self.normal_font,
                        background=COLORS['primary'],
                        foreground=COLORS['button_text'])
                        
        # Button styles
        style.configure('Primary.TButton', 
                            background=COLORS['primary'],
                            foreground=COLORS['button_text'],
                            font=self.button_font)
        style.map('Primary.TButton',
                    background=[('active', COLORS['primary_light'])])

    def create_widgets(self):
        main_frame = ttk.Frame(self, style='Card.TFrame', padding=20)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Student info
        info_frame = ttk.Frame(main_frame, style='Card.TFrame')
        info_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(info_frame, text=f"Absences de {self.student['prenom']} {self.student['nom']}", 
                    style='Title.TLabel').pack(pady=(0, 10))

        ttk.Label(info_frame, text=f"Classe: {self.student['classe']} | ID: {self.student['id']}",
                    style='TLabel').pack()
        
        # Absences count and rate
        nbr_abs = len(self.student_absences)
        taux = attendance_rate(30, nbr_abs)  # If We Have 30 days/month
        
        ttk.Label(info_frame, text=f"Nombre d'absences: {nbr_abs} | Taux d'assiduité: {taux}%",
                    style='TLabel').pack(pady=(5, 0))
        
        # Absences table
        table_frame = ttk.Frame(main_frame, style='Card.TFrame')
        table_frame.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')

        # Table
        columns = ("ID", "Nombre Absences", "Date")
        self.absences_tree = ttk.Treeview(
            table_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set
        )

        self.absences_tree.column("ID", width=100, anchor='center')
        self.absences_tree.heading("ID", text="ID")

        self.absences_tree.column("Nombre Absences", width=120, anchor='center')
        self.absences_tree.heading("Nombre Absences", text="Nombre d'absences")

        self.absences_tree.column("Date", width=250, anchor='center')
        self.absences_tree.heading("Date", text="Date de l'absence")

        self.absences_tree.pack(fill='both', expand=True)
        scrollbar.config(command=self.absences_tree.yview)

        # Fill table
        for absence in self.student_absences:
            self.absences_tree.insert('', 'end', values=(absence[0], absence[1], absence[2]))
        
        # Buttons
        button_frame = ttk.Frame(main_frame, style='Card.TFrame')
        button_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(button_frame, text="Modifier l'absence sélectionnée", 
                command=self.modifier_absence, 
                style='Primary.TButton').pack(side='left', padx=5)

        ttk.Button(button_frame, text="Supprimer l'absence sélectionnée", 
                    command=self.delete_selected_absence, 
                    style='Primary.TButton').pack(side='left', padx=5)

        ttk.Button(button_frame, text="Fermer", 
                    command=self.destroy, 
                    style='Primary.TButton').pack(side='right', padx=5)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width + 200, height + 70, x - 100, y - 50))

    def modifier_absence(self):
        selected_absence = self.absences_tree.selection()
        if not selected_absence:
            messagebox.showerror("Erreur", "Aucune absence sélectionnée", parent=self)
            return
        absence_id = self.absences_tree.item(selected_absence[0])['values'][0]
        AbsenceForm(self, absence_id)
        self.parent.refresh_table()
        self.destroy()

    def delete_selected_absence(self):
        selected_absence = self.absences_tree.selection()
        if not selected_absence:
            messagebox.showerror("Erreur", "Aucune absence sélectionnée", parent=self)
            return
        absence_id = self.absences_tree.item(selected_absence[0])['values'][0]
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette absence?", parent=self):
            db.delete_absence(absence_id)
            self.absences_tree.delete(selected_absence[0])
            self.parent.refresh_table()
            self.destroy()
            messagebox.showinfo("Succès", "Absence supprimée avec succès")