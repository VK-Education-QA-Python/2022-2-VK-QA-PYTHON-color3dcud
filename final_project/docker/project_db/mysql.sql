CREATE database if not exists vkeducation;

CREATE USER if not exists 'test_qa'@'%' IDENTIFIED BY 'qa_test';
GRANT ALL PRIVILEGES ON *.* TO 'test_qa'@'%';
FLUSH PRIVILEGES;

USE vkeducation;
CREATE TABLE `test_users` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `surname` varchar(255) NOT NULL,
    `middle_name` varchar(255) DEFAULT NULL,
    `username` varchar(16) DEFAULT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(64) NOT NULL,
    `access` smallint DEFAULT NULL,
    `active` smallint DEFAULT NULL,
    `start_active_time` datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`),
    UNIQUE KEY `ix_test_users_username` (`username`)
);

INSERT INTO test_users (name, surname, username, password, email, access) VALUES ('Test', 'Test', 'test_user', 'test', 'test@test.qa', 1);
INSERT INTO test_users (name, surname, username, password, email, access) VALUES ('No', 'Username', 'no_username', 'test', 'no_username@test.qa', 1);
INSERT INTO test_users (name, surname, username, password, email, access) VALUES ('Mock', 'Value', 'test_mock', 'test', 'test_mock@test.qa', 1);
INSERT INTO test_users (name, surname, username, password, email, access) VALUES ('No', 'Access', 'no_access', 'test', 'no_access@test.qa', 0);
INSERT INTO test_users (name, surname, username, password, email, access) VALUES ('Delete', 'Delete', 'delete_user', 'test', 'delete_user@test.qa', 1);
