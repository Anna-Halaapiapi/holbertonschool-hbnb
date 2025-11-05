-- Scripts for table creation and initial data insert
CREATE DATABASE IF NOT EXISTS hbnb_db;
USE hbnb_db;

-- TABLE CREATION
-- Create User Table
CREATE TABLE `users` (
    `id` CHAR(36),
    `first_name` VARCHAR(255),
    `last_name` VARCHAR(255),
    `email` VARCHAR(255) UNIQUE,
    `password` VARCHAR(255),
    `is_admin` BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (`id`)
);

-- Create Place Table
CREATE TABLE `places` (
    `id` CHAR(36),
    `title` VARCHAR(255),
    `description` TEXT,
    `price` DECIMAL(10,2),
    `latitude` FLOAT,
    `longitude` FLOAT,
    `owner_id` CHAR(36),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
);

-- Create Review Table
CREATE TABLE `reviews` (
    `id` CHAR(36),
    `text` TEXT,
    `rating` INT CHECK (`rating` BETWEEN 1 AND 5),
    `user_id` CHAR(36),
    `place_id` CHAR(36),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
    FOREIGN KEY (`place_id`) REFERENCES `places` (`id`),
    UNIQUE (`user_id`, `place_id`)
);

-- Create Amenity Table
CREATE TABLE `amenities` (
    `id` CHAR(36),
    `name` VARCHAR(255) UNIQUE,
    PRIMARY KEY(`id`)
);

-- Create Place_Amenity Table
CREATE TABLE `place_amenity` (
    `place_id` CHAR(36),
    `amenity_id` CHAR(36),
    PRIMARY KEY (`place_id`, `amenity_id`),
    FOREIGN KEY (`place_id`) REFERENCES `places` (`id`),
    FOREIGN KEY (`amenity_id`) REFERENCES `amenities` (`id`)
);

-- INITIAL DATA INSERT
-- Administrator User, p/w is bcrypt hashed using 12 rounds
INSERT into `users`
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2a$12$J34myE4s28hOlXG8NwUfF.5V9tj/js.QasGVDgBqJjs2RdT1zm0mm',
    TRUE
    );

-- Initial Amenities
-- UUID v4 tool used to gen ids
INSERT into `amenities`
VALUES
    ('e26d5d10-c86d-4e9a-98f6-5cef8508f1e2', 'WiFi'),
    ('d5908763-ca8f-4988-816e-26756f11d86c', 'Swimming Pool'),
    ('fe30f80c-34f8-4a11-a3d8-c7aaf374e649', 'Air Conditioning');
