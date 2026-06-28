-- =====================================
-- CREATE DATABASE
-- =====================================

CREATE DATABASE IF NOT EXISTS ai_event_system;

USE ai_event_system;

-- =====================================
-- STUDENTS TABLE
-- =====================================

CREATE TABLE IF NOT EXISTS students (

    id INT AUTO_INCREMENT PRIMARY KEY,

    roll_number VARCHAR(20) UNIQUE NOT NULL,

    student_name VARCHAR(100) NOT NULL,

    email VARCHAR(100) UNIQUE,

    branch VARCHAR(20),

    year VARCHAR(20),

    qr_path VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- =====================================
-- ATTENDANCE TABLE
-- =====================================

CREATE TABLE IF NOT EXISTS attendance (

    attendance_id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,

    scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    status VARCHAR(20) DEFAULT 'Present',

    FOREIGN KEY(student_id)
    REFERENCES students(id)
    ON DELETE CASCADE

);

-- =====================================
-- EVENTS TABLE
-- =====================================

CREATE TABLE IF NOT EXISTS events (

    event_id INT AUTO_INCREMENT PRIMARY KEY,

    event_name VARCHAR(100),

    event_date DATE,

    venue VARCHAR(100),

    venue_limit INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- =====================================
-- PREDICTIONS TABLE
-- =====================================

CREATE TABLE IF NOT EXISTS predictions (

    prediction_id INT AUTO_INCREMENT PRIMARY KEY,

    registrations INT,

    weather VARCHAR(20),

    weekend BOOLEAN,

    celebrity BOOLEAN,

    predicted_attendance INT,

    rice_needed DECIMAL(10,2),

    predicted_waste DECIMAL(10,2),

    peak_hour INT,

    prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- =====================================
-- ADMINS TABLE
-- =====================================

CREATE TABLE IF NOT EXISTS admins (

    admin_id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) UNIQUE,

    password VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- =====================================
-- DEFAULT ADMIN
-- username : admin
-- password : admin123
-- (Change later)
-- =====================================

INSERT INTO admins(username,password)
VALUES(
'admin',
'$2b$12$xxxxxxxxxxxxxxxxxxxxxxxx'
);