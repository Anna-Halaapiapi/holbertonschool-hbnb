# 🐞 Task 9 - SQL Script Testing
**Intro**  
The purpose of this document is to outline the testing that was performed for Part 3, Task 9 of the HBnB project, along with testing outcomes.

**Objectives**  
The goals were to verify:  
* Task requirements were adhered to strictly
* the SQL scripts to generate the full database schema matched task requirements
* the initial data was inserted into the database per task requirements
* CRUD operations function as expected to ensure data integrity

**Part One - Testing Database and Table Creation**  
This part verifies that the database and tables are created correctly. The constraints and relationships of all tables are also confirmed against the specifications of the task in this section.

**Part Two : Testing Initial Data Insertion**  
This part verifies that the initial data is inserted into the database per task requirements, the admin user's password is stored in hashed format, and that the admin user's 'is_admin' column is set to TRUE.

**Part Three: Testing CRUD functionality on all tables**
This part verifies that CRUD (Create, Read, Update, Delete) operations function as expected for all tables in the database (users, reviews, amenities, places, place_amenity tables). Testing of happy paths are used to simulate valid CRUD operations, whereas testing of negative paths are used to simulate invalid CRUD operations.

**Outcome**  
All tests returned the expected results, indicating that the SQL scripts have been created correctly.

## PART ONE: TABLE CREATION
The aim of this test is to verify:  
a) the database is created successfully  
b) the tables in the database are created successfully, with all constraints and relationships in place
### Step 1: Enter MySQL
```bash
mysql -u root
```
### Step 2: Execute tables.sql
```sql
SOURCE /path/to/tables.sql;
```
### Step 3: Check tables are created
```sql
USE hbnb_db;
SHOW TABLES;
```
**Expected Result:**
```
+-------------------+
| Tables_in_hbnb_db |
+-------------------+
| amenities         |
| place_amenity     |
| places            |
| reviews           |
| users             |
+-------------------+
```
### Step 4: Check columns, constraints, relationships in tables
```sql
SHOW CREATE TABLE users\G
SHOW CREATE TABLE places\G
SHOW CREATE TABLE reviews\G
SHOW CREATE TABLE amenities\G
SHOW CREATE TABLE place_amenity\G
```
**Expected Results:**
```
mysql> SHOW CREATE TABLE users\G
*************************** 1. row ***************************
       Table: users
Create Table: CREATE TABLE `users` (
  `id` char(36) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
)

mysql> SHOW CREATE TABLE places\G
*************************** 1. row ***************************
       Table: places
Create Table: CREATE TABLE `places` (
  `id` char(36) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` text,
  `price` decimal(10,2) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `owner_id` char(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `places_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
)

mysql> SHOW CREATE TABLE reviews\G
*************************** 1. row ***************************
       Table: reviews
Create Table: CREATE TABLE `reviews` (
  `id` char(36) NOT NULL,
  `text` text,
  `rating` int DEFAULT NULL,
  `user_id` char(36) DEFAULT NULL,
  `place_id` char(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`place_id`),
  KEY `place_id` (`place_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`place_id`) REFERENCES `places` (`id`),
  CONSTRAINT `reviews_chk_1` CHECK ((`rating` between 1 and 5))
)

mysql> SHOW CREATE TABLE amenities\G
*************************** 1. row ***************************
       Table: amenities
Create Table: CREATE TABLE `amenities` (
  `id` char(36) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
)

mysql> SHOW CREATE TABLE place_amenity\G
*************************** 1. row ***************************
       Table: place_amenity
