CREATE TABLE users (
    name TEXT UNIQUE,
    password TEXT,
    balance INTEGER,
    PRIMARY KEY(name)
);

INSERT INTO users (name, password, balance)
VALUES ('Ichi', 'B0N1T0', 10000);

INSERT INTO users (name, password, balance)
VALUES ('Jenni', 'secreto', 2000);

UPDATE users
SET balance = 10000
WHERE name = 'Ichi';