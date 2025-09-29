CREATE TABLE IF NOT EXISTS professional_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    fullname TEXT,
    email TEXT,
    phone TEXT,
    branch TEXT,
    cgpa TEXT,
    graduation_year TEXT,
    skills TEXT,
    experience TEXT,
    domain TEXT,
    linkedin TEXT,
    github TEXT
);
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    year INTEGER
);
