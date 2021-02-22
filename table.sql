-- use `mysql`;
-- CREATE USER 'bidatauser1'@'localhost' IDENTIFIED WITH mysql_native_password BY 'bidatauser1234';
-- GRANT ALL PRIVILEGES ON bidata.* TO 'bidatauser1'@'localhost';
-- FLUSH PRIVILEGES;
-- set foreign_key_checks=0;
DROP TABLE IF EXISTS `bidata`;
CREATE DATABASE IF NOT EXISTS `bidata` character set utf8mb4 collate utf8mb4_general_ci;
use `bidata`;
set
  foreign_key_checks = 0;
-- 콘텐츠정보(영화,드라마,예능등등등)
  DROP TABLE IF EXISTS `Contents`;
CREATE TABLE `Contents` (
    `contUid` int(11) NOT NULL AUTO_INCREMENT,
    `crUid` int(11) DEFAULT 0,
    `cid` varchar(150) DEFAULT NULL,
    `creator` varchar(150) DEFAULT NULL,
    `title` longtext DEFAULT NULL,
    `tags` longtext DEFAULT NULL,
    `thumbnail` longtext DEFAULT NULL,
    `description` longtext DEFAULT NULL,
    `hits` varchar(50) DEFAULT NULL,
    `thumbsUp` int(11) DEFAULT 0,
    `cDate` datetime DEFAULT current_timestamp(),
    FOREIGN KEY (`crUid`) REFERENCES `Creator`(`crUid`),
    PRIMARY KEY (`contUid`)
  ) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8mb4;
--insert into Contents
set
  cid = 'fdsfdsfds',
  crea CREATE TABLE `comments`(
    `uid` int(11) NOT NULL AUTO_INCREMENT,
    `comment` longtext DEFAULT NULL,
    `cDate` DATETIME DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (`uid`)
  ) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8mb4;
CREATE TABLE `words`(
    `uid` int(11) NOT NULL AUTO_INCREMENT,
    `cid` varchar(150) DEFAULT NULL,
    `words` varchar(150) DEFAULT NULL,
    `count` BIGINT (11) DEFAULT NULL,
    `comment` longtext DEFAULT NULL,
    `cDate` DATETIME DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (`uid`)
  ) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8mb4;