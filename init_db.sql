CREATE DATABASE IF NOT EXISTS lost_and_found CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE lost_and_found;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(150),
  phone VARCHAR(25),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  category VARCHAR(100),
  status ENUM('lost','found','resolved') NOT NULL DEFAULT 'lost',
  location VARCHAR(255),
  event_date DATE,
  image_path VARCHAR(500),
  reporter_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (reporter_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_title_desc ON items(title(100), description(255));
CREATE INDEX idx_status ON items(status);
