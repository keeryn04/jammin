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
SET @user3 = UUID();
SET @user4 = UUID();
SET @user5 = UUID();
SET @user6 = UUID();

SET @user_data1 = UUID();
SET @user_data2 = UUID();
SET @user_data3 = UUID();
SET @user_data4 = UUID();
SET @user_data5 = UUID();
SET @user_data6 = UUID();

INSERT INTO users_music_data (
    user_data_id, spotify_id, profile_name, profile_image, 
    top_songs, top_songs_pictures, top_artists, top_artists_pictures, 
    top_genres, top_genres_pictures
) 

VALUES 
    (@user_data1, 'spotify_12345', 'Tony Stark', 'https://pbs.twimg.com/profile_images/685915759055351808/ILeBa4II_400x400.png',
    'Igor, Flower Boy, Graduation, Lucid Dreams, Goodbye', 'https://www.billboard.com/wp-content/uploads/media/tyler-the-creator-igor-album-art-2019-billboard-embed.jpg?w=600, https://aimm.edu/hubfs/Blog%20Images/Top%2010%20Album%20Covers%20of%202017/Tyler%20the%20Creator-%20Flower%20boy.jpg, https://s.yimg.com/ny/api/res/1.2/TdT5KvjU14pp8TUgwnvMsw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTk2MA--/https://media.zenfs.com/en/one37pm_956/72d7b3dc8acef1991bb74d8e90c9ceab, https://creativereview.imgix.net/content/uploads/2024/12/tyler-the-creator-chromakopia.jpg?auto=compress,format&q=60&w=1200&h=1189, https://miro.medium.com/v2/resize:fit:681/1*EBOL4lka5QjcYoxj6AHp-g.png',
    'Pink Floyd, Kanye, Drake, Kendrick Lamar', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0DkvCVRV1EJo0u_8ayX_wxGNpL45T4w4GYA&s, https://www.creativeboom.com/upload/articles/db/db1a6b372e7c23636f9b8d88f879a9a815c6825c_1280.jpeg, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTq6btiFtFEfR4FWX2AxXL6iORWzSl7qPVsyg&s, https://www.sleek-mag.com/wp-content/uploads/2016/08/AlbumCovers_Blonde-1200x1200.jpg, https://www.udiscovermusic.com/wp-content/uploads/2022/04/600NWA-3000DPI300RGB1000162059.jpg',
    'Rock, Jazz, Pop', 'https://example.com/rock.jpg, https://example.com/jazz.jpg, https://example.com/pop.jpg'),

    (@user_data2, 'spotify_3456', 'Thor', 'https://upload.wikimedia.org/wikipedia/en/3/3c/Chris_Hemsworth_as_Thor.jpg',
    'Not Igor, Flower Boy, Graduation, Lucid Dreams, Goodbye', 'https://www.billboard.com/wp-content/uploads/media/tyler-the-creator-igor-album-art-2019-billboard-embed.jpg?w=600, https://aimm.edu/hubfs/Blog%20Images/Top%2010%20Album%20Covers%20of%202017/Tyler%20the%20Creator-%20Flower%20boy.jpg, https://s.yimg.com/ny/api/res/1.2/TdT5KvjU14pp8TUgwnvMsw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTk2MA--/https://media.zenfs.com/en/one37pm_956/72d7b3dc8acef1991bb74d8e90c9ceab, https://creativereview.imgix.net/content/uploads/2024/12/tyler-the-creator-chromakopia.jpg?auto=compress,format&q=60&w=1200&h=1189, https://miro.medium.com/v2/resize:fit:681/1*EBOL4lka5QjcYoxj6AHp-g.png',
    'Not Pink Floyd, Kanye, Drake, Kendrick Lamar', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0DkvCVRV1EJo0u_8ayX_wxGNpL45T4w4GYA&s, https://www.creativeboom.com/upload/articles/db/db1a6b372e7c23636f9b8d88f879a9a815c6825c_1280.jpeg, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTq6btiFtFEfR4FWX2AxXL6iORWzSl7qPVsyg&s, https://www.sleek-mag.com/wp-content/uploads/2016/08/AlbumCovers_Blonde-1200x1200.jpg, https://www.udiscovermusic.com/wp-content/uploads/2022/04/600NWA-3000DPI300RGB1000162059.jpg',
    'Metal, Blues, EDM', 'https://example.com/metal.jpg, https://example.com/blues.jpg, https://example.com/edm.jpg'),

    (@user_data3, 'spotify_999', 'Steve Rogers', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQx8tUHYT2ARBwnbBoNLLS-FGawGhHKwJFlag&s',
    'Igor, Flower Boy, Graduation, Lucid Dreams, Goodbye', 'https://www.billboard.com/wp-content/uploads/media/tyler-the-creator-igor-album-art-2019-billboard-embed.jpg?w=600, https://aimm.edu/hubfs/Blog%20Images/Top%2010%20Album%20Covers%20of%202017/Tyler%20the%20Creator-%20Flower%20boy.jpg, https://s.yimg.com/ny/api/res/1.2/TdT5KvjU14pp8TUgwnvMsw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTk2MA--/https://media.zenfs.com/en/one37pm_956/72d7b3dc8acef1991bb74d8e90c9ceab, https://creativereview.imgix.net/content/uploads/2024/12/tyler-the-creator-chromakopia.jpg?auto=compress,format&q=60&w=1200&h=1189, https://miro.medium.com/v2/resize:fit:681/1*EBOL4lka5QjcYoxj6AHp-g.png',
    'Pink Floyd, Kanye, Drake, Kendrick Lamar', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0DkvCVRV1EJo0u_8ayX_wxGNpL45T4w4GYA&s, https://www.creativeboom.com/upload/articles/db/db1a6b372e7c23636f9b8d88f879a9a815c6825c_1280.jpeg, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTq6btiFtFEfR4FWX2AxXL6iORWzSl7qPVsyg&s, https://www.sleek-mag.com/wp-content/uploads/2016/08/AlbumCovers_Blonde-1200x1200.jpg, https://www.udiscovermusic.com/wp-content/uploads/2022/04/600NWA-3000DPI300RGB1000162059.jpg',
    'Rock, Jazz, Pop', 'https://example.com/rock.jpg, https://example.com/jazz.jpg, https://example.com/pop.jpg'),

    (@user_data4, 'spotify_lover6', 'Bruce Banner', 'https://www.themarysue.com/wp-content/uploads/2021/10/Mark-Ruffalo-Bruce-Banner.jpeg?fit=1200%2C742',
    'Igor, Flower Boy, Graduation, Lucid Dreams, Goodbye', 'https://www.billboard.com/wp-content/uploads/media/tyler-the-creator-igor-album-art-2019-billboard-embed.jpg?w=600, https://aimm.edu/hubfs/Blog%20Images/Top%2010%20Album%20Covers%20of%202017/Tyler%20the%20Creator-%20Flower%20boy.jpg, https://s.yimg.com/ny/api/res/1.2/TdT5KvjU14pp8TUgwnvMsw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTk2MA--/https://media.zenfs.com/en/one37pm_956/72d7b3dc8acef1991bb74d8e90c9ceab, https://creativereview.imgix.net/content/uploads/2024/12/tyler-the-creator-chromakopia.jpg?auto=compress,format&q=60&w=1200&h=1189, https://miro.medium.com/v2/resize:fit:681/1*EBOL4lka5QjcYoxj6AHp-g.png',
    'Pink Floyd, Kanye, Drake, Kendrick Lamar', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0DkvCVRV1EJo0u_8ayX_wxGNpL45T4w4GYA&s, https://www.creativeboom.com/upload/articles/db/db1a6b372e7c23636f9b8d88f879a9a815c6825c_1280.jpeg, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTq6btiFtFEfR4FWX2AxXL6iORWzSl7qPVsyg&s, https://www.sleek-mag.com/wp-content/uploads/2016/08/AlbumCovers_Blonde-1200x1200.jpg, https://www.udiscovermusic.com/wp-content/uploads/2022/04/600NWA-3000DPI300RGB1000162059.jpg',
    'Metal, Blues, EDM', 'https://example.com/metal.jpg, https://example.com/blues.jpg, https://example.com/edm.jpg'),

    (@user_data5, 'spotify_666', 'Natasha Romanoff', 'https://m.media-amazon.com/images/I/81Jgy1tfvcL.jpg',
    'Igor, Flower Boy, Graduation, Lucid Dreams, Goodbye', 'https://www.billboard.com/wp-content/uploads/media/tyler-the-creator-igor-album-art-2019-billboard-embed.jpg?w=600, https://aimm.edu/hubfs/Blog%20Images/Top%2010%20Album%20Covers%20of%202017/Tyler%20the%20Creator-%20Flower%20boy.jpg, https://s.yimg.com/ny/api/res/1.2/TdT5KvjU14pp8TUgwnvMsw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTk2MA--/https://media.zenfs.com/en/one37pm_956/72d7b3dc8acef1991bb74d8e90c9ceab, https://creativereview.imgix.net/content/uploads/2024/12/tyler-the-creator-chromakopia.jpg?auto=compress,format&q=60&w=1200&h=1189, https://miro.medium.com/v2/resize:fit:681/1*EBOL4lka5QjcYoxj6AHp-g.png',
    'Pink Floyd, Kanye, Drake, Kendrick Lamar', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0DkvCVRV1EJo0u_8ayX_wxGNpL45T4w4GYA&s, https://www.creativeboom.com/upload/articles/db/db1a6b372e7c23636f9b8d88f879a9a815c6825c_1280.jpeg, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTq6btiFtFEfR4FWX2AxXL6iORWzSl7qPVsyg&s, https://www.sleek-mag.com/wp-content/uploads/2016/08/AlbumCovers_Blonde-1200x1200.jpg, https://www.udiscovermusic.com/wp-content/uploads/2022/04/600NWA-3000DPI300RGB1000162059.jpg',
    'Rock, Jazz, Pop', 'https://example.com/rock.jpg, https://example.com/jazz.jpg, https://example.com/pop.jpg'),

    (@user_data6, 'spotify_lover3', 'Clint Barton', 'https://www.hollywoodreporter.com/wp-content/uploads/2021/07/MCDAVEN_EC081-H-2021.jpg?w=1296&h=730&crop=1',
    'Igor, Flower Boy, Graduation, Lucid Dreams, Goodbye', 'https://www.billboard.com/wp-content/uploads/media/tyler-the-creator-igor-album-art-2019-billboard-embed.jpg?w=600, https://aimm.edu/hubfs/Blog%20Images/Top%2010%20Album%20Covers%20of%202017/Tyler%20the%20Creator-%20Flower%20boy.jpg, https://s.yimg.com/ny/api/res/1.2/TdT5KvjU14pp8TUgwnvMsw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTk2MA--/https://media.zenfs.com/en/one37pm_956/72d7b3dc8acef1991bb74d8e90c9ceab, https://creativereview.imgix.net/content/uploads/2024/12/tyler-the-creator-chromakopia.jpg?auto=compress,format&q=60&w=1200&h=1189, https://miro.medium.com/v2/resize:fit:681/1*EBOL4lka5QjcYoxj6AHp-g.png',
    'Pink Floyd, Kanye, Drake, Kendrick Lamar', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0DkvCVRV1EJo0u_8ayX_wxGNpL45T4w4GYA&s, https://www.creativeboom.com/upload/articles/db/db1a6b372e7c23636f9b8d88f879a9a815c6825c_1280.jpeg, https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTq6btiFtFEfR4FWX2AxXL6iORWzSl7qPVsyg&s, https://www.sleek-mag.com/wp-content/uploads/2016/08/AlbumCovers_Blonde-1200x1200.jpg, https://www.udiscovermusic.com/wp-content/uploads/2022/04/600NWA-3000DPI300RGB1000162059.jpg',
    'Metal, Blues, EDM', 'https://example.com/metal.jpg, https://example.com/blues.jpg, https://example.com/edm.jpg');

