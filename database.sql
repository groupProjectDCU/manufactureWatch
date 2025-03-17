CREATE DATABASE factory_machinery;
USE factory_machinery;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Technician', 'Repair', 'Manager') DEFAULT 'Technician'
);

CREATE TABLE machinery (
    machine_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    model VARCHAR(255) NOT NULL,
    status ENUM('OK', 'Warning', 'Fault') DEFAULT 'OK',
    priority INT DEFAULT 0,
    campus VARCHAR(255) NOT NULL,
    building VARCHAR(255) NOT NULL,
    floor VARCHAR(255) NOT NULL,
    room VARCHAR(255) NOT NULL,
);

CREATE TABLE fault_cases (
    case_id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id INT,
    created_by INT,
    status ENUM('Open', 'Resolved') DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    FOREIGN KEY (machine_id) REFERENCES machinery(machine_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE fault_notes (
    note_id INT AUTO_INCREMENT PRIMARY KEY,
    case_id INT,
    user_id INT,
    note TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES fault_cases(case_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE warnings (
    warning_id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id INT,
    message VARCHAR(255) NOT NULL,
    added_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (machine_id) REFERENCES machinery(machine_id) ON DELETE CASCADE,
    FOREIGN KEY (added_by) REFERENCES users(user_id) ON DELETE SET NULL
);
