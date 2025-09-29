import sqlite3
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, g
from datetime import datetime
import random

# helper to infer topic from question text (fallback)
def infer_topic_from_text(text: str) -> str:
    t = (text or "").lower()
    if any(k in t for k in ["select ", "sql", "query", "join", "database", "table"]):
        return "SQL"
    if any(k in t for k in ["python", "str(", "string", "list", "tuple", "dict"]):
        return "Python"
    if any(k in t for k in ["java", "class ", "new ", "extends", "implements"]):
        return "Java"
    if any(k in t for k in ["algorithm", "complexity", "time complexity", "sort", "dp", "recurrence"]):
        return "DSA"
    if any(k in t for k in ["neural", "machine learning", "ml", "deep learning", "model", "regression", "classification"]):
        return "AI/ML"
    if any(k in t for k in ["network", "tcp", "udp", "ip", "routing", "packet"]):
        return "Networking"
    if any(k in t for k in ["software engineering", "sdlc", "uml", "design pattern", "git", "testing"]):
        return "Software Engineering"
    # fallback
    return "General"


app = Flask(__name__)
app.secret_key = "replace_this_with_a_random_secret"  # change for production
DATABASE = "db.sqlite"

# A dictionary mapping skills to free learning resources
SKILL_RESOURCES = {
    "Python": "https://www.freecodecamp.org/learn/scientific-computing-with-python/",
    "TensorFlow": "https://www.tensorflow.org/tutorials",
    "PyTorch": "https://pytorch.org/tutorials/",
    "NLP": "https://www.deeplearning.ai/short-courses/natural-language-processing-specialization/",
    "Computer Vision": "https://www.udacity.com/course/introduction-to-computer-vision--ud810",
    "Advanced ML": "https://developers.google.com/machine-learning/crash-course",
    "Deep Learning": "https://www.deeplearning.ai/courses/deep-learning-specialization/",
    "Reinforcement Learning": "https://www.deeplearning.ai/courses/reinforcement-learning-specialization/",
    "MLOps": "https://www.deeplearning.ai/courses/machine-learning-engineering-for-production-mlops-specialization/",
    "SQL": "https://www.khanacademy.org/computing/computer-programming/sql",
    "Tableau": "https://www.tableau.com/learn/training/20221",
    "Power BI": "https://learn.microsoft.com/en-us/power-bi/fundamentals/power-bi-learning-paths",
    "Excel": "https://www.excel-easy.com/",
    "Statistics": "https://www.khanacademy.org/math/statistics-probability",
    "Advanced SQL": "https://www.geeksforgeeks.org/advanced-sql/",
    "ETL Pipelines": "https://www.projectpro.io/article/etl-pipeline-projects/565",
    "Big Data (Spark)": "https://spark.apache.org/docs/latest/api/python/getting_started/index.html",
    "A/B Testing": "https://www.optimizely.com/optimization-glossary/ab-testing/",
    "HTML5": "https://www.w3schools.com/html/",
    "CSS3": "https://www.w3schools.com/css/",
    "JavaScript": "https://javascript.info/",
    "React": "https://react.dev/learn",
    "Vue.js": "https://vuejs.org/guide/introduction.html",
    "TypeScript": "https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html",
    "Next.js": "https://nextjs.org/learn",
    "GraphQL": "https://graphql.org/learn/",
    "Webpack": "https://webpack.js.org/guides/getting-started/",
    "CI/CD": "https://www.atlassian.com/continuous-delivery/ci-cd-basics",
    "Node.js": "https://nodejs.dev/learn",
    "Django": "https://docs.djangoproject.com/en/5.0/intro/tutorial01/",
    "Databases": "https://www.codecademy.com/learn/learn-sql",
    "APIs": "https://www.freecodecamp.org/news/what-is-an-api-in-english-please/",
    "System Design Basics": "https://github.com/donnemartin/system-design-primer",
    "Microservices": "https://microservices.io/",
    "Docker": "https://docs.docker.com/get-started/",
    "Kubernetes": "https://kubernetes.io/docs/tutorials/kubernetes-basics/",
    "Cloud (AWS/GCP)": "https://aws.amazon.com/training/digital/",
    "Message Queues": "https://aws.amazon.com/message-queue/",
}

