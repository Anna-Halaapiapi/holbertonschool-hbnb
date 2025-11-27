-- Creates Administration User
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at) VALUES (
    '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', -- UUID v4 generated using online tool
    'AMATRIX',
    'Superuser',
    'admin@example.com',
    '$2a$12$0SHxEVM9elZCfsKX6y5YY.RBMXRO7dTM8oshubA4sQADExUoYky/a', -- hashed p/w
    TRUE,
    datetime('now', 'localtime'), -- mimics Python's local timestamping
    datetime('now', 'localtime')
);

-- Createsplaceholder places that belong to the admin user
INSERT into places (id, title, description, price, latitude, longitude, user_id, created_at, updated_at) VALUES (
    '73248542-bb18-4b36-a04e-a8cf43999249',
    'Neon Lounge Loft',
    'A stylish industrial loft, illuminated by dynamic neon under-lighting and ambient wall projections.',
    10,
    37.7749,
    -122.4194,
    '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', -- admin user's user_id
    datetime('now', 'localtime'),
    datetime('now', 'localtime')
),
(
    'c7ac3268-ee45-40e2-a1cf-538538448330',
    'Skyline Sleeper Pod',
    'A luxury capsule suite, overlooking a futuristic megacity skyline.',
    50,
    10.7545,
    -155.5484,
    '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', -- admin user's user_id
    datetime('now', 'localtime'),
    datetime('now', 'localtime')
),
(
    '53842c68-75ff-4fdf-b8e1-efc22b761b3d',
    'Horizon Glass Suite',
    'A panoramic living space, with glass walls facing a neon-soaked harbour.',
    80,
    50.5442,
    -115.5462,
    '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', -- admin user's user_id
    datetime('now', 'localtime'),
    datetime('now', 'localtime')
),
(
    '023e6b24-3eac-4413-805d-07bb6dd350f0',
    'Cyber-Villa',
    'A geometric, neon-lined smart villa with adaptive light architecture.',
    150,
    30.4445,
    -112.7785,
    '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', -- admin user's user_id
    datetime('now', 'localtime'),
    datetime('now', 'localtime')
),
(
    '46bd48fb-4fff-4d30-9867-becf6f5945ba',
    'Synthwave Hideout',
    'Sleek, modern, a perfect hideaway for late-night hacking sessions or covert op teams',
    250,
    35.6895,
    -139.6917,
    '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', -- admin user's user_id
    datetime('now', 'localtime'),
    datetime('now', 'localtime')
),
(
    'fe973153-4dc1-47c8-ad41-3c89a9514f26',
    'The Quantum Lounge Suite',
    'High-end entertainment suite, featuring chromatic lighting, holo-screens and minimalist vibes.',
    140,
    22.3193,
    114.1694,
    '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', -- admin user's user_id
    datetime('now', 'localtime'),
    datetime('now', 'localtime')
);
