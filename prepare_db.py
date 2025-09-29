import sqlite3
import os

DATABASE = "db.sqlite"

def create_new_db():
    """
    Deletes the old database file and creates a new one with the correct
    schema and a sample set of questions.
    """
    # Delete the old database file if it exists
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print(f"Removed old database file: {DATABASE}")

    # Connect to the new database (this will create the file)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    print(f"Created new database: {DATABASE}")

    # --- Create Tables ---
    # This schema must match the one in your app.py's init_db function
    cursor.executescript("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            year INTEGER
        );
        CREATE TABLE questions (
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
        CREATE TABLE results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER,
            max_score INTEGER,
            percent REAL,
            taken_at TEXT,
            details TEXT
        );
        CREATE TABLE professional_info (
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
    """)
    print("Created tables: users, questions, results, professional_info")

    # --- Sample Questions ---
    questions = [
        # --- Aptitude: Easy (5) ---
        ('aptitude', 'easy', 1, 'If a car travels at 60 km/h, how far will it travel in 2.5 hours?', '120 km', '150 km', '180 km', '200 km', 'B'),
        ('aptitude', 'easy', 1, 'What is the next number in the series: 2, 4, 6, 8, ...?', '9', '10', '11', '12', 'B'),
        ('aptitude', 'easy', 1, 'If 5 apples cost $2, how much will 20 apples cost?', '$6', '$8', '$10', '$12', 'B'),
        ('aptitude', 'easy', 1, 'A clock shows 3:15. What is the angle between the hour and minute hands?', '7.5 degrees', '10 degrees', '15 degrees', '0 degrees', 'A'),
        ('aptitude', 'easy', 1, 'Which of the following words is the odd one out?', 'Car', 'Bicycle', 'Boat', 'Bus', 'C'),

        # --- Aptitude: Medium (5) ---
        ('aptitude', 'medium', 1, 'A train 100m long is running at a speed of 30 km/hr. Find the time it takes to pass a man standing near the railway line.', '10 seconds', '12 seconds', '15 seconds', '18 seconds', 'B'),
        ('aptitude', 'medium', 1, 'The sum of the ages of a father and son is 45 years. Five years ago, the product of their ages was 34. What are their current ages?', '36, 9', '39, 6', '40, 5', '42, 3', 'B'),
        ('aptitude', 'medium', 1, 'In a group of 6 boys and 4 girls, four children are to be selected. In how many different ways can they be selected such that at least one boy should be there?', '209', '205', '200', '212', 'A'),
        ('aptitude', 'medium', 1, 'A man can row upstream at 8 kmph and downstream at 13 kmph. The speed of the stream is:', '2.5 kmph', '4.2 kmph', '5 kmph', '10.5 kmph', 'A'),
        ('aptitude', 'medium', 1, 'Find the compound interest on $16,000 at 20% per annum for 9 months, compounded quarterly.', '$2522', '$2520', '$2518', '$2516', 'A'),
        
        # --- Aptitude: Hard (5) ---
        ('aptitude', 'hard', 1, 'A and B can do a piece of work in 30 days, while B and C can do the same work in 24 days and C and A in 20 days. They all work together for 10 days, then B and C leave. How many days more will A take to finish the work?', '18 days', '20 days', '24 days', '30 days', 'A'),
        ('aptitude', 'hard', 1, 'Two pipes A and B can fill a tank in 15 minutes and 20 minutes respectively. Both pipes are opened together but after 4 minutes, pipe A is turned off. What is the total time required to fill the tank?', '10 min 20 sec', '11 min 45 sec', '12 min 30 sec', '14 min 40 sec', 'D'),
        ('aptitude', 'hard', 1, 'A bag contains 2 red, 3 green and 2 blue balls. Two balls are drawn at random. What is the probability that none of the balls drawn is blue?', '10/21', '11/21', '2/7', '5/7', 'A'),
        ('aptitude', 'hard', 1, 'In an election between two candidates, one got 55% of the total valid votes, 20% of the votes were invalid. If the total number of votes was 7500, the number of valid votes that the other candidate got was:', '2700', '2900', '3000', '3100', 'A'),
        ('aptitude', 'hard', 1, 'A trader mixes 26 kg of rice at Rs. 20 per kg with 30 kg of rice of other variety at Rs. 36 per kg and sells the mixture at Rs. 30 per kg. His profit percent is:', 'No profit, no loss', '5%', '8%', '10%', 'B'),

        # --- Technical: Easy (5) ---
        ('technical', 'easy', 1, 'What does HTML stand for?', 'Hyper Text Markup Language', 'High Tech Modern Language', 'Hyperlink and Text Markup Language', 'Home Tool Markup Language', 'A'),
        ('technical', 'easy', 1, 'Which of the following is NOT a valid variable name in Python?', 'my_var', '1st_var', '_myvar', 'myVar', 'B'),
        ('technical', 'easy', 1, 'In SQL, which command is used to retrieve data from a database?', 'GET', 'FETCH', 'SELECT', 'RETRIEVE', 'C'),
        ('technical', 'easy', 1, 'What is the correct syntax for a single-line comment in Java?', '// This is a comment', '/* This is a comment */', '# This is a comment', '<!-- This is a comment -->', 'A'),
        ('technical', 'easy', 1, 'Which data structure uses the LIFO (Last-In, First-Out) principle?', 'Queue', 'Array', 'Stack', 'Linked List', 'C'),

        # --- Technical: Medium (5) ---
        ('technical', 'medium', 1, 'What is the time complexity of a binary search algorithm?', 'O(n)', 'O(log n)', 'O(n^2)', 'O(1)', 'B'),
        ('technical', 'medium', 1, 'In object-oriented programming, what is encapsulation?', 'The ability of an object to take on many forms.', 'The process of hiding the internal state of an object and restricting access to it.', 'A mechanism for basing an object or class upon another object or class.', 'The process of creating a new object.', 'B'),
        ('technical', 'medium', 1, 'What is the purpose of the `JOIN` clause in SQL?', 'To filter records.', 'To sort records.', 'To combine rows from two or more tables based on a related column.', 'To update records.', 'C'),
        ('technical', 'medium', 1, 'Which of the following is a key feature of a RESTful API?', 'It is stateful.', 'It uses XML exclusively.', 'It is stateless.', 'It requires a SOAP protocol.', 'C'),
        ('technical', 'medium', 1, 'In Python, what is the difference between a list and a tuple?', 'Lists are mutable, tuples are immutable.', 'Tuples are mutable, lists are immutable.', 'They are the same.', 'Lists can only store integers.', 'A'),

        # --- Technical: Hard (5) ---
        ('technical', 'hard', 1, 'What is the "N+1 selects" problem in the context of an ORM?', 'A performance issue where an ORM executes N additional queries to fetch related data for N parent objects.', 'A security vulnerability related to SQL injection.', 'A problem with database indexing.', 'A problem with transaction rollbacks.', 'A'),
        ('technical', 'hard', 1, 'In machine learning, what is overfitting?', 'When a model performs well on training data but poorly on unseen data.', 'When a model performs poorly on both training and unseen data.', 'When a model is too simple to capture the underlying pattern of the data.', 'The process of selecting the best features for a model.', 'A'),
        ('technical', 'hard', 1, 'What is the purpose of a `finally` block in a try-catch-finally statement in Java?', 'It is executed only if an exception occurs.', 'It is executed only if no exception occurs.', 'It is always executed, regardless of whether an exception occurred.', 'It is used to re-throw an exception.', 'C'),
        ('technical', 'hard', 1, 'Describe the concept of database normalization.', 'The process of denormalizing a database for faster reads.', 'The process of organizing columns and tables in a relational database to minimize data redundancy.', 'The process of creating indexes to speed up queries.', 'The process of creating backups of a database.', 'B'),
        ('technical', 'hard', 1, 'What is the difference between TCP and UDP?', 'TCP is connectionless and UDP is connection-oriented.', 'TCP guarantees delivery of packets, while UDP does not.', 'UDP is faster for streaming than TCP.', 'Both B and C are correct.', 'D')
    ]

    # Insert questions into the database
    cursor.executemany("""
        INSERT INTO questions (category, difficulty, min_year, question, option_a, option_b, option_c, option_d, answer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, questions)
    print(f"Inserted {len(questions)} sample questions into the database.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database preparation complete.")

if __name__ == '__main__':
    create_new_db()