Create Table: CREATE TABLE `place_amenity` (
  `place_id` char(36) NOT NULL,
  `amenity_id` char(36) NOT NULL,
  PRIMARY KEY (`place_id`,`amenity_id`),
  KEY `amenity_id` (`amenity_id`),
  CONSTRAINT `place_amenity_ibfk_1` FOREIGN KEY (`place_id`) REFERENCES `places` (`id`),
  CONSTRAINT `place_amenity_ibfk_2` FOREIGN KEY (`amenity_id`) REFERENCES `amenities` (`id`)
)
```
## PART TWO: INITIAL DATA INSERTION
The aim of this test is to verify:  
a) the initial data has been inserted correctly  
b) the admin user's password is stored in hashed format  
c) the admin user's is_admin column is set to TRUE

### Step 1: Enter MySQL
```bash
mysql -u root
```
### Step 2: Execute initial_data.sql
```sql
SOURCE /path/to/initial_data.sql;
```
### Step 3: Verify the admin user's details
```sql
USE hbnb_db;
SELECT *
FROM users
WHERE first_name = 'Admin';
```
**Expected Result:**
```
+--------------------------------------+------------+-----------+---------------+--------------------------------------------------------------+----------+
| id                                   | first_name | last_name | email         | password                                                     | is_admin |
+--------------------------------------+------------+-----------+---------------+--------------------------------------------------------------+----------+
| 36c9050e-ddd3-4c3b-9731-9f487208bbc1 | Admin      | HBnB      | admin@hbnb.io | $2a$12$J34myE4s28hOlXG8NwUfF.5V9tj/js.QasGVDgBqJjs2RdT1zm0mm |        1 |
+--------------------------------------+------------+-----------+---------------+--------------------------------------------------------------+----------+
```
### Step 4: Verify the amenities have been inserted correctly
```sql
SELECT *
FROM amenities;
```
**Expected Result:**
```
+--------------------------------------+------------------+
| id                                   | name             |
+--------------------------------------+------------------+
| fe30f80c-34f8-4a11-a3d8-c7aaf374e649 | Air Conditioning |
| d5908763-ca8f-4988-816e-26756f11d86c | Swimming Pool    |
| e26d5d10-c86d-4e9a-98f6-5cef8508f1e2 | WiFi             |
+--------------------------------------+------------------+
```
## PART THREE: CRUD OPERATIONS
The aim of these tests is to verify CRUD (Create, Read, Update, Delete) functionality for each table.  
### Step 1: Enter MySQL
```bash
mysql -u root
```
### Step 2: Use database
```sql
USE hbnb_db;
```
### Step 3: Start Transaction
Note: Starting transaction will group all of the subsequent CRUD testing operations together to behave as one single action for temporary testing purposes. 
```sql
START TRANSACTION;
```
### Step 4: End transaction 
Note: Use ROLLBACK **after** CRUD testing is complete to cancel everything since START TRANSACTION.
```sql
ROLLBACK;
```
****
### USERS TABLE
#### CREATE (happy path)
Add a valid user
```sql
SET @id = UUID();

INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (@id, 'Jane', 'Doe', 'janedoe@example.io', '$2a$12$kRjBrjCFAl7xr.jZHzsH9Ot6VDuVKv4cBUBUsDNuFjRSRDur7NQXS', 0);

SELECT *
FROM users
WHERE email = 'janedoe@example.io';
```
**Expected Results:**
```
+--------------------------------------+------------+-----------+--------------------+--------------------------------------------------------------+----------+
| id                                   | first_name | last_name | email              | password                                                     | is_admin |
+--------------------------------------+------------+-----------+--------------------+--------------------------------------------------------------+----------+
| 7574874d-badc-11f0-b9af-a6591eb97a79 | Jane       | Doe       | janedoe@example.io | $2a$12$kRjBrjCFAl7xr.jZHzsH9Ot6VDuVKv4cBUBUsDNuFjRSRDur7NQXS |        0 |
+--------------------------------------+------------+-----------+--------------------+--------------------------------------------------------------+----------+
```
#### CREATE (negative path)
Attempt to create a user with a duplicate email to test UNIQUE constraint
```sql
SET @id = UUID();

INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (@id, 'Janey', 'Dough', 'janedoe@example.io', '$2a$12$kRjBrjCFAl7xr.jZHzsH9Ot6VDuVKv4cBUBUsDNuFjRSRDur7NQXS', 0);
```
**Expected Results:**
```
ERROR 1062 (23000): Duplicate entry 'janedoe@example.io' for key 'users.email'
```

#### CREATE (negative path)
Attempt to create a user with too long last_name (strict mode ON)
```sql
SET SESSION sql_mode = 'STRICT_TRANS_TABLES';
SET @id = UUID();

INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (@id, 'Janey', REPEAT('Doey', 290), 'janeydoey@example.io', '$2a$12$kRjBrjCFAl7xr.jZHzsH9Ot6VDuVKv4cBUBUsDNuFjRSRDur7NQXS', 0);
```
**Expected Result**
```
ERROR 1406 (22001): Data too long for column 'last_name' at row 1
```
#### READ (happy path)
View whole table
```sql
SELECT *
FROM users;
```
**Expected result**
```
+--------------------------------------+------------+-----------+--------------------+--------------------------------------------------------------+----------+
| id                                   | first_name | last_name | email              | password                                                     | is_admin |
+--------------------------------------+------------+-----------+--------------------+--------------------------------------------------------------+----------+
| 36c9050e-ddd3-4c3b-9731-9f487208bbc1 | Admin      | HBnB      | admin@hbnb.io      | $2a$12$J34myE4s28hOlXG8NwUfF.5V9tj/js.QasGVDgBqJjs2RdT1zm0mm |        1 |
| 7574874d-badc-11f0-b9af-a6591eb97a79 | Jane       | Doe       | janedoe@example.io | $2a$12$kRjBrjCFAl7xr.jZHzsH9Ot6VDuVKv4cBUBUsDNuFjRSRDur7NQXS |        0 |
+--------------------------------------+------------+-----------+--------------------+--------------------------------------------------------------+----------+
```

#### READ (happy path)
View one record
```sql
SELECT *
FROM users
WHERE email = 'janedoe@example.io';
```
**Expected result**
```
+--------------------------------------+------------+-----------+--------------------+--------------------------------------------------------------+----------+
| id                                   | first_name | last_name | email              | password                                                     | is_admin |
+--------------------------------------+------------+-----------+--------------------+--------------------------------------------------------------+----------+
| 7574874d-badc-11f0-b9af-a6591eb97a79 | Jane       | Doe       | janedoe@example.io | $2a$12$kRjBrjCFAl7xr.jZHzsH9Ot6VDuVKv4cBUBUsDNuFjRSRDur7NQXS |        0 |
+--------------------------------------+------------+-----------+--------------------+--------------------------------------------------------------+----------+
```

#### READ (negative path)
Attempt to view a record that doesn't exist
```sql
SELECT *
FROM users
WHERE email = 'johndoe@example.io';
```
**Expected result**
```
Empty set
```

#### UPDATE (happy path)
Update a user's info and validate the info has been updated in the database
```sql
UPDATE users
SET first_name = 'Janet', last_name = 'Jackson', email = 'janetjackson@example.io', is_admin = 1
WHERE id = '7574874d-badc-11f0-b9af-a6591eb97a79';
```
**Expected result**
```
Rows matched: 1  Changed: 1  Warnings: 0
```

#### UPDATE (negative path)
Attempt to update a user that doesn't exist
```sql
UPDATE users
SET first_name = 'Janet', last_name = 'Jackson', email = 'janetjackson@example.io', is_admin = 1
WHERE id = '79';
```
**Expected result**
```
Rows matched: 0  Changed: 0  Warnings: 0
```

#### UPDATE (negative path)
Attempt to update a user with wrong data type
```sql
UPDATE users
SET is_admin = 'thisisnotanumber'
WHERE id = '7574874d-badc-11f0-b9af-a6591eb97a79';
```
**Expected result**
```
ERROR 1366 (HY000): Incorrect integer value: 'thisisnotanumber' for column 'is_admin' at row 1
```


#### DELETE (happy path)
Delete a valid user
```sql
DELETE FROM users
WHERE ID = '7574874d-badc-11f0-b9af-a6591eb97a79';
SELECT * FROM users;
```
**Expected Result**
```
Query OK, 1 row affected

+--------------------------------------+------------+-----------+---------------+--------------------------------------------------------------+----------+
| id                                   | first_name | last_name | email         | password                                                     | is_admin |
+--------------------------------------+------------+-----------+---------------+--------------------------------------------------------------+----------+
| 36c9050e-ddd3-4c3b-9731-9f487208bbc1 | Admin      | HBnB      | admin@hbnb.io | $2a$12$J34myE4s28hOlXG8NwUfF.5V9tj/js.QasGVDgBqJjs2RdT1zm0mm |        1 |
+--------------------------------------+------------+-----------+---------------+--------------------------------------------------------------+----------+
```
### DELETE (negative path)
Attempt to delete a user with incorrect ID
```sql
DELETE FROM users
WHERE ID = '78';
```
**Expected Result**
```
Query OK, 0 rows affected
```
****
### PLACES TABLE
#### CREATE (happy path)
Create valid place
```sql
SET @id = UUID();
SET @owner = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (@id, 'Bag End', 'A cozy place to stay', 180.00, -44.56, 133.55, @owner);

