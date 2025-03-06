CREATE DATABASE IF NOT EXISTS jammin_db;

USE jammin_db;

CREATE TABLE IF NOT EXISTS users (
    user_id CHAR(36) PRIMARY KEY,
    spotify_id VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    age INT CHECK (age >= 13),
    bio TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_settings (
    setting_id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    discoverability BOOLEAN NOT NULL DEFAULT TRUE,
    notifications BOOLEAN NOT NULL DEFAULT TRUE,
    theme_preference VARCHAR(10) CHECK (theme_preference IN ('light', 'dark', 'auto')) DEFAULT 'auto',
    language VARCHAR(20) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS matches (
    match_id CHAR(36) PRIMARY KEY,
    user_1_id CHAR(36) NOT NULL,
    user_2_id CHAR(36) NOT NULL,
    match_score FLOAT,
    status VARCHAR(10) CHECK (status IN ('pending', 'accepted', 'rejected')) DEFAULT NULL,
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_1_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (user_2_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS swipes (
    swipe_id CHAR(36) PRIMARY KEY,
    swiper_id CHAR(36) NOT NULL,
    swiped_id CHAR(36) NOT NULL,
    action VARCHAR(4) CHECK (action IN ('like', 'pass')) DEFAULT NULL,
    swiped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (swiper_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (swiped_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users_music_data (
    user_data_id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    profile_name VARCHAR(100) UNIQUE NOT NULL,
    profile_image VARCHAR(1000) UNIQUE NOT NULL,
    top_songs VARCHAR(300) NOT NULL,
    top_songs_pictures VARCHAR(1000) NOT NULL,
    top_artists VARCHAR(300) NOT NULL,
    top_artists_pictures VARCHAR(1000) NOT NULL,
    top_genres VARCHAR(300) NOT NULL,
    top_genres_pictures VARCHAR(1000) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Test data, remove later
INSERT INTO users (user_id, spotify_id, username, email, password_hash, age, bio)
VALUES 
    (@user1 := UUID(), 'spotify_123', 'testuser1', 'test1@example.com', 'hashedpassword1', 25, 'Music lover'),
    (@user2 := UUID(), 'spotify_456', 'testuser2', 'test2@example.com', 'hashedpassword2', 30, 'I enjoy live concerts');

INSERT INTO user_settings (setting_id, user_id, discoverability, notifications, theme_preference, language)
VALUES 
    (UUID(), @user1, TRUE, FALSE, 'dark', 'en'),
    (UUID(), @user2, FALSE, TRUE, 'light', 'es');

INSERT INTO matches (match_id, user_1_id, user_2_id, match_score, status)
VALUES 
    (UUID(), @user1, @user2, 85.5, 'accepted');

INSERT INTO swipes (swipe_id, swiper_id, swiped_id, action)
VALUES 
    (UUID(), @user1, @user2, 'like'),
    (UUID(), @user2, @user1, 'like');
