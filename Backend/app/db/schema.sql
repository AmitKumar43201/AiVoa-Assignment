CREATE database assignment;

USE assignment;

CREATE TABLE hcp_master (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE interactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hcp_id INT NOT NULL,
    hcp_name VARCHAR(255) NOT NULL,
    interaction_type VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    sentiment ENUM('positive', 'neutral', 'negative') DEFAULT 'neutral',
    outcomes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (hcp_id) REFERENCES hcp_master(id)
);

CREATE TABLE followUps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interaction_id INT NOT NULL,
    follow_up TEXT NOT NULL,
    FOREIGN KEY (interaction_id) REFERENCES interactions(id) ON DELETE CASCADE
);

CREATE TABLE attendees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interaction_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    FOREIGN KEY (interaction_id) REFERENCES interactions(id) ON DELETE CASCADE
);

CREATE TABLE topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interaction_id INT NOT NULL,
    topic TEXT NOT NULL,
    FOREIGN KEY (interaction_id) REFERENCES interactions(id) ON DELETE CASCADE
);

CREATE TABLE materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interaction_id INT NOT NULL,
    material_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (interaction_id) REFERENCES interactions(id) ON DELETE CASCADE
);

CREATE TABLE samples (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interaction_id INT NOT NULL,
    sample_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (interaction_id) REFERENCES interactions(id) ON DELETE CASCADE
);