SELECT *
FROM places;
```
**Expected result**
```
Query OK, 1 row affected

+--------------------------------------+---------+----------------------+--------+----------+-----------+--------------------------------------+
| id                                   | title   | description          | price  | latitude | longitude | owner_id                             |
+--------------------------------------+---------+----------------------+--------+----------+-----------+--------------------------------------+
| 87b5421e-bae5-11f0-b9af-a6591eb97a79 | Bag End | A cozy place to stay | 180.00 |   -44.56 |    133.55 | 36c9050e-ddd3-4c3b-9731-9f487208bbc1 |
+--------------------------------------+---------+----------------------+--------+----------+-----------+--------------------------------------+
```
#### CREATE (negative path)
Attempt to create place with invalid owner_id (foreign key)
```sql
SET @id = UUID();
INSERT INTO places (id, title, price, owner_id)
VALUES (@id, 'Negative place', 50.00, '111');
```
**Expected result**
```
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails
```
#### READ (happy path)
```sql
SELECT *
FROM places;
```
**Expected result**
```
+--------------------------------------+---------+----------------------+--------+----------+-----------+--------------------------------------+
| id                                   | title   | description          | price  | latitude | longitude | owner_id                             |
+--------------------------------------+---------+----------------------+--------+----------+-----------+--------------------------------------+
| 87b5421e-bae5-11f0-b9af-a6591eb97a79 | Bag End | A cozy place to stay | 180.00 |   -44.56 |    133.55 | 36c9050e-ddd3-4c3b-9731-9f487208bbc1 |
+--------------------------------------+---------+----------------------+--------+----------+-----------+--------------------------------------+
```
#### READ (negative path)
Attempt to read a place that doesn't exist
```sql
SELECT *
FROM places
WHERE id = '111';
```
**Expected result**
```
Empty set
```
#### UPDATE (happy path)
Update a valid place record
```sql
UPDATE places
SET price = 200.00
WHERE id = '87b5421e-bae5-11f0-b9af-a6591eb97a79';
```
**Expected result**
```
Rows matched: 1  Changed: 1  Warnings: 0
```
#### UPDATE (negative path)
Attempt to update the owner_id (foreign key) on a valid place record
```sql
UPDATE places
SET owner_id = '111'
WHERE id = '87b5421e-bae5-11f0-b9af-a6591eb97a79';
```
**Expected result**
```
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails
```
#### DELETE (happy path)
Delete a valid place
```sql
DELETE FROM places
WHERE id = '87b5421e-bae5-11f0-b9af-a6591eb97a79';
```
**Expected result**
```
Query OK, 1 row affected
```
#### DELETE (negative path)
Attempt to delete a place that does not exist
```sql
DELETE FROM places
WHERE id = '123';
```
**Expected result**
```
Query OK, 0 rows affected
```
****
### REVIEWS TABLE
#### CREATE (happy path)
Create a valid review
```sql
SET @admin = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
SET @place = UUID();

INSERT INTO places (id, title, price, owner_id)
VALUES (@place, 'Place to review', 50.00, @admin);

SET @review = UUID();
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (@review, 'Cool place', 5, @admin, @place);

SELECT * FROM reviews;
```
**Expected result**
```
+--------------------------------------+------------+--------+--------------------------------------+--------------------------------------+
| id                                   | text       | rating | user_id                              | place_id                             |
+--------------------------------------+------------+--------+--------------------------------------+--------------------------------------+
| 10136bf0-bae8-11f0-b9af-a6591eb97a79 | Cool place |      5 | 36c9050e-ddd3-4c3b-9731-9f487208bbc1 | 095eaeca-bae8-11f0-b9af-a6591eb97a79 |
+--------------------------------------+------------+--------+--------------------------------------+--------------------------------------+
```

#### CREATE (negative path)
Create review with rating outside of acceptable 1-5 range
```sql
SET @admin = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
SET @place = '10136bf0-bae8-11f0-b9af-a6591eb97a79';
SET @id = UUID();

INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (@id, 'Invalid rating', 100, @admin, @place);
```
**Expected result**
```
ERROR 3819 (HY000): Check constraint 'reviews_chk_1' is violated.
```

#### READ (happy path)
View a valid review
```sql
SELECT *
FROM reviews
WHERE id = '10136bf0-bae8-11f0-b9af-a6591eb97a79';
```
**Expected result**
```
+--------------------------------------+------------+--------+--------------------------------------+--------------------------------------+
| id                                   | text       | rating | user_id                              | place_id                             |
+--------------------------------------+------------+--------+--------------------------------------+--------------------------------------+
| 10136bf0-bae8-11f0-b9af-a6591eb97a79 | Cool place |      5 | 36c9050e-ddd3-4c3b-9731-9f487208bbc1 | 095eaeca-bae8-11f0-b9af-a6591eb97a79 |
+--------------------------------------+------------+--------+--------------------------------------+--------------------------------------+
```
#### READ (negative path)
Attempt to read a non-existent review
```sql
SELECT *
FROM reviews
WHERE id = '101';
```
**Expected result**
```
Empty set
```
#### UPDATE (happy path)
update a valid review
```sql
UPDATE reviews
SET rating = 2, text = 'Poor stay'
WHERE id = '10136bf0-bae8-11f0-b9af-a6591eb97a79';
```
**Expected result**
```
Rows matched: 1  Changed: 1  Warnings: 0
```
#### UPDATE (negative path)
attempt to have a user leave a second review on the same place
```sql
SET @admin = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
SET @place_id = '095eaeca-bae8-11f0-b9af-a6591eb97a79';
SET @id = UUID();

INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (@id, 'Amazing!', 5, @admin, @place_id);
```
**Expected result**
```
ERROR 1062 (23000): Duplicate entry '36c9050e-ddd3-4c3b-9731-9f487208bbc1-095eaeca-bae8-11f0-b9af-a65' for key 'reviews.user_id'
```
#### DELETE (happy path)
Delete a review
```sql
DELETE FROM reviews
WHERE id = '10136bf0-bae8-11f0-b9af-a6591eb97a79';
```
**Expected result**
```
Query OK, 1 row affected
```
#### DELETE (negative path)
Attempt to delete a review that doesn't exist
```sql
DELETE FROM reviews
WHERE id = '1';
```
**Expected result**
```
Query OK, 0 rows affected
```
****
### AMENITIES TABLE
#### CREATE (happy path)
create a valid amenity
```sql
SET @amenity = UUID();

INSERT INTO amenities (id, name)
VALUES (@amenity, 'Hot tub');

SELECT *
FROM amenities;
```
**Expected Result**
```
Query OK, 1 row affected

+--------------------------------------+------------------+
| id                                   | name             |
+--------------------------------------+------------------+
| fe30f80c-34f8-4a11-a3d8-c7aaf374e649 | Air Conditioning |
| dc1d578b-baea-11f0-b9af-a6591eb97a79 | Hot tub          |
| d5908763-ca8f-4988-816e-26756f11d86c | Swimming Pool    |
| e26d5d10-c86d-4e9a-98f6-5cef8508f1e2 | WiFi             |
+--------------------------------------+------------------+
```
#### CREATE (negative path)
Attempt to create an amenity with a duplicate name
```sql
SET @amenity = UUID();

INSERT INTO amenities (id, name)
VALUES (@amenity, 'Hot tub');
```
**Expected Result**
```
ERROR 1062 (23000): Duplicate entry 'Hot tub' for key 'amenities.name'
```

#### READ (happy path)
View a record by name
```sql
SELECT *
FROM amenities
WHERE name = 'Hot tub';
```
**Expected Result**
```
+--------------------------------------+---------+
| id                                   | name    |
+--------------------------------------+---------+
| dc1d578b-baea-11f0-b9af-a6591eb97a79 | Hot tub |
+--------------------------------------+---------+
```
#### READ (negative path)
Attempt to view a record that doesn't exist
```sql
SELECT *
FROM amenities
WHERE name = 'Hot tub time machine';
```
**Expected Result**
```
Empty set
```
#### UPDATE (happy path)
Update a valid amenity record
```sql
UPDATE amenities
SET name = 'Spa'
WHERE name = 'Hot tub';

SELECT *
FROM amenities;
```
**Expected Result**
```
Rows matched: 1  Changed: 1  Warnings: 0

