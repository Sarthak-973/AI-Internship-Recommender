# 🚀 AI Internship Recommender

The **AI Internship Recommender** is a Flask-based web app that helps students explore tech careers, analyze resumes, and take adaptive tests to identify suitable internship paths. It bridges the gap between academic learning and industry expectations with personalized insights.

---

## ✅ Features

### 🔐 User Authentication
- Secure login & registration

### 🏠 User Dashboard
- Performance trend chart  
- Test stats  
- Explore tech domains with:
  - Learning roadmaps
  - Resources
  - Certifications  
- Auto-scrolling tech news

### 🧠 Adaptive Internship Test
- 30 questions (15 aptitude + 15 technical)  
- Easy/Medium/Hard mix  
- Full-screen tracking with violation warnings

### 📄 Resume Analyzer (AI-Simulated)
- Upload PDF  
- ATS score  
- Suggested job roles  
- Keyword & section analysis  
- Improvement tips

### 📊 Test Results
- Pie & bar charts  
- Personalized learning suggestions  
- Internship recommendations (for 65%+ scores)

---

## 🛠️ Tech Stack
- **Backend:** Flask (Python)  
- **Database:** SQLite  
- **Frontend:** HTML, CSS, JavaScript  
- **Charts:** Chart.js

---

## ⚙️ Setup & Installation

```bash
# Clone repository
git clone https://github.com/your-username/ai-internship-recommender.git
cd ai-internship-recommender
```
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# or
source venv/bin/activate   # macOS/Linux
```
```bash
# Install dependencies
pip install -r requirements.txt
```
```bash
# Set up the database
python prepare_db.py
```
```bash
# Run the app
flask run
```

📂 Project Structure
/<br> 
├── app.py                                    <br> 
├── prepare_db.py                            <br> 
├── db.sqlite                                 <br> 
├── templates/                                <br> 
│   ├── login.html                             <br> 
│   ├── register.html                           <br> 
│   ├── profile.html                            <br> 
│   ├── student_profile.html                       <br> 
│   ├── test.html                                <br> 
│   ├── results.html                               <br> 
│   └── resume_analyzer.html                         <br> 
└── README.md                                           <br> 

Thank you for checking out the AI Internship Recommender!
