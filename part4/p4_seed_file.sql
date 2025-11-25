-- Creates Administration User
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at) VALUES (
    '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', -- UUID v4 generated using online tool
    'Super',
    'Admin',
    'admin@example.com',
    '$2a$12$0SHxEVM9elZCfsKX6y5YY.RBMXRO7dTM8oshubA4sQADExUoYky/a', -- hashed p/w
    TRUE,
    datetime('now', 'localtime'), -- mimics Python's local timestamping
    datetime('now', 'localtime')
);

-- Createsplaceholder places that belong to the admin user
INSERT into places (id, title, description, price, latitude, longitude, user_id, created_at, updated_at) VALUES (
    '73248542-bb18-4b36-a04e-a8cf43999249',
    'Title: Placeholder Place 1',
    'Description: Place 1 description',
    10,
    37.7749,
    -122.4194,
    '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', -- admin user's user_id
    datetime('now', 'localtime'),
    datetime('now', 'localtime')
),
(
    'c7ac3268-ee45-40e2-a1cf-538538448330',
    'Title: Placeholder Place 2',
    'Description: Place 2 description',
    50,
    10.7545,
    -155.5484,
    '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', -- admin user's user_id
    datetime('now', 'localtime'),
    datetime('now', 'localtime')
),
(
    '53842c68-75ff-4fdf-b8e1-efc22b761b3d',
    'Title: Placeholder Place 3',
    'Description: Place 3 description',
    80,
    50.5442,
    -115.5462,
    '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', -- admin user's user_id
    datetime('now', 'localtime'),
    datetime('now', 'localtime')
),
(
    '023e6b24-3eac-4413-805d-07bb6dd350f0',
    'Title: Placeholder Place 4',
    'Description: Place 4 description',
    150,
    30.4445,
    -112.7785,
    '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', -- admin user's user_id
    datetime('now', 'localtime'),
    datetime('now', 'localtime')
);
