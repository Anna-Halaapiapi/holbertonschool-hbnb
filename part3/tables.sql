-- Scripts for database and table creation
-- DATABASE CREATION
CREATE DATABASE IF NOT EXISTS hbnb_db;
USE hbnb_db;

-- TABLE CREATION
-- Create User Table
CREATE TABLE IF NOT EXISTS `users` (
    `id` CHAR(36),
    `first_name` VARCHAR(255),
    `last_name` VARCHAR(255),
    `email` VARCHAR(255) UNIQUE,
    `password` VARCHAR(255),
    `is_admin` BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (`id`)
);

-- Create Place Table
CREATE TABLE IF NOT EXISTS `places` (
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
CREATE TABLE IF NOT EXISTS `reviews` (
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
CREATE TABLE IF NOT EXISTS `amenities` (
    `id` CHAR(36),
    `name` VARCHAR(255) UNIQUE,
    PRIMARY KEY(`id`)
);

-- Create Place_Amenity Table
CREATE TABLE IF NOT EXISTS `place_amenity` (
    `place_id` CHAR(36),
    `amenity_id` CHAR(36),
    PRIMARY KEY (`place_id`, `amenity_id`),
    FOREIGN KEY (`place_id`) REFERENCES `places` (`id`),
    FOREIGN KEY (`amenity_id`) REFERENCES `amenities` (`id`)
);
