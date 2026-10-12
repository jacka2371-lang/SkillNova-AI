# SkillNova-AI 🚀
AI-Powered Resume Analysis, Skill Development & Career Platform

SkillNova-AI is a Python-based platform designed to help users analyze resumes, identify skill gaps, improve their skills, and explore career opportunities through a unified dashboard.

✨ Features:

- 📄 Resume Analysis — Extract text from PDF and DOCX resumes.
- 🎯 Skill Matching — Compare candidate skills with the requirements of a selected job role.
- 📊 Match Score — View resume-to-role matching results.
- 💡 Skill Gap Analysis — Identify missing skills and receive recommendations.
- 💼 Job Opportunities — Explore available job listings and application links.
- 🎓 Learning Center — Access learning modules and quizzes.
- 🏆 Progress Tracking — Earn points and badges through learning activities.
- 🔐 User Authentication — Register and log in to a personal account.
- 🗄️ Database Integration — Store application data using SQLite.

## 🛠️ Tech Stack

- Language: Python
- Frontend: Streamlit
- Database: SQLite
- Resume Processing: PDF and DOCX text extraction
- Data Processing: Pandas
- Version Control: Git and GitHub

## 🗂️ Project Structure

```text
SkillNova-AI/
├── app.py
├── database.py
├── resume_parser.py
├── registration.py
├── login.py
├── theme.py
├── learning.py
├── jobs.py
├── ER-Diagram.md
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/jacka2371-lang/SkillNova-AI.git
cd SkillNova-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment on Windows

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m streamlit run app.py
```

## 🗄️ Database Design

View the database entity relationship diagram here:

[ER Diagram](ER-Diagram.md)

## 🎯 Project Objective

The goal of SkillNova-AI is to bring resume analysis, skill-gap identification, learning progress, and career exploration together in one platform.

## Author

Angel Blessy

GitHub: [jacka2371-lang](https://github.com/jacka2371-lang)