# --- UPDATED: Tech News with recent, valid links and relevant images ---
TECH_NEWS = {
    "ai": [
        {
            "title": "Microsoft overtakes Apple as world's most valuable company",
            "source": "Reuters",
            "url": "https://www.reuters.com/technology/microsoft-overtakes-apple-worlds-most-valuable-company-2024-01-12/",
            "image": "https://placehold.co/600x400/7E57C2/FFFFFF?text=AI+Market"
        },
        {
            "title": "Meta says its next AI model will be the 'most powerful' open source system",
            "source": "The Verge",
            "url": "https://www.theverge.com/2024/3/13/24099913/meta-llama-3-open-source-ai-model",
            "image": "https://placehold.co/600x400/5C6BC0/FFFFFF?text=Open+Source+AI"
        }
    ],
    "data": [
        {
            "title": "DataStax acquires Langflow to accelerate generative AI development",
            "source": "VentureBeat",
            "url": "https://venturebeat.com/ai/datastax-acquires-langflow-to-accelerate-generative-ai-development/",
            "image": "https://placehold.co/600x400/42A5F5/FFFFFF?text=GenAI+Data"
        },
        {
            "title": "Gartner Identifies Top Trends in Data and Analytics for 2024",
            "source": "Gartner",
            "url": "https://www.gartner.com/en/newsroom/press-releases/2024-03-11-gartner-identifies-top-trends-in-data-and-analytics-for-2024",
            "image": "https://placehold.co/600x400/29B6F6/FFFFFF?text=Data+Trends"
        }
    ],
    "frontend": [
        {
            "title": "React 19: The New Features We're Excited About",
            "source": "InfoQ",
            "url": "https://www.infoq.com/news/2024/02/react-19/",
            "image": "https://placehold.co/600x400/26A69A/FFFFFF?text=React+19"
        },
        {
            "title": "Vite 5.0 is out!",
            "source": "Vite Blog",
            "url": "https://vitejs.dev/blog/announcing-vite5",
            "image": "https://placehold.co/600x400/66BB6A/FFFFFF?text=ViteJS"
        }
    ],
    "backend": [
        {
            "title": "The growing popularity of Rust in backend development",
            "source": "LogRocket Blog",
            "url": "https://blog.logrocket.com/grows-rust-popularity-backend-development/",
            "image": "https://placehold.co/600x400/FFA726/FFFFFF?text=Rust+Lang"
        },
        {
            "title": "What is Platform Engineering?",
            "source": "InfoQ",
            "url": "https://www.infoq.com/articles/what-is-platform-engineering/",
            "image": "https://placehold.co/600x400/FF7043/FFFFFF?text=Platform+Eng"
        }
    ]
}


