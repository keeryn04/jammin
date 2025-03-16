-- SQLBook: Code
CREATE DATABASE IF NOT EXISTS jammin_db;

USE jammin_db;

CREATE TABLE IF NOT EXISTS users_music_data (
    user_data_id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    spotify_id VARCHAR(100) UNIQUE NOT NULL,
    profile_name VARCHAR(100) UNIQUE NOT NULL,
    profile_image VARCHAR(TEXT) UNIQUE NOT NULL,
    top_songs VARCHAR(300) NOT NULL,
    top_songs_pictures VARCHAR(TEXT) NOT NULL,
    top_artists VARCHAR(300) NOT NULL,
    top_artists_pictures VARCHAR(TEXT) NOT NULL,
    top_genres VARCHAR(300) NOT NULL,
    top_genres_pictures VARCHAR(TEXT) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
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
    FOREIGN KEY (user_1_id) REFERENCES users_music_data(user_data_id) ON DELETE CASCADE,
    FOREIGN KEY (user_2_id) REFERENCES users_music_data(user_data_id) ON DELETE CASCADE,
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
SET @user7 = UUID();
SET @user8 = UUID();
SET @user9 = UUID();
SET @user10 = UUID();
SET @user11 = UUID();
SET @user12 = UUID();

SET @user_data1 = UUID();
SET @user_data2 = UUID();
SET @user_data3 = UUID();
SET @user_data4 = UUID();
SET @user_data5 = UUID();
SET @user_data6 = UUID();
SET @user_data7 = UUID();
SET @user_data8 = UUID();
SET @user_data9 = UUID();
SET @user_data10 = UUID();
SET @user_data11 = UUID();
SET @user_data12 = UUID();

INSERT INTO users_music_data (
    user_data_id, spotify_id, profile_name, profile_image, 
    top_songs, top_songs_pictures, top_artists, top_artists_pictures, 
    top_genres, top_genres_pictures
) 

VALUES 
    (@user_data1, 'spotify_12345', 'Tony Stark', 'https://pbs.twimg.com/profile_images/685915759055351808/ILeBa4II_400x400.png',
    'Bohemian Rhapsody, Blinding Lights, Hotel California, Shape of You, Stairway to Heaven', 'https://example.com/bohemian.jpg, https://example.com/blinding.jpg, https://example.com/hotel.jpg, https://example.com/shape.jpg, https://example.com/stairway.jpg',
    'Queen, The Weeknd, Eagles, Ed Sheeran, Led Zeppelin', 'https://example.com/queen.jpg, https://example.com/weeknd.jpg, https://example.com/eagles.jpg, https://example.com/ed.jpg, https://example.com/zeppelin.jpg',
    'Rock, Pop, Classic Rock, Alternative, Electronic', 'https://example.com/rock.jpg, https://example.com/pop.jpg, https://example.com/classicrock.jpg, https://example.com/alternative.jpg, https://example.com/electronic.jpg'),

    (@user_data2, 'spotify_3456', 'Thor', 'https://upload.wikimedia.org/wikipedia/en/3/3c/Chris_Hemsworth_as_Thor.jpg',
        'Thunderstruck, Uptown Funk, Smells Like Teen Spirit, Rolling in the Deep, Shape of You', 'https://example.com/thunderstruck.jpg, https://example.com/uptown.jpg, https://example.com/smells.jpg, https://example.com/rolling.jpg, https://example.com/shape.jpg',
        'AC/DC, Mark Ronson ft. Bruno Mars, Nirvana, Adele, Ed Sheeran', 'https://example.com/acdc.jpg, https://example.com/mark.jpg, https://example.com/nirvana.jpg, https://example.com/adele.jpg, https://example.com/ed.jpg',
        'Hard Rock, Funk, Pop, Grunge, Soul', 'https://example.com/hardrock.jpg, https://example.com/funk.jpg, https://example.com/pop.jpg, https://example.com/grunge.jpg, https://example.com/soul.jpg'),

    (@user_data3, 'spotify_999', 'Steve Rogers', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQx8tUHYT2ARBwnbBoNLLS-FGawGhHKwJFlag&s',
        'Humble, Bad Guy, Old Town Road, Someone Like You, Shape of You', 'https://example.com/humble.jpg, https://example.com/badguy.jpg, https://example.com/oldtown.jpg, https://example.com/someone.jpg, https://example.com/shape.jpg',
        'Kendrick Lamar, Billie Eilish, Lil Nas X, Adele, Ed Sheeran', 'https://example.com/kendrick.jpg, https://example.com/billie.jpg, https://example.com/lilnas.jpg, https://example.com/adele.jpg, https://example.com/ed.jpg',
        'Hip-Hop, Pop, Country Rap, Indie, Electronic', 'https://example.com/hiphop.jpg, https://example.com/pop.jpg, https://example.com/countryrap.jpg, https://example.com/indie.jpg, https://example.com/electronic.jpg'),

    (@user_data4, 'spotify_lover6', 'Bruce Banner', 'https://www.themarysue.com/wp-content/uploads/2021/10/Mark-Ruffalo-Bruce-Banner.jpeg?fit=1200%2C742',
        'Radioactive, Believer, Demons, Thunder, Rolling in the Deep', 'https://example.com/radioactive.jpg, https://example.com/believer.jpg, https://example.com/demons.jpg, https://example.com/thunder.jpg, https://example.com/rolling.jpg',
        'Imagine Dragons, Adele, Ed Sheeran, Queen, The Weeknd', 'https://example.com/imaginedragons.jpg, https://example.com/adele.jpg, https://example.com/ed.jpg, https://example.com/queen.jpg, https://example.com/weeknd.jpg',
        'Alternative Rock, Pop Rock, Rock, Electronic, Soul', 'https://example.com/alternativerock.jpg, https://example.com/poprock.jpg, https://example.com/rock.jpg, https://example.com/electronic.jpg, https://example.com/soul.jpg'),

    (@user_data5, 'spotify_666', 'Natasha Romanoff', 'https://m.media-amazon.com/images/I/81Jgy1tfvcL.jpg',
        'Shallow, Always Remember Us This Way, I Will Always Love You, Rolling in the Deep, Someone Like You', 'https://example.com/shallow.jpg, https://example.com/always.jpg, https://example.com/alwayslove.jpg, https://example.com/rolling.jpg, https://example.com/someone.jpg',
        'Lady Gaga, Whitney Houston, Adele, Ed Sheeran, The Weeknd', 'https://example.com/ladygaga.jpg, https://example.com/whitney.jpg, https://example.com/adele.jpg, https://example.com/ed.jpg, https://example.com/weeknd.jpg',
        'Pop, Ballad, Soul, Electronic, R&B', 'https://example.com/pop.jpg, https://example.com/ballad.jpg, https://example.com/soul.jpg, https://example.com/electronic.jpg, https://example.com/rnb.jpg'),

    (@user_data6, 'spotify_lover3', 'Clint Barton', 'https://www.hollywoodreporter.com/wp-content/uploads/2021/07/MCDAVEN_EC081-H-2021.jpg?w=1296&h=730&crop=1',
        'Take On Me, Africa, Take Me Home Country Roads, Eye of the Tiger, Shape of You', 'https://example.com/takeonme.jpg, https://example.com/africa.jpg, https://example.com/countryroads.jpg, https://example.com/eye.jpg, https://example.com/shape.jpg',
        'a-ha, Toto, John Denver, Survivor, Ed Sheeran', 'https://example.com/aha.jpg, https://example.com/toto.jpg, https://example.com/johndenver.jpg, https://example.com/survivor.jpg, https://example.com/ed.jpg',
        'Synth-pop, Soft Rock, Pop, Country, Arena Rock', 'https://example.com/synthpop.jpg, https://example.com/softrock.jpg, https://example.com/pop.jpg, https://example.com/country.jpg, https://example.com/arenarock.jpg'),

    (@user_data7, 'spotify_2024', 'Keeryn Johnson', 'https://media.licdn.com/dms/image/v2/D5603AQFTlUd5G6X5Pw/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1677177020737?e=1747267200&v=beta&t=iI5bl_AtAR8cglDuLjHDoaqHLh1mfZp8gKjhDCFtZFU',
        'Sicko Mode, Gods Plan, In My Feelings, Hotline Bling, Shape of You', 'https://example.com/sicko.jpg, https://example.com/godsplan.jpg, https://example.com/feelings.jpg, https://example.com/hotline.jpg, https://example.com/shape.jpg',
        'Drake, Ed Sheeran, The Weeknd, Kendrick Lamar, Bruno Mars', 'https://example.com/drake.jpg, https://example.com/ed.jpg, https://example.com/weeknd.jpg, https://example.com/kendrick.jpg, https://example.com/bruno.jpg',
        'Hip-Hop, R&B, Pop, Electronic, Funk', 'https://example.com/hiphop.jpg, https://example.com/rnb.jpg, https://example.com/pop.jpg, https://example.com/electronic.jpg, https://example.com/funk.jpg'),

    (@user_data8, 'spotify_2023', 'Sam Haque', 'https://instagram.fyyc7-1.fna.fbcdn.net/v/t51.2885-19/457871978_867794188190980_4331431307544718980_n.jpg?_nc_ht=instagram.fyyc7-1.fna.fbcdn.net&_nc_cat=104&_nc_oc=Q6cZ2AHcgyLEEGVfTZL9xntDnNLxxbczEZVulXtUAYGzuxkJYftQrnCYMGPdUPpX0Zb0Jy7BQ3Xhq9CxwmvVpsMeZfzW&_nc_ohc=gFaxQ9Tzn2kQ7kNvgHNQold&_nc_gid=92207a7f7ad3492796a4565435d8ee80&edm=APoiHPcBAAAA&ccb=7-5&oh=00_AYHXxZ6N9eIPwQy1vrbUEDBUYMxRcRWTH-dtmeZW5No8Kw&oe=67D80A96&_nc_sid=22de04',
        'Shape of You, Perfect, Thinking Out Loud, Castle on the Hill, Rolling in the Deep', 'https://example.com/shape.jpg, https://example.com/perfect.jpg, https://example.com/thinking.jpg, https://example.com/castle.jpg, https://example.com/rolling.jpg',
        'Ed Sheeran, Adele, The Weeknd, Queen, Bruno Mars', 'https://example.com/ed.jpg, https://example.com/adele.jpg, https://example.com/weeknd.jpg, https://example.com/queen.jpg, https://example.com/bruno.jpg',
        'Pop, Folk-pop, Soul, Rock, Electronic', 'https://example.com/pop.jpg, https://example.com/folkpop.jpg, https://example.com/soul.jpg, https://example.com/rock.jpg, https://example.com/electronic.jpg'),

    (@user_data9, 'spotify_2025', 'Evan Mann', 'https://media.licdn.com/dms/image/v2/D5603AQEvQwUZ1jKFiw/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1727207825228?e=1747267200&v=beta&t=YoHlj7WqscoSJhH-g_Y_tYtaSg-3dyGyd-8kfz_Za2Q',
        'All of Me, Say Something, Stay With Me, Thinking Out Loud, Shape of You', 'https://example.com/allofme.jpg, https://example.com/saysomething.jpg, https://example.com/staywithme.jpg, https://example.com/thinking.jpg, https://example.com/shape.jpg',
        'John Legend, A Great Big World, Sam Smith, Ed Sheeran, Adele', 'https://example.com/johnlegend.jpg, https://example.com/greatbigworld.jpg, https://example.com/samsmith.jpg, https://example.com/ed.jpg, https://example.com/adele.jpg',
        'Pop, Soul, Ballad, R&B, Electronic', 'https://example.com/pop.jpg, https://example.com/soul.jpg, https://example.com/ballad.jpg, https://example.com/rnb.jpg, https://example.com/electronic.jpg'),

    (@user_data10, 'spotify_2026', 'Elias Poitras', 'https://media.licdn.com/dms/image/v2/D5603AQFTlUd5G6X5Pw/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1677177020737?e=1747267200&v=beta&t=iI5bl_AtAR8cglDuLjHDoaqHLh1mfZp8gKjhDCFtZFU',
        'Uptown Funk, 24K Magic, Thats What I Like, Finesse, Shape of You', 'https://example.com/uptown.jpg, https://example.com/24kmagic.jpg, https://example.com/like.jpg, https://example.com/finesse.jpg, https://example.com/shape.jpg',
        'Bruno Mars, Ed Sheeran, The Weeknd, Drake, Kendrick Lamar', 'https://example.com/bruno.jpg, https://example.com/ed.jpg, https://example.com/weeknd.jpg, https://example.com/drake.jpg, https://example.com/kendrick.jpg',
        'Funk, R&B, Pop, Hip-Hop, Electronic', 'https://example.com/funk.jpg, https://example.com/rnb.jpg, https://example.com/pop.jpg, https://example.com/hiphop.jpg, https://example.com/electronic.jpg'),

    (@user_data11, 'spotify_2027', 'Ryan', 'https://instagram.fyyc7-1.fna.fbcdn.net/v/t51.2885-19/457871978_867794188190980_4331431307544718980_n.jpg?_nc_ht=instagram.fyyc7-1.fna.fbcdn.net&_nc_cat=104&_nc_oc=Q6cZ2AHcgyLEEGVfTZL9xntDnNLxxbczEZVulXtUAYGzuxkJYftQrnCYMGPdUPpX0Zb0Jy7BQ3Xhq9CxwmvVpsMeZfzW&_nc_ohc=gFaxQ9Tzn2kQ7kNvgHNQold&_nc_gid=92207a7f7ad3492796a4565435d8ee80&edm=APoiHPcBAAAA&ccb=7-5&oh=00_AYHXxZ6N9eIPwQy1vrbUEDBUYMxRcRWTH-dtmeZW5No8Kw&oe=67D80A96&_nc_sid=22de04',
        'Havana, Señorita, Dont Go Yet, Bam Bam, Shape of You', 'https://example.com/havana.jpg, https://example.com/senorita.jpg, https://example.com/dontgo.jpg, https://example.com/bambam.jpg, https://example.com/shape.jpg',
        'Camila Cabello, Ed Sheeran, Bruno Mars, The Weeknd, Adele', 'https://example.com/camila.jpg, https://example.com/ed.jpg, https://example.com/bruno.jpg, https://example.com/weeknd.jpg, https://example.com/adele.jpg',
        'Pop, Latin Pop, R&B, Electronic, Soul', 'https://example.com/pop.jpg, https://example.com/latinpop.jpg, https://example.com/rnb.jpg, https://example.com/electronic.jpg, https://example.com/soul.jpg'),

    (@user_data12, 'spotify_2028', 'Petr', 'https://instagram.fyyc7-1.fna.fbcdn.net/v/t51.2885-19/457871978_867794188190980_4331431307544718980_n.jpg?_nc_ht=instagram.fyyc7-1.fna.fbcdn.net&_nc_cat=104&_nc_oc=Q6cZ2AHcgyLEEGVfTZL9xntDnNLxxbczEZVulXtUAYGzuxkJYftQrnCYMGPdUPpX0Zb0Jy7BQ3Xhq9CxwmvVpsMeZfzW&_nc_ohc=gFaxQ9Tzn2kQ7kNvgHNQold&_nc_gid=92207a7f7ad3492796a4565435d8ee80&edm=APoiHPcBAAAA&ccb=7-5&oh=00_AYHXxZ6N9eIPwQy1vrbUEDBUYMxRcRWTH-dtmeZW5No8Kw&oe=67D80A96&_nc_sid=22de04',
        'Despacito, Échame La Culpa, Vives, Bailando, Love Yourself', 'https://example.com/despacito.jpg, https://example.com/culpa.jpg, https://example.com/vives.jpg, https://example.com/bailando.jpg, https://example.com/shape.jpg',
        'Luis Fonsi, Daddy Yankee, Justine Bieber, Bruno Mars, The Weeknd', 'https://example.com/luis.jpg, https://example.com/daddy.jpg, https://example.com/ed.jpg, https://example.com/bruno.jpg, https://example.com/weeknd.jpg',
        'Latin Pop, Reggaeton, Pop, R&B, Electronic', 'https://example.com/latinpop.jpg, https://example.com/reggaeton.jpg, https://example.com/pop.jpg, https://example.com/rnb.jpg, https://example.com/electronic.jpg');

INSERT INTO users (user_id, user_data_id, username, email, password_hash, age, bio, gender, school, occupation, looking_for, spotify_auth) 
VALUES 
    (@user1, @user_data1, 'testuser1', 'test1@example.com', 'hashedpassword1', 25, 'Music lover', 'Male', 'UofC', 'Job', 'love', TRUE),
    (@user2, @user_data2,'testuser2', 'test2@example.com', 'hashedpassword2', 30, 'I enjoy live concerts', 'Female', 'MRU', 'Home Hardware', 'frnd', FALSE),
    (@user3, @user_data3,'testuser3', 'test3@example.com', 'hashedpassword3', 26, 'I like rap', 'Female', 'MRU', 'Home Hardware', 'frnd', FALSE),
    (@user4, @user_data4,'testuser4', 'test4@example.com', 'hashedpassword4', 26, 'I like rap', 'Female', 'MRU', 'Home Hardware', 'frnd', FALSE),
    (@user5, @user_data5,'testuser5', 'test5@example.com', 'hashedpassword3', 26, 'I like rap', 'Female', 'MRU', 'Home Hardware', 'frnd', FALSE),
    (@user6, @user_data6,'testuser6', 'test6@example.com', 'hashedpassword4', 26, 'I like rap', 'Female', 'MRU', 'Home Hardware', 'frnd', FALSE),
    (@user7, @user_data7,'testuser7', 'test7@example.com', 'hashedpassword3', 20, 'I like arcane', 'Male', 'UofC', 'McDonalds', 'frnd', FALSE),
    (@user8, @user_data8,'testuser8', 'test8@example.com', 'hashedpassword4', 20, 'I like rap', 'Male', 'Harvard', 'Amazon', 'lovepls', TRUE),
    (@user9, @user_data9,'testuser9', 'test9@example.com', 'hashedpassword3', 21, 'I like laufey', 'Male', 'UofC', 'Tim Hortons', 'frnd', FALSE),
    (@user10, @user_data10,'testuser10', 'test10@example.com', 'hashedpassword3', 20, 'I like arcane', 'Male', 'UofC', 'McDonalds', 'frnd', FALSE),
    (@user11, @user_data11,'testuser11', 'test11@example.com', 'hashedpassword4', 20, 'I like rap', 'Male', 'Harvard', 'Amazon', 'lovepls', TRUE),
    (@user12, @user_data12,'testuser12', 'test12@example.com', 'hashedpassword3', 21, 'I like laufey', 'Male', 'UofC', 'Tim Hortons', 'frnd', FALSE);

INSERT INTO user_settings (setting_id, user_id, discoverability, notifications, theme_preference, language)
VALUES 
    (UUID(), @user1, 1, 0, 'dark', 'en'),
    (UUID(), @user2, 0, 1, 'light', 'es'),
    (UUID(), @user3, 1, 0, 'dark', 'en'),
    (UUID(), @user4, 0, 1, 'light', 'es');

INSERT INTO matches (match_id, user_1_id, user_2_id, match_score, status)
VALUES 
    (UUID(), @user_data1, @user_data2, 85.5, 'accepted');

INSERT INTO swipes (swipe_id, swiper_id, swiped_id, action)
VALUES 
    (UUID(), @user1, @user2, 'like'),
    (UUID(), @user2, @user1, 'like');