+--------------------------------------+------------------+
| id                                   | name             |
+--------------------------------------+------------------+
| fe30f80c-34f8-4a11-a3d8-c7aaf374e649 | Air Conditioning |
| dc1d578b-baea-11f0-b9af-a6591eb97a79 | Spa              |
| d5908763-ca8f-4988-816e-26756f11d86c | Swimming Pool    |
| e26d5d10-c86d-4e9a-98f6-5cef8508f1e2 | WiFi             |
+--------------------------------------+------------------+
```
#### UPDATE (negative path)
Attempt to update an amenities name, to a name that already exists in the table
```sql
UPDATE amenities
SET name = 'WiFi'
WHERE name = 'Spa';
```
**Expected Result**
```
ERROR 1062 (23000): Duplicate entry 'WiFi' for key 'amenities.name'
```
#### DELETE (happy path)
Delete a valid record
```sql
DELETE FROM amenities
WHERE name = 'Spa';

SELECT *
FROM amenities
WHERE name = 'Spa';
```
**Expected Result**
```
Query OK, 1 row affected
...
Empty set
```
#### DELETE (negative path)
Attempt to delete an amenity that doesn't exist
```sql
DELETE FROM amenities
WHERE name = 'Time Machine';
```
**Expected Result**
```
Query OK, 0 rows affected
```
****
### PLACE_AMENITY TABLE
#### CREATE (happy path)

```sql
SET @place_id = '095eaeca-bae8-11f0-b9af-a6591eb97a79';
SET @amenity_id = 'fe30f80c-34f8-4a11-a3d8-c7aaf374e649';

INSERT INTO place_amenity (place_id, amenity_id)
VALUES (@place_id, @amenity_id);

SELECT *
FROM place_amenity;

```
**Expected Result:**
```
Query OK, 1 row affected

+--------------------------------------+--------------------------------------+
| place_id                             | amenity_id                           |
+--------------------------------------+--------------------------------------+
| 095eaeca-bae8-11f0-b9af-a6591eb97a79 | fe30f80c-34f8-4a11-a3d8-c7aaf374e649 |
+--------------------------------------+--------------------------------------+
```
#### CREATE (negative path)
Attempt to create a duplicate entry to test composite primary key unique constraint
```sql
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (@place_id, @amenity_id);
```
**Expected Result:**
```
ERROR 1062 (23000): Duplicate entry '095eaeca-bae8-11f0-b9af-a6591eb97a79-fe30f80c-34f8-4a11-a3d8-c7a' for key 'place_amenity.PRIMARY'
```
#### READ (happy path)
Read an individual record in table
```sql
SELECT *
FROM place_amenity
WHERE place_id = '095eaeca-bae8-11f0-b9af-a6591eb97a79';
```
**Expected Result:**
```
+--------------------------------------+--------------------------------------+
| place_id                             | amenity_id                           |
+--------------------------------------+--------------------------------------+
| 095eaeca-bae8-11f0-b9af-a6591eb97a79 | fe30f80c-34f8-4a11-a3d8-c7aaf374e649 |
+--------------------------------------+--------------------------------------+
```
#### READ (negative path)
Attempt to view a record that doesn't exist
```sql
SELECT *
FROM place_amenity
WHERE place_id = '09';
```
**Expected Result:**
```
Empty set
```
#### UPDATE (happy path)
Update the amenity id of the record to an amenity that exists
```sql
UPDATE place_amenity
SET amenity_id = 'd5908763-ca8f-4988-816e-26756f11d86c'
WHERE place_id = '095eaeca-bae8-11f0-b9af-a6591eb97a79';
```
**Expected Result:**
```
Rows matched: 1  Changed: 1  Warnings: 0
```
#### UPDATE (negative path)
Attempt to update the amenity id of the record to an amenity that does not exist
```sql
UPDATE place_amenity
SET amenity_id = '123'
WHERE place_id = '095eaeca-bae8-11f0-b9af-a6591eb97a79';
```
**Expected Result:**
```
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails (`hbnb_db`.`place_amenity`, CONSTRAINT `place_amenity_ibfk_2` FOREIGN KEY (`amenity_id`) REFERENCES `amenities` (`id`))
```
#### DELETE (happy path)
Delete a record from table
```sql
SET @place_id = '095eaeca-bae8-11f0-b9af-a6591eb97a79';

DELETE FROM place_amenity
WHERE place_id = @place_id;
```
**Expected Result:**
```
Query OK, 1 row affected
```
#### DELETE (negative path)
Attempt to delete a non-existent record
```sql
DELETE FROM place_amenity
WHERE place_id = '567';
```
**Expected Result:**
```
Query OK, 0 rows affected
```
