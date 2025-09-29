🚀 AI Internship Recommender 🚀
Welcome to the AI Internship Recommender, a smart, Flask-powered web application designed to help students and aspiring professionals navigate their career paths. This platform goes beyond simple job listings by providing personalized, data-driven insights through adaptive tests, a professional resume analyzer, and a dynamic resource hub.

Our goal is to bridge the gap between academic knowledge and industry requirements, offering users a clear roadmap to success in the competitive tech landscape.

✨ Key Features
This application is packed with features designed to provide a comprehensive career-building experience:

🔐 Secure User Authentication: A complete login and registration system to manage user profiles.

📊 Dynamic User Dashboard: A modern, professional dashboard that features:

Performance Trend Graph: A visual representation of the user's test performance over time.

At-a-Glance Stats: Key metrics like average score and total tests taken.

Interactive Domain Exploration: Users can explore various tech domains (AI/ML, Data Science, etc.), each with a detailed pop-up modal showing a learning roadmap, free resources, and certification guidance.

Auto-Scrolling Tech News: A continuously scrolling feed of the latest news articles relevant to different tech fields to keep users informed.

🧠 Adaptive Internship Test:

Generates a unique 30-question test with a balanced mix of 15 aptitude and 15 technical questions.

Questions are curated with a 5-5-5 split of easy, medium, and hard difficulties.

Proctoring Features: The system warns users for exiting full-screen or switching tabs, with an auto-submit feature after three violations.

📄 AI-Powered Resume Analyzer:

A dedicated page for users to upload their PDF resume.

Provides an instant (simulated) ATS Friendliness Score.

Analyzes content to suggest Recommended Job Roles, detect Keywords, and check for crucial elements like Action Verbs and Contact Info.

Offers actionable Suggestions for Improvement in a clean, tabbed interface.

📈 Detailed Performance Analysis:

After each test, users receive a comprehensive results page.

Includes a Pie Chart for the overall score and a Bar Chart breaking down performance by topic.

Provides personalized Learning Recommendations and Course Resources based on weak areas.

Conditionally recommends internships from reputable platforms if the user scores above 65%.

🛠️ Tech Stack
This project is built with a modern and efficient technology stack:

Backend: Python with Flask

Database: SQLite

Frontend: HTML5, CSS3, JavaScript

Charting: Chart.js

Styling: Modern, custom CSS with a futuristic theme.

⚙️ Setup and Installation
To get the project running on your local machine, follow these simple steps:

Clone the Repository

git clone [https://github.com/your-username/ai-internship-recommender.git](https://github.com/your-username/ai-internship-recommender.git)
cd ai-internship-recommender

Create a Virtual Environment
It's recommended to use a virtual environment to manage project dependencies.

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install Dependencies
Install all the required Python packages from the requirements.txt file.

pip install -r requirements.txt

(Note: You will need to create a requirements.txt file by running pip freeze > requirements.txt in your terminal.)

Prepare the Database
Run the prepare_db.py script once to create and populate a fresh db.sqlite file with the correct schema and sample questions.

python prepare_db.py

Run the Application
Start the Flask development server.

flask run

The application will be available at http://127.0.0.1:5000 in your web browser.

📂 Project Structure
/
├── app.py <br>                 # Main Flask application file with all routes and logic.
├── prepare_db.py <br>           # Script to initialize and populate the database.
├── db.sqlite <br>              # The SQLite database file.
├── templates/<br>
│   ├── login.html<br>          # Login page.
│   ├── register.html <br>      # Registration page.
│   ├── profile.html <br>       # Main user dashboard.
│   ├── student_profile.html<br> # Detailed user profile view.
│   ├── test.html  <br>         # The proctored test page.
│   ├── results.html  <br>      # The test results and analysis page.
│   └── resume_analyzer.html <br># The dedicated resume analyzer page.
└── README.md <br>              # You are here!

🚀 Future Enhancements
This project has a strong foundation with many possibilities for future development:

Real-time News: Integrate a live news API (e.g., NewsAPI) to fetch the latest tech articles automatically.

Advanced ML Model: Implement a real machine learning model for more accurate resume analysis and job role recommendations.

User Progress Tracking: Develop a more detailed skill-tracking system based on multiple test performances.

Company Profiles: Add a section for companies to post internship listings directly on the platform.

Thank you for checking out the AI Internship Recommender!
