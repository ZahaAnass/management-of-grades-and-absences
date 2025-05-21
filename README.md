# Grade and Absence Management System 📚✏️

## Overview
A comprehensive educational management system designed for teachers and academic administrators to track student performance and attendance. This application provides an intuitive interface for managing grades, monitoring absences, and generating detailed analytical reports.

## Key Features 🌟

### Student Management 👥
- Complete student profile management (Add/Edit/Delete)
- Required fields: First name, Last name, Class
- Interactive student list with search capabilities
- Data validation and error handling

### Grade Management 📊
- Grade entry by subject
- Grade modification and deletion
- Automatic average calculation
  - Individual student averages
  - Class averages
  - Subject-specific averages
- Grade history tracking

### Attendance Tracking 📅
- Absence recording with specific dates
- Multiple absence entry modes:
  - Single day absences
  - Multi-day periods
- Automatic attendance rate calculation
- Attendance history visualization

### Interactive Data View 🔍
- Modern TreeView implementation featuring:
  - Sortable columns
  - Search functionality
  - Class-based filtering
  - Subject-based filtering
- Real-time data updates

### Reporting System 📈
- Export capabilities:
  - CSV format for data analysis
  - PDF reports with professional formatting
- Statistical reporting:
  - Individual student performance
  - Class performance metrics
  - Attendance rate analysis

## Technical Stack 💻
- **Python 3.8+**: Core programming language
- **Tkinter/ttk**: Modern GUI framework
- **SQLite**: Local database engine
- **tkcalendar**: Date selection widget
- **ReportLab**: PDF report generation

## Database Structure 🗄️
```sql
-- Students Table
CREATE TABLE eleves (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    classe TEXT NOT NULL
);

-- Grades Table
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    eleve_id INTEGER,
    matiere TEXT NOT NULL,
    note REAL NOT NULL,
    date_note DATE,
    FOREIGN KEY (eleve_id) REFERENCES eleves(id)
);

-- Absences Table
CREATE TABLE absences (
    id INTEGER PRIMARY KEY,
    eleve_id INTEGER,
    date_absence DATE,
    nb_jours INTEGER,
    FOREIGN KEY (eleve_id) REFERENCES eleves(id)
);
```

## Project Structure 📂
```
management-of-grades-and-absences/
│
├── app.py           # Application entry point
├── database.py      # Database operations (CRUD)
├── views.py         # GUI implementation
├── utils.py         # Helper functions
├── requirements.txt # Dependencies
└── grademanagement.db # SQLite database
```

## Installation Guide 🚀

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/ZahaAnass/management-of-grades-and-absences.git
cd management-of-grades-and-absences
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage Guide 📖

1. Launch the application:
```bash
python app.py
```

2. Main Features:
   - Use the top navigation bar for main functions
   - Access student management from the left panel
   - View grades and absences in the central table
   - Generate reports using the export menu

3. Data Entry:
   - Add students via the "New Student" form
   - Enter grades through the "Grade Entry" interface
   - Record absences using the calendar widget

4. Reporting:
   - Export data using the "Export" menu
   - Generate PDF reports with the "Report" button
   - View statistics in the "Analytics" section

## Contributing 🤝
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## Project Status 📈
- Version: 1.0.0
- Active development
- Regular updates

## Links 🔗
- Repository: [GitHub](https://github.com/ZahaAnass/management-of-grades-and-absences)
- Issues: [Bug Reports](https://github.com/ZahaAnass/management-of-grades-and-absences/issues)

## License 📜
This project is licensed under the MIT License.