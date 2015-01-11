DROP TABLE IF EXISTS users;

CREATE TABLE users (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    passwordhash TEXT NOT NULL
);

DROP TABLE IF EXISTS submissions;

CREATE TABLE submissions (
    userid INTEGER PRIMARY KEY,
    submissionid INTEGER,
    filepath TEXT NOT NULL,
    time_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grade_received NUMERIC DEFAULT NULL
);

DROP TABLE IF EXISTS actions;

CREATE TABLE actions (
    userid INTEGER PRIMARY KEY,
    action TEXT NOT NULL,
    time_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS assignments;

CREATE TABLE assignments(
    assignmentid INTEGER PRIMARY KEY AUTOINCREMENT,
    due_date DATE NOT NULL,
    point_value INTEGER NOT NULL
);