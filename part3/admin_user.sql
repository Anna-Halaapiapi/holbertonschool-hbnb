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