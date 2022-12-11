CREATE USER IF NOT EXISTS 'moacir'@'localhost' IDENTIFIED BY 'kmvd96ui';

CREATE DATABASE IF NOT EXISTS db_mcadv;

GRANT ALL PRIVILEGES ON db_mcadv.* TO '%' IDENTIFIED BY 'kmvd96ui';
GRANT ALL PRIVILEGES ON db_mcadv.* TO moacir@localhost IDENTIFIED BY 'kmvd96ui';

FLUSH PRIVILEGES;

CREATE TABLE users (
    id INTEGER NOT NULL AUTO_INCREMENT,
    email VARCHAR(200),
    hashed_password VARCHAR(100),
    is_active BOOL,
    PRIMARY KEY (id)
);