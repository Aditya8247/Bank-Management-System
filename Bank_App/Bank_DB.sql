CREATE DATABASE bankdb;

CREATE TABLE accounts (
    acc_no INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    password VARCHAR(50),
    dob DATE,
    balance FLOAT DEFAULT 0
);


ALTER TABLE accounts AUTO_INCREMENT = 101;
select * from accounts;