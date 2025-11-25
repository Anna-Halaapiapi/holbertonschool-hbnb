-- INITIAL DATA INSERT
-- Administrator User, p/w is bcrypt hashed using 12 rounds and online tool
INSERT into `users`
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2a$12$J34myE4s28hOlXG8NwUfF.5V9tj/js.QasGVDgBqJjs2RdT1zm0mm',
    TRUE
    );

-- Initial Amenities
-- UUID v4 online tool used to gen ids
INSERT into `amenities`
VALUES
    ('e26d5d10-c86d-4e9a-98f6-5cef8508f1e2', 'WiFi'),
    ('d5908763-ca8f-4988-816e-26756f11d86c', 'Swimming Pool'),
    ('fe30f80c-34f8-4a11-a3d8-c7aaf374e649', 'Air Conditioning');
