-- Creates Administration User
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at) VALUES (
    '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', -- UUID v4 generated using online tool
    'Super',
    'Admin',
    'admin@example.com',
    '$2a$12$8mqK0BGhkRzmWgXz2n8vKevouTPHQvS.Tfr/3Qz32bUw78D4wz/Mq', -- hashed p/w
    TRUE
);