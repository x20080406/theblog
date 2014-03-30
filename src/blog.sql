-- MySQL dump 10.13  Distrib 5.5.36, for Linux (x86_64)
--
-- Host: localhost    Database: app2
-- ------------------------------------------------------
-- Server version	5.5.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `group_permission`
--

DROP TABLE IF EXISTS `group_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_permission` (
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`group_id`,`permission_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `group_permission_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `group_permission_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_permission`
--

LOCK TABLES `group_permission` WRITE;
/*!40000 ALTER TABLE `group_permission` DISABLE KEYS */;
INSERT INTO `group_permission` VALUES (1,1),(2,1),(1,2),(2,2),(1,3);
/*!40000 ALTER TABLE `group_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groups` (
  `name` varchar(255) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups`
--

LOCK TABLES `groups` WRITE;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
INSERT INTO `groups` VALUES ('admins',1),('users',2);
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permissions` (
  `name` varchar(255) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions`
--

LOCK TABLES `permissions` WRITE;
/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
INSERT INTO `permissions` VALUES ('delete',3),('read',2),('write',1);
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_articles`
--

DROP TABLE IF EXISTS `t_articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `comment_num` smallint(6) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  `edit_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_articles`
--

LOCK TABLES `t_articles` WRITE;
/*!40000 ALTER TABLE `t_articles` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_articles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_categories`
--

DROP TABLE IF EXISTS `t_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(17) NOT NULL,
  `id_num` smallint(6) NOT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_categories`
--

LOCK TABLES `t_categories` WRITE;
/*!40000 ALTER TABLE `t_categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_category_article_rel`
--

DROP TABLE IF EXISTS `t_category_article_rel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_category_article_rel` (
  `category_id` int(11) NOT NULL,
  `article_id` int(11) NOT NULL,
  PRIMARY KEY (`category_id`,`article_id`),
  KEY `article_id` (`article_id`),
  CONSTRAINT `t_category_article_rel_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `t_categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `t_category_article_rel_ibfk_2` FOREIGN KEY (`article_id`) REFERENCES `t_articles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_category_article_rel`
--

LOCK TABLES `t_category_article_rel` WRITE;
/*!40000 ALTER TABLE `t_category_article_rel` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_category_article_rel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_comments`
--

DROP TABLE IF EXISTS `t_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `url` varchar(75) DEFAULT NULL,
  `visible` tinyint(1) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  `content` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_comments`
--

LOCK TABLES `t_comments` WRITE;
/*!40000 ALTER TABLE `t_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_invitees`
--

DROP TABLE IF EXISTS `t_invitees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_invitees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `tel` bigint(20) DEFAULT NULL,
  `sid` int(11) DEFAULT NULL,
  `invite_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `invite_id` (`invite_id`),
  CONSTRAINT `t_invitees_ibfk_1` FOREIGN KEY (`invite_id`) REFERENCES `t_inviters` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_invitees`
--

LOCK TABLES `t_invitees` WRITE;
/*!40000 ALTER TABLE `t_invitees` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_invitees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_inviters`
--

DROP TABLE IF EXISTS `t_inviters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_inviters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `tel` bigint(20) DEFAULT NULL,
  `sid` int(11) DEFAULT NULL,
  `sendTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_inviters`
--

LOCK TABLES `t_inviters` WRITE;
/*!40000 ALTER TABLE `t_inviters` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_inviters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_tag_article_rel`
--

DROP TABLE IF EXISTS `t_tag_article_rel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_tag_article_rel` (
  `tag_id` int(11) NOT NULL,
  `article_id` int(11) NOT NULL,
  PRIMARY KEY (`tag_id`,`article_id`),
  KEY `article_id` (`article_id`),
  CONSTRAINT `t_tag_article_rel_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `t_tags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `t_tag_article_rel_ibfk_2` FOREIGN KEY (`article_id`) REFERENCES `t_articles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_tag_article_rel`
--

LOCK TABLES `t_tag_article_rel` WRITE;
/*!40000 ALTER TABLE `t_tag_article_rel` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_tag_article_rel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_tags`
--

DROP TABLE IF EXISTS `t_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_tags` (
  `name` varchar(255) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sort` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_tags`
--

LOCK TABLES `t_tags` WRITE;
/*!40000 ALTER TABLE `t_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_visitinfo`
--

DROP TABLE IF EXISTS `t_visitinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_visitinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` smallint(6) DEFAULT NULL,
  `ip` bigint(20) DEFAULT NULL,
  `visit_date` datetime DEFAULT NULL,
  `channel` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_visitinfo`
--

LOCK TABLES `t_visitinfo` WRITE;
/*!40000 ALTER TABLE `t_visitinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_visitinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_group`
--

DROP TABLE IF EXISTS `user_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_group` (
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`group_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `user_group_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_group_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_group`
--

LOCK TABLES `user_group` WRITE;
/*!40000 ALTER TABLE `user_group` DISABLE KEYS */;
INSERT INTO `user_group` VALUES (1,1),(2,2),(3,2);
/*!40000 ALTER TABLE `user_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'tianjie','tianj','PBKDF2$sha256$10000$FQpEM1/x1F1m80IN$XCe58XEAagP7IoZDPkj2w3vYxH7I+aMu',1),(2,'baz','baz姓','PBKDF2$sha256$10000$01fEdvcFBJ9McMZx$qXcy/JXzfpMpOVOLCJ9hCynJKlu9erRz',0),(3,'bar','bar','PBKDF2$sha256$10000$F8IRGnlW3cWpbUMB$BZu3MuQTHCCvy/HKGgCtTzOVgG3qqq3N',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-03-22 20:02:11