DOMAIN_DETAILS = {
    "ai": {
        "title": "Artificial Intelligence & ML",
        "image": "https://images.unsplash.com/photo-1599058917212-d750089bc07e?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "what_to_learn": [
            "Master Python and its data science libraries (NumPy, Pandas, Matplotlib).",
            "Understand Machine Learning fundamentals: Supervised vs. Unsupervised Learning, Regression, and Classification.",
            "Dive into Deep Learning: Neural Networks, CNNs for images, and RNNs for text.",
            "Get hands-on with a framework like TensorFlow or PyTorch.",
            "Explore a specialization like Natural Language Processing (NLP) or Computer Vision."
        ],
        "resources": [
            {"name": "Google's Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course"},
            {"name": "DeepLearning.AI on Coursera", "url": "https://www.coursera.org/specializations/deep-learning"},
            {"name": "Kaggle for hands-on projects", "url": "https://www.kaggle.com/"}
        ],
        "certifications": [
            "TensorFlow Developer Certificate",
            "AWS Certified Machine Learning - Specialty",
            "DeepLearning.AI TensorFlow Developer Professional Certificate"
        ],
        "guidance": "Focus on building a strong portfolio of projects. Start with simple datasets and gradually move to more complex problems. Understanding the underlying math and statistics is crucial for long-term success. Contribute to open-source projects to gain real-world experience."
    },
    "data": {
        "title": "Data Science & Analytics",
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "what_to_learn": [
            "Become proficient in SQL for data extraction and manipulation.",
            "Learn Python or R for statistical analysis and data modeling.",
            "Master data visualization tools like Tableau or Power BI.",
            "Understand key statistical concepts: Probability, Hypothesis Testing, and A/B Testing.",
            "Learn about data warehousing, ETL pipelines, and data cleaning techniques."
        ],
        "resources": [
            {"name": "Khan Academy - SQL: Querying and managing data", "url": "https://www.khanacademy.org/computing/computer-programming/sql"},
            {"name": "freeCodeCamp - Data Analysis with Python", "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/"},
            {"name": "Google Data Analytics Professional Certificate", "url": "https://www.coursera.org/professional-certificates/google-data-analytics"}
        ],
        "certifications": [
            "Google Data Analytics Professional Certificate",
            "IBM Data Analyst Professional Certificate",
            "Microsoft Power BI Data Analyst Associate"
        ],
        "guidance": "Develop strong storytelling skills. Your ability to communicate insights from data is as important as your technical skills. Start a blog or create a public portfolio of your analysis projects. Attention to detail and a curious mindset are key."
    },
    "frontend": {
        "title": "Frontend Development",
        "image": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "what_to_learn": [
            "Build a strong foundation in HTML, CSS, and modern JavaScript (ES6+).",
            "Master a popular framework like React, Vue, or Angular.",
            "Understand responsive design and mobile-first development.",
            "Learn about state management libraries (e.g., Redux, Vuex).",
            "Get comfortable with version control (Git) and package managers (npm/yarn)."
        ],
        "resources": [
            {"name": "The Odin Project - Full Stack JavaScript", "url": "https://www.theodinproject.com/paths/full-stack-javascript"},
            {"name": "React Official Documentation", "url": "https://react.dev/learn"},
            {"name": "CSS-Tricks for all things CSS", "url": "https://css-tricks.com/"}
        ],
        "certifications": [
            "freeCodeCamp Responsive Web Design Certification",
            "Meta Front-End Developer Professional Certificate"
        ],
        "guidance": "Create a visually appealing portfolio of web projects. Replicate complex UIs from popular websites to challenge yourself. Focus on user experience and web performance. Keep up-to-date with the fast-evolving ecosystem of tools and frameworks."
    },
    "backend": {
        "title": "Backend Development",
        "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "what_to_learn": [
            "Choose a language and framework (e.g., Python with Django/Flask, Node.js with Express).",
            "Understand how to design and build RESTful APIs.",
            "Learn about different types of databases (SQL like PostgreSQL, and NoSQL like MongoDB).",
            "Grasp concepts of authentication, security, and data protection.",
            "Explore containerization with Docker and basics of cloud deployment."
        ],
        "resources": [
            {"name": "MDN Web Docs - Server-side website programming", "url": "https://developer.mozilla.org/en-US/docs/Learn/Server-side"},
            {"name": "Postman Learning Center for APIs", "url": "https://www.postman.com/learning/"},
            {"name": "Docker Get Started Guide", "url": "https://docs.docker.com/get-started/"}
        ],
        "certifications": [
            "AWS Certified Developer - Associate",
            "IBM Back-End Development Professional Certificate"
        ],
        "guidance": "Focus on logic, efficiency, and security. Build robust APIs for your frontend projects. Understand how data flows through a system. Reading about system design principles will be highly beneficial for interviews and career growth."
    }
}


# ---------- Database helpers ----------
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    return cur.lastrowid

