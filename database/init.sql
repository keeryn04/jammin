CREATE DATABASE IF NOT EXISTS jammin_db;

USE jammin_db;

CREATE TABLE IF NOT EXISTS songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    release_year INT,
    genre VARCHAR(100),
    duration_seconds INT
);

-- Generic test data
INSERT INTO songs (title, artist, release_year, genre, duration_seconds)
VALUES ('Song 1', 'Artist 1', 2022, 'Pop', 180);
