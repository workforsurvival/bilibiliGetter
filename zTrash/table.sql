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
  DROP TABLE IF EXISTS `contents`;
CREATE TABLE `contents` (
    `contUid` int(11) NOT NULL AUTO_INCREMENT,
    `cid` varchar(150) DEFAULT NULL,
    `title` longtext DEFAULT NULL,
    `creator` varchar(150) DEFAULT NULL,
    `tmCount` varchar(50) DEFAULT NULL,
    `info` longtext DEFAULT NULL,
    `addCount` varchar(50) DEFAULT NULL,
    `tags` longtext DEFAULT NULL,
    `cDate` datetime DEFAULT current_timestamp(),
    PRIMARY KEY (`contUid`)
  ) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8mb4;

insert into contents set cid = 'BV1wi4y1T7jZ',creator='sfds',title='fkfkfk',tags='gsgdsfds',info='fdsfdsfds',addCount='100000';

  DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments`(
    `uid` int(11) NOT NULL AUTO_INCREMENT,
    `cid` varchar(150) DEFAULT NULL,
    `comment` longtext DEFAULT NULL,
    `type` tinyint(2) DEFAULT 0,
    `cDate` DATETIME DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (`uid`)
  ) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8mb4;

insert into comments set cid='BV1wi4y1T7jZ',comment='올라',type=1;

DROP TABLE IF EXISTS `words`;
CREATE TABLE `words`(
    `uid` int(11) NOT NULL AUTO_INCREMENT,
    `cid` varchar(150) DEFAULT NULL,
    `words` varchar(150) DEFAULT NULL,
    `count` BIGINT (11) DEFAULT 1,
    `comment` longtext DEFAULT NULL,
    `cDate` DATETIME DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (`uid`)
  ) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8mb4;
alter table words add index words(words);
alter table words add index cid(cid);
insert into words set cid='BV1wi4y1T7jZ',words='sum';
update words set count=count+1 where cid='BV1wi4y1T7jZ';


