# Grade and Absence Management System 📚✏️

## Overview
A comprehensive Python-based application for managing student grades and absences, designed to help educational institutions track and analyze student performance and attendance.

## Features 🌟
- Student Management
  - Add, edit, and delete student records
  - Track student information (name, class)

- Grade Management
  - Record and manage student grades
  - Calculate average grades
  - Export grades to CSV and PDF

- Absence Tracking
  - Record student absences
  - Calculate attendance rates
  - Visualize absence data

## Technologies Used 💻
- Python
- Tkinter (GUI)
- SQLite (Database)
- tkcalendar (Date selection)
- ReportLab (PDF generation)

## Prerequisites 🛠️
- Python 3.8+
- pip (Python package manager)

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/ZahaAnass/management-of-grades-and-absences.git
cd management-of-grades-and-absences
```

2. Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application 🖥️
```bash
python app.py
```

## Project Structure 📂
```
management-of-grades-and-absences/
│
├── app.py           # Main application entry point
├── view.py          # User interface and forms
├── database.py      # Database operations
├── utils.py         # Utility functions
├── requirements.txt # Project dependencies
└── grademanagement.db  # SQLite database file
```

## Export Capabilities 📄
- Export student grades to CSV
- Generate PDF reports of student performance

## Contributing 🤝
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Project Link: [https://github.com/ZahaAnass/management-of-grades-and-absences](https://github.com/ZahaAnass/management-of-grades-and-absences)