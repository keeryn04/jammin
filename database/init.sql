CREATE DATABASE IF NOT EXISTS jammin_db;

USE jammin_db;

CREATE TABLE IF NOT EXISTS users_music_data (
    user_data_id CHAR(36) PRIMARY KEY,
    spotify_id VARCHAR(100) UNIQUE NOT NULL,
    profile_name VARCHAR(100) UNIQUE NOT NULL,
    profile_image VARCHAR(1000) NOT NULL,
    top_songs VARCHAR(300) NOT NULL,
    top_songs_pictures VARCHAR(1000) NOT NULL,
    top_artists VARCHAR(300) NOT NULL,
    top_artists_pictures VARCHAR(1000) NOT NULL,
    top_genres VARCHAR(300) NOT NULL,
    top_genres_pictures VARCHAR(1000) NOT NULL
);
CREATE TABLE IF NOT EXISTS users (
    user_id CHAR(36) PRIMARY KEY,
    user_data_id CHAR(36),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    age INT CHECK (age >= 13),
    bio TEXT DEFAULT NULL,
    gender VARCHAR(10) DEFAULT NULL,
    school VARCHAR(20) DEFAULT NULL,
    occupation VARCHAR(20) DEFAULT NULL,
    looking_for VARCHAR(20) DEFAULT NULL,
    spotify_auth BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_data_id) REFERENCES users_music_data(user_data_id) ON DELETE CASCADE
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
    reasoning CHAR(250),
    status VARCHAR(10) CHECK (status IN ('pending', 'accepted', 'rejected')) DEFAULT NULL,
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_1_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (user_2_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE (user_1_id, user_2_id)
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

-- Test data, remove later
SET @user1 = UUID();
SET @user2 = UUID();

SET @user_data1 = UUID();
SET @user_data2 = UUID();

INSERT INTO users_music_data (
    user_data_id, spotify_id, profile_name, profile_image, 
    top_songs, top_songs_pictures, top_artists, top_artists_pictures, 
    top_genres, top_genres_pictures
) 
VALUES 
    (@user_data1, 'spotify_12345', 'CoolUser', 'https://example.com/profile.jpg',
    'Song1, Song2, Song3', 'https://example.com/song1.jpg, https://example.com/song2.jpg, https://example.com/song3.jpg',
    'Artist1, Artist2, Artist3', 'https://example.com/artist1.jpg, https://example.com/artist2.jpg, https://example.com/artist3.jpg',
    'Rock, Jazz, Pop', 'https://example.com/rock.jpg, https://example.com/jazz.jpg, https://example.com/pop.jpg'),

    (@user_data2, 'spotify_3456', 'BadUser', 'https://example.com/profile2.jpg',
    'Song4, Song5, Song6', 'https://example.com/song4.jpg, https://example.com/song5.jpg, https://example.com/song6.jpg',
    'Artist4, Artist5, Artist6', 'https://example.com/artist4.jpg, https://example.com/artist5.jpg, https://example.com/artist6.jpg',
    'Metal, Blues, EDM', 'https://example.com/metal.jpg, https://example.com/blues.jpg, https://example.com/edm.jpg');

INSERT INTO users (user_id, user_data_id, username, email, password_hash, age, bio, gender, school, occupation, looking_for, spotify_auth) 
VALUES 
    (@user1, @user_data1, 'testuser1', 'test1@example.com', 'hashedpassword1', 25, 'Music lover', 'Male', 'UofC', 'Job', 'love', TRUE),
    (@user2, @user_data2,'testuser2', 'test2@example.com', 'hashedpassword2', 30, 'I enjoy live concerts', 'Female', 'MRU', 'Home Hardware', 'frnd', FALSE);

INSERT INTO user_settings (setting_id, user_id, discoverability, notifications, theme_preference, language)
VALUES 
    (UUID(), @user1, 1, 0, 'dark', 'en'),
    (UUID(), @user2, 0, 1, 'light', 'es');

INSERT INTO matches (match_id, user_1_id, user_2_id, match_score, status)
VALUES 
    (UUID(), @user1, @user2, 85.5, 'accepted');

INSERT INTO swipes (swipe_id, swiper_id, swiped_id, action)
VALUES 
    (UUID(), @user1, @user2, 'like'),
    (UUID(), @user2, @user1, 'like');
