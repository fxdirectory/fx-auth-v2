USE fx_auth;

INSERT INTO users (username, password, role) VALUES
('admin', '1234', 'admin'),
('user1', '1234', 'user')
ON DUPLICATE KEY UPDATE username = username;