INSERT INTO users (user_id, user_data_id, username, email, password_hash, age, bio, gender, school, occupation, looking_for, spotify_auth) 
VALUES 
    (@user1, @user_data1, 'testuser1', 'test1@example.com', 'hashedpassword1', 25, 'Music lover', 'Male', 'UofC', 'Job', 'love', TRUE),
    (@user2, @user_data2,'testuser2', 'test2@example.com', 'hashedpassword2', 30, 'I enjoy live concerts', 'Female', 'MRU', 'Home Hardware', 'frnd', FALSE),
    (@user3, @user_data3,'testuser3', 'test3@example.com', 'hashedpassword3', 26, 'I like rap', 'Female', 'MRU', 'Home Hardware', 'frnd', FALSE),
    (@user4, @user_data4,'testuser4', 'test4@example.com', 'hashedpassword4', 26, 'I like rap', 'Female', 'MRU', 'Home Hardware', 'frnd', FALSE),
    (@user5, @user_data5,'testuser5', 'test5@example.com', 'hashedpassword3', 26, 'I like rap', 'Female', 'MRU', 'Home Hardware', 'frnd', FALSE),
    (@user6, @user_data6,'testuser6', 'test6@example.com', 'hashedpassword4', 26, 'I like rap', 'Female', 'MRU', 'Home Hardware', 'frnd', FALSE);

INSERT INTO user_settings (setting_id, user_id, discoverability, notifications, theme_preference, language)
VALUES 
    (UUID(), @user1, 1, 0, 'dark', 'en'),
    (UUID(), @user2, 0, 1, 'light', 'es'),
    (UUID(), @user3, 1, 0, 'dark', 'en'),
    (UUID(), @user4, 0, 1, 'light', 'es');

INSERT INTO matches (match_id, user_1_id, user_2_id, match_score, status)
VALUES 
    (UUID(), @user1, @user2, 85.5, 'accepted');

INSERT INTO swipes (swipe_id, swiper_id, swiped_id, action)
VALUES 
    (UUID(), @user1, @user2, 'like'),
    (UUID(), @user2, @user1, 'like');
