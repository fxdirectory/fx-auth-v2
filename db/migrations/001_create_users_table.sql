CREATE DATABASE IF NOT EXISTS fx_auth
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE fx_auth;

CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(100) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,           
    token       VARCHAR(64)  NULL,               
    role        VARCHAR(50)  NOT NULL DEFAULT 'user',
    last_login  DATETIME     NULL,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