# Create missing tables if not present (safe to run always)
def init_db():
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        year INTEGER
    );
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        difficulty TEXT,
        min_year INTEGER,
        question TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        answer TEXT
    );
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        score INTEGER,
        max_score INTEGER,
        percent REAL,
        taken_at TEXT,
        details TEXT
    );
    CREATE TABLE IF NOT EXISTS professional_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        fullname TEXT,
        college TEXT,
        graduation_year INTEGER,
        cgpa TEXT,
        bio TEXT,
        linkedin_url TEXT,
        github_url TEXT,
        work_experience TEXT,
        projects TEXT,
        skills TEXT
    );
    """
    db = get_db()
    db.executescript(sql)
    db.commit()

# ensure DB & tables exist on startup
with app.app_context():
    if not os.path.exists(DATABASE):
        open(DATABASE, "a").close()
    init_db()

# ---------- Routes ----------
@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        year_raw = request.form.get("year", "1")
        try:
            year = int(year_raw)
            if year not in (1,2,3,4):
                year = 1
        except:
            year = 1

        if not (name and email and password):
            return render_template("register.html", error="Please fill all required fields.")

        hashed = generate_password_hash(password)
        try:
            execute_db("INSERT INTO users (name,email,password,year) VALUES (?,?,?,?)", (name,email,hashed,year))
        except sqlite3.IntegrityError:
            return render_template("register.html", error="An account with that email already exists.")
        except Exception as e:
            return render_template("register.html", error=f"Error: {e}")

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = query_db("SELECT * FROM users WHERE email=?", (email,), one=True)
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    uid = session["user_id"]
    user = query_db("SELECT * FROM users WHERE id=?", (uid,), one=True)
    if not user:
        session.clear()
        return redirect(url_for("login"))

    stats = query_db("""
        SELECT
            COUNT(*) as tests_taken,
            ROUND(AVG(percent), 2) as average_score,
            MAX(percent) as best_score
        FROM results WHERE user_id=?
    """, (uid,), one=True)

    results = query_db("SELECT * FROM results WHERE user_id=? ORDER BY taken_at DESC LIMIT 5", (uid,))

    # --- NEW: Fetch data for performance graph ---
    graph_results = query_db("""
        SELECT percent, taken_at 
        FROM results 
        WHERE user_id=? 
        ORDER BY taken_at ASC 
        LIMIT 10
    """, (uid,))

    # Process data for the chart
    chart_labels = []
    chart_scores = []
    if graph_results:
        for row in graph_results:
            date = datetime.strptime(row['taken_at'].split(' ')[0], '%Y-%m-%d').strftime('%b %d')
            chart_labels.append(date)
            chart_scores.append(row['percent'])
    # --- END NEW ---

    return render_template(
        "profile.html", 
        user=user, 
        stats=stats, 
        results=results, 
        domain_details=DOMAIN_DETAILS, 
        tech_news=TECH_NEWS,
        chart_labels=json.dumps(chart_labels),
        chart_scores=json.dumps(chart_scores)
    )

@app.route("/student-profile", methods=["GET", "POST"])
def view_student_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    uid = session["user_id"]

    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        college = request.form.get("college", "").strip()
        graduation_year = request.form.get("graduation_year")
        cgpa = request.form.get("cgpa", "").strip()
        bio = request.form.get("bio", "").strip()
        linkedin_url = request.form.get("linkedin_url", "").strip()
        github_url = request.form.get("github_url", "").strip()
        work_experience = request.form.get("work_experience", "").strip()
        projects = request.form.get("projects", "").strip()
        skills = request.form.get("skills", "").strip()
        
        existing_profile = query_db("SELECT id FROM professional_info WHERE user_id = ?", (uid,), one=True)
        
        if existing_profile:
            execute_db("""
                UPDATE professional_info SET
                fullname=?, college=?, graduation_year=?, cgpa=?, bio=?, linkedin_url=?, github_url=?,
                work_experience=?, projects=?, skills=?
                WHERE user_id=?
            """, (fullname, college, graduation_year, cgpa, bio, linkedin_url, github_url, work_experience, projects, skills, uid))
        else:
            execute_db("""
                INSERT INTO professional_info 
                (user_id, fullname, college, graduation_year, cgpa, bio, linkedin_url, github_url, work_experience, projects, skills)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (uid, fullname, college, graduation_year, cgpa, bio, linkedin_url, github_url, work_experience, projects, skills))
        
        return redirect(url_for('view_student_profile'))

    user = query_db("SELECT * FROM users WHERE id=?", (uid,), one=True)
    prof_info = query_db("SELECT * FROM professional_info WHERE user_id=?", (uid,), one=True)
    
    return render_template("student_profile.html", user=user, prof_info=prof_info)

# --- NEW ROUTE for Resume Analyzer ---
@app.route("/resume-analyzer")
def resume_analyzer():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = query_db("SELECT * FROM users WHERE id=?", (session["user_id"],), one=True)
    return render_template("resume_analyzer.html", user=user)


@app.route("/start_test/<string:section>")
def start_test(section):
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    uid = session["user_id"]
    user = query_db("SELECT * FROM users WHERE id=?", (uid,), one=True)
    year = int(user["year"]) if user and user["year"] else 1

    difficulty_distribution = {'easy': 5, 'medium': 5, 'hard': 5}
    
    apt_qs = []
    tech_qs = []

    for difficulty, count in difficulty_distribution.items():
        query = "SELECT * FROM questions WHERE category='aptitude' AND difficulty=? AND min_year<=? ORDER BY RANDOM() LIMIT ?"
        questions = query_db(query, (difficulty, year, count))
        apt_qs.extend(questions)
    
    if len(apt_qs) < 15:
        print("Warning: Could not find enough aptitude questions with specified difficulties. Falling back to random selection.")
        query = "SELECT * FROM questions WHERE category='aptitude' AND min_year<=? ORDER BY RANDOM() LIMIT 15"
        apt_qs = query_db(query, (year,))

    for difficulty, count in difficulty_distribution.items():
        query = "SELECT * FROM questions WHERE category='technical' AND difficulty=? AND min_year<=? ORDER BY RANDOM() LIMIT ?"
        questions = query_db(query, (difficulty, year, count))
        tech_qs.extend(questions)

    if len(tech_qs) < 15:
        print("Warning: Could not find enough technical questions with specified difficulties. Falling back to random selection.")
        query = "SELECT * FROM questions WHERE category='technical' AND min_year<=? ORDER BY RANDOM() LIMIT 15"
        tech_qs = query_db(query, (year,))

    final_qs = [dict(q) for q in apt_qs] + [dict(q) for q in tech_qs]
    
    unique_qs_dict = {q['id']: q for q in final_qs}
    final_qs = list(unique_qs_dict.values())
    random.shuffle(final_qs)

    for q in final_qs:
        if not q.get("topic"):
            q["topic"] = infer_topic_from_text(q.get("question"))
            
    question_ids = [q['id'] for q in final_qs]
    session["question_ids"] = question_ids
    
    session["test_started_at"] = datetime.utcnow().isoformat()
    session["time_limit"] = 30 * 60

    return render_template("test.html", questions=final_qs, section=section)


@app.route("/submit_test", methods=["POST"])
def submit_test():
    if "user_id" not in session:
        return redirect(url_for("login"))

    question_ids = session.get("question_ids", [])
    if not question_ids:
        return redirect(url_for("dashboard"))

    placeholders = ','.join(['?'] * len(question_ids))
    query = f"SELECT * FROM questions WHERE id IN ({placeholders})"
    all_questions_from_db = query_db(query, question_ids)
    
    if not all_questions_from_db:
        return redirect(url_for("dashboard"))

    qs_dict = {q['id']: dict(q) for q in all_questions_from_db}
    qs = [qs_dict[qid] for qid in question_ids if qid in qs_dict]
    
    score = 0
    max_score = len(qs)
    detailed = []
    topic_stats = {}
    
    for q in qs:
        if not q.get("topic"):
            q["topic"] = infer_topic_from_text(q.get("question"))
            
        qid = str(q.get("id"))
        selected = request.form.get("q_" + qid, "") 
        correct = q.get("answer", "N/A")
        is_correct = (selected == correct)
        if is_correct:
            score += 1

        topic = q.get("topic")
        ts = topic_stats.setdefault(topic, {"correct": 0, "total": 0, "incorrect": 0})
        ts["total"] += 1
        if is_correct:
            ts["correct"] += 1
        else:
            ts["incorrect"] += 1

        detailed.append({
            "id": q.get("id"),
            "question": q.get("question"),
            "selected": selected if selected else "Not answered",
            "correct": correct,
            "is_correct": is_correct,
            "topic": topic,
            "difficulty": q.get("difficulty", "N/A")
        })

    percent = round(score / max_score * 100, 2) if max_score > 0 else 0

    recs = []
    if percent >= 80:
        recs.append("Excellent work! You have a strong grasp of the fundamentals. Consider exploring advanced topics in your areas of interest.")
    elif percent >= 50:
        recs.append("Solid performance. You have a good foundation to build upon and can improve with targeted practice.")
    else:
        recs.append("A good starting point. Focusing on key areas will significantly boost your performance.")

    weak_topics = []
    for topic, vals in topic_stats.items():
        t_percent = round(vals["correct"] / vals["total"] * 100, 2) if vals["total"] > 0 else 0
        if t_percent < 60:
            weak_topics.append((topic, t_percent))

    weak_topics.sort(key=lambda x: x[1])

    for topic, _ in weak_topics[:5]:
        if topic == "DSA":
            recs.append("Strengthen your Data Structures & Algorithms. Practice problems on platforms like LeetCode or HackerRank.")
        elif topic == "SQL":
            recs.append("Focus on SQL. Practice writing complex queries involving JOINs, subqueries, and window functions.")
        elif topic == "Python":
            recs.append("Improve your Python fundamentals, including data types, loops, and object-oriented concepts.")
        elif topic == "AI/ML":
            recs.append("Deepen your understanding of AI/ML. Work on a hands-on project using Scikit-learn or TensorFlow.")
        elif topic == "Networking":
            recs.append("Review core concepts in Networking, such as the OSI model, TCP/IP, and common protocols.")
        else:
            recs.append(f"Review core concepts in {topic}. Building a small project can help solidify your understanding.")
    
    topic_internship_map = {
        "SQL": ["Database Management Internship", "Data Analytics Internship"],
        "Python": ["AI/ML Internship", "Data Science Internship", "Automation Internship"],
        "Java": ["Backend Development Internship", "Android Development Internship"],
        "DSA": ["Software Engineering Internship", "Competitive Programming Internship"],
        "AI/ML": ["AI/ML Internship", "Deep Learning Internship"],
        "Networking": ["Network Engineering Internship", "Cloud Networking Internship"],
        "Software Engineering": ["Software Engineering Internship"],
        "General": ["General Software Internship"]
    }
    aicte_internships = {
        "Database Management Internship": "https://unstop.com/internships?oppstatus=open&category=dba-data-warehousing&quickApply=true",
        "Data Analytics Internship": "https://unstop.com/internships?oppstatus=open&category=data-science-machine-learning&quickApply=true",
        "AI/ML Internship": "https://unstop.com/internships?oppstatus=open&category=data-science-machine-learning&quickApply=true",
        "Data Science Internship": "https://unstop.com/internships?oppstatus=open&category=data-science-machine-learning&quickApply=true",
        "Backend Development Internship": "https://unstop.com/internships?oppstatus=open&category=full-stack-development&quickApply=true",
        "Software Engineering Internship": "https://internship.aicte-india.org/software-engineering",
    }
        
    internships = []
    if percent >= 65:
        strong_topics = []
        for topic, vals in topic_stats.items():
            t_percent = round(vals["correct"] / vals["total"] * 100, 2) if vals["total"] > 0 else 0
            strong_topics.append((topic, t_percent))
        
        strong_topics.sort(key=lambda x: x[1], reverse=True)
        
        internship_names_set = set()
        for topic, _ in strong_topics[:2]:
            for internship_name in topic_internship_map.get(topic, []):
                if internship_name not in internship_names_set:
                    internship_names_set.add(internship_name)
                    internships.append({
                        "name": internship_name,
                        "url": aicte_internships.get(internship_name, "https://internship.aicte-india.org/")
                    })
    
    recommended_resources = []
    for topic, _ in weak_topics:
        if topic in SKILL_RESOURCES:
            recommended_resources.append({
                "topic": topic,
                "url": SKILL_RESOURCES[topic]
            })

    uid = session["user_id"]
    execute_db(
        "INSERT INTO results (user_id,score,max_score,percent,taken_at,details) VALUES (?,?,?,?,datetime('now'),?)",
        (uid, score, max_score, percent, json.dumps(detailed))
    )
    
    session.pop('question_ids', None)
    session.pop('test_started_at', None)

    topics = list(topic_stats.keys())
    correct_counts = [topic_stats[t]['correct'] for t in topics]
    incorrect_counts = [topic_stats[t]['incorrect'] for t in topics]

    return render_template(
        "results.html",
        score=score, 
        max_score=max_score, 
        percent=percent, 
        recs=recs,
        details=detailed, 
        internships=internships,
        topics=json.dumps(topics),
        correct_counts=json.dumps(correct_counts),
        incorrect_counts=json.dumps(incorrect_counts),
        recommended_resources=recommended_resources
    )

# ----------------- Run -----------------
if __name__ == "__main__":
    app.run(debug=True)



