CREATE DATABASE factory_machinery;
USE factory_machinery;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) UNIQUE NOT NULL,
    last_name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL
    password VARCHAR(255) NOT NULL,
    role ENUM('Technician', 'Repair', 'Manager','View-only') DEFAULT 'View-only'
);

CREATE TABLE machinery (
    machine_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    model VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    status ENUM('OK', 'Warning', 'Fault') DEFAULT 'OK',
    priority INT DEFAULT 0,
);

CREATE TABLE machinery_assigment (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    is_active ENUM('True','False') DEFAULT 'True',
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    machine_id INT,
    FOREIGN KEY (machine_id) REFERENCES machinery(machine_id) ON DELETE CASCADE,
    );

CREATE TABLE collections (
    collection_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    );

CREATE TABLE machinery_collections (
    mach_coll_id INT AUTO_INCREMENT PRIMARY KEY,
    collection_id INT,
    machinery_id INT,
    FOREIGN KEY (machine_id) REFERENCES machinery(machine_id) ON DELETE CASCADE,
    FOREIGN KEY (collection_id) REFERENCES collections(collections_id) ON DELETE CASCADE,
    );

CREATE TABLE fault_cases (
    case_id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id INT,
    created_by INT,
    status ENUM('Open', 'In progress', 'Resolved') DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    resolved_by INT NULL,
    FOREIGN KEY (machine_id) REFERENCES machinery(machine_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (resolved_by) REFERENCES users(user_id) ON DELETE SET NULL

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
    is_active ENUM('True','False') DEFAULT 'False',
    resolved_at TIMESTAMP NULL,
    resolved_by INT NULL,
    machine_id INT,
    message VARCHAR(255) NOT NULL,
    added_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (machine_id) REFERENCES machinery(machine_id) ON DELETE CASCADE,
    FOREIGN KEY (added_by) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (resolved_by) REFERENCES users(user_id) ON DELETE SET NULL
);
