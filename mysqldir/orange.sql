-- MySQL dump 10.13  Distrib 5.6.21-70.0, for Linux (x86_64)
--
-- Host: localhost    Database: orange
-- ------------------------------------------------------
-- Server version	5.6.21-70.0-log

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
-- Table structure for table `t_acc_group`
--

DROP TABLE IF EXISTS `t_acc_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_acc_group` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL,
  `nums` int(10) NOT NULL,
  `remarks` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_acc_group`
--

LOCK TABLES `t_acc_group` WRITE;
/*!40000 ALTER TABLE `t_acc_group` DISABLE KEYS */;
INSERT INTO `t_acc_group` VALUES (1,'admin',1,'管理员组');
/*!40000 ALTER TABLE `t_acc_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_acc_user`
--

DROP TABLE IF EXISTS `t_acc_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_acc_user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `alias` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `group` varchar(24) DEFAULT NULL,
  `password` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `usrole` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mail` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `remarks` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_acc_user`
--

LOCK TABLES `t_acc_user` WRITE;
/*!40000 ALTER TABLE `t_acc_user` DISABLE KEYS */;
INSERT INTO `t_acc_user` VALUES (1,'管理员','admin',NULL,'YWRtaW4=','admin','18301022797@163.com','超级管理员'),(4,'徐志威','xuzhiwei',NULL,'b3Jhbmdl','develop','954157605@qq.com','运维');
/*!40000 ALTER TABLE `t_acc_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_auth_host`
--

DROP TABLE IF EXISTS `t_auth_host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_auth_host` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `user` varchar(255) DEFAULT NULL,
  `user_group` varchar(255) DEFAULT NULL,
  `host_group` varchar(255) DEFAULT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_auth_host`
--

LOCK TABLES `t_auth_host` WRITE;
/*!40000 ALTER TABLE `t_auth_host` DISABLE KEYS */;
INSERT INTO `t_auth_host` VALUES (1,'所有权限','admin','','default,yace,test,docker','管理员权限'),(3,'test','admin,xuzhiwei','','docker,test','测试1');
/*!40000 ALTER TABLE `t_auth_host` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_command_log`
--

DROP TABLE IF EXISTS `t_command_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_command_log` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `com_name` varchar(30) NOT NULL,
  `com_type` varchar(30) NOT NULL,
  `com_info` varchar(255) NOT NULL,
  `com_host` varchar(255) NOT NULL,
  `com_status` varchar(10) NOT NULL,
  `com_reason` varchar(255) DEFAULT NULL,
  `com_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_command_log`
--

LOCK TABLES `t_command_log` WRITE;
/*!40000 ALTER TABLE `t_command_log` DISABLE KEYS */;
INSERT INTO `t_command_log` VALUES (1,'xuzhiwei','批量命令','hostname','14,28','成功',NULL,'2021-05-24 16:24:12'),(2,'xuzhiwei','批量命令','dasf','14,28','成功',NULL,'2021-05-24 16:26:47'),(3,'xuzhiwei','批量命令','dasf','14,28','成功',NULL,'2021-05-24 16:26:47'),(4,'xuzhiwei','批量命令','ls /data','14','成功',NULL,'2021-05-24 16:27:32'),(5,'xuzhiwei','批量脚本','1.sh','28,14','成功',NULL,'2021-05-24 16:34:37'),(6,'xuzhiwei','批量命令','whoami','14,28','成功',NULL,'2021-05-25 11:01:45'),(7,'xuzhiwei','批量命令','hostname','14,28','成功',NULL,'2021-05-27 14:42:51'),(8,'admin','批量命令','whoami','14,28,17,22,23,27,1,2,4','成功',NULL,'2021-06-02 17:28:18'),(9,'xuzhiwei','批量命令','hostname','14,28','成功',NULL,'2021-06-13 17:36:13'),(10,'xuzhiwei','批量命令','date','14,28','成功',NULL,'2021-06-13 17:36:27'),(11,'admin','批量命令','lsblk','1,2,4','成功',NULL,'2021-07-06 09:57:20'),(12,'admin','批量命令','lsblk','1,2,4','成功',NULL,'2021-07-06 10:20:20'),(13,'admin','批量命令','lsblk','14,17,22,23,27','失败','连接主机失败','2021-07-06 10:20:33'),(14,'admin','批量命令','lsblk','14,17,22,23,27','失败','连接主机失败','2021-07-06 10:20:50'),(15,'admin','批量命令','lsblk','14','成功',NULL,'2021-07-06 10:20:58'),(16,'admin','批量命令','lsblk','17,22,23,27','失败','连接主机失败','2021-07-06 10:34:44'),(17,'admin','批量命令','lsblk','17,22,23,27','失败','连接主机失败','2021-07-06 10:34:58'),(18,'admin','批量命令','lsblk','17,22,23,27','成功',NULL,'2021-07-06 10:42:52'),(19,'admin','批量命令','lsblk','17,22,23,27','成功',NULL,'2021-07-06 10:43:30'),(20,'admin','批量命令','lsblk','17,22,23,27','失败','连接主机失败','2021-07-06 10:45:23'),(21,'admin','批量命令','lsblk','17,22,23,27','失败','连接主机失败','2021-07-06 10:49:45'),(22,'admin','批量命令','lsblk','17,22,23,27','失败','连接主机失败','2021-07-06 10:50:23'),(23,'admin','批量命令','lsblk','17,22,23,27','失败','连接主机失败','2021-07-06 10:50:49'),(24,'admin','批量命令','lsblk','17,22,23,27','失败','连接主机失败','2021-07-06 10:51:59'),(25,'admin','批量命令','lsblk','17,22,23,27','失败','连接主机失败','2021-07-06 10:54:27'),(26,'admin','批量命令','hostname','17,22,23,27','失败','连接主机失败','2021-07-06 10:55:13'),(27,'admin','批量命令','hostname','17,22,23,27','失败','连接主机失败','2021-07-06 10:55:54'),(28,'admin','批量命令','hostname','17,22,23,27','失败','连接主机失败','2021-07-06 10:56:55'),(29,'admin','批量命令','hostname','17,22,23,27','失败','连接主机失败','2021-07-06 11:00:31'),(30,'admin','批量命令','hostname','17,22,23,27','失败','连接主机失败','2021-07-06 11:00:52'),(31,'admin','批量命令','hostname','17,22,23,27','失败','连接主机失败','2021-07-06 11:01:16'),(32,'admin','批量命令','hostname','17,22,23,27','失败','连接主机失败','2021-07-06 11:03:14'),(33,'admin','批量命令','hostname','28','成功',NULL,'2021-07-06 11:04:50'),(34,'admin','批量脚本','1.sh','17,22,23,27','失败','连接主机失败','2021-07-06 13:59:30'),(35,'admin','批量脚本','1.sh','17,22,23,27','失败','连接主机失败','2021-07-06 13:59:42'),(36,'admin','批量脚本','1.sh','17,22,23,27','失败','连接主机失败','2021-07-06 14:01:29'),(37,'admin','批量脚本','1.sh','27','成功',NULL,'2021-07-06 14:01:55'),(38,'admin','批量脚本','1.sh','28,1,2,4','成功',NULL,'2021-07-06 15:54:14');
/*!40000 ALTER TABLE `t_command_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_cz_log`
--

DROP TABLE IF EXISTS `t_cz_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_cz_log` (
  `id` int(10) NOT NULL,
  `cz_name` varchar(30) NOT NULL,
  `cz_type` varchar(30) NOT NULL,
  `cz_info` varchar(255) NOT NULL,
  `cz_details` varchar(255) NOT NULL,
  `cz_status` varchar(10) NOT NULL,
  `cz_reason` varchar(255) DEFAULT NULL,
  `cz_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_cz_log`
--

LOCK TABLES `t_cz_log` WRITE;
/*!40000 ALTER TABLE `t_cz_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_cz_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_group`
--

DROP TABLE IF EXISTS `t_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_group` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL,
  `nums` int(5) NOT NULL,
  `remarks` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_group`
--

LOCK TABLES `t_group` WRITE;
/*!40000 ALTER TABLE `t_group` DISABLE KEYS */;
INSERT INTO `t_group` VALUES (1,'default',3,'默认组'),(2,'docker',1,''),(3,'yace',4,NULL),(7,'test',1,'测试');
/*!40000 ALTER TABLE `t_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_host`
--

DROP TABLE IF EXISTS `t_host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_host` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `alias` varchar(25) NOT NULL,
  `host_ip` varchar(16) NOT NULL,
  `host_port` int(5) NOT NULL,
  `host_user` varchar(20) NOT NULL,
  `host_password` varchar(20) NOT NULL,
  `group` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_host`
--

LOCK TABLES `t_host` WRITE;
/*!40000 ALTER TABLE `t_host` DISABLE KEYS */;
INSERT INTO `t_host` VALUES (1,'yw199','10.0.1.199',22,'root','amxiMTIz','default'),(2,'yw200','10.0.1.200',22,'root','amxiMTIz','default'),(4,'test-python-238','10.0.1.238',22,'root','amxidGVzdEAyMzgj','default'),(14,'test-yw-197','10.0.1.197',22,'root','amxiMTIz','docker'),(17,'test-db-185','10.0.1.185',22,'root','amxidGVzdEAxODUj','yace'),(22,'test-web-182','10.0.1.182',22,'root','amxidGVzdEAxODIj','yace'),(23,'test-server-184','10.0.1.184',22,'root','amxidGVzdEAxODQj','yace'),(27,'test-client-181','10.0.1.181',22,'root','amxidGVzdEAxODEj','yace'),(28,'测试环境web245','10.0.1.245',22,'root','amxidGVzdEAyNDUj','test');
/*!40000 ALTER TABLE `t_host` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_line_chart`
--

DROP TABLE IF EXISTS `t_line_chart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_line_chart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chart_date` date DEFAULT NULL,
  `login_count` int(255) DEFAULT NULL,
  `user_count` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_line_chart`
--

LOCK TABLES `t_line_chart` WRITE;
/*!40000 ALTER TABLE `t_line_chart` DISABLE KEYS */;
INSERT INTO `t_line_chart` VALUES (1,'2021-05-11',3,2),(2,'2021-05-12',3,2),(3,'2021-05-13',2,1),(4,'2021-05-14',2,2),(5,'2021-05-15',0,0),(6,'2021-05-16',0,0),(7,'2021-05-17',2,1),(8,'2021-05-18',5,2),(9,'2021-05-19',4,2),(10,'2021-05-20',0,0),(11,'2021-05-21',2,1),(12,'2021-05-22',0,0),(13,'2021-05-23',0,0),(14,'2021-05-24',4,2),(15,'2021-05-25',2,1),(16,'2021-05-26',12,2),(17,'2021-05-27',1,1),(18,'2021-05-28',0,0),(19,'2021-05-29',0,0),(20,'2021-05-30',0,0),(21,'2021-05-31',11,3),(22,'2021-06-01',4,2),(23,'2021-06-02',2,1),(30,'2021-06-03',1,1),(31,'2021-06-04',1,1),(32,'2021-06-07',3,1),(33,'2021-06-08',9,2),(34,'2021-06-09',1,1),(35,'2021-06-10',2,2),(36,'2021-06-13',3,2),(37,'2021-06-15',0,0),(38,'2021-06-17',2,1),(39,'2021-06-18',1,1),(40,'2021-06-21',0,0),(41,'2021-06-22',4,2),(42,'2021-06-23',2,1),(43,'2021-06-25',2,2),(44,'2021-06-28',1,1),(45,'2021-06-29',1,1),(46,'2021-06-30',1,1),(47,'2021-07-01',4,1),(48,'2021-07-02',2,1),(49,'2021-07-06',3,1),(50,'2021-07-07',1,1),(51,'2021-07-08',1,1);
/*!40000 ALTER TABLE `t_line_chart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_login_log`
--

DROP TABLE IF EXISTS `t_login_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_login_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login_name` varchar(30) NOT NULL,
  `login_nw_ip` varchar(20) NOT NULL,
  `login_gw_ip` varchar(20) DEFAULT NULL,
  `login_gw_cs` varchar(20) DEFAULT NULL,
  `login_agent` varchar(255) NOT NULL,
  `login_status` varchar(10) NOT NULL,
  `login_reason` varchar(30) DEFAULT NULL,
  `login_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_login_log`
--

LOCK TABLES `t_login_log` WRITE;
/*!40000 ALTER TABLE `t_login_log` DISABLE KEYS */;
INSERT INTO `t_login_log` VALUES (9,'saf','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36','失败','用户名无效','2021-05-11 11:29:04'),(10,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36','成功',NULL,'2021-05-11 11:30:10'),(11,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36','成功',NULL,'2021-05-11 14:55:47'),(12,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36','成功',NULL,'2021-05-12 09:59:18'),(13,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36','成功',NULL,'2021-05-12 11:31:44'),(14,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36','成功',NULL,'2021-05-12 15:52:33'),(15,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-13 10:09:42'),(16,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-13 14:44:20'),(17,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-14 11:27:07'),(18,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-14 14:46:45'),(19,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-17 10:02:55'),(20,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-17 14:04:26'),(21,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-18 10:10:09'),(22,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-18 11:34:33'),(23,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-18 11:34:46'),(24,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-18 15:51:25'),(25,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-18 16:04:19'),(26,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-19 10:34:40'),(27,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-19 10:51:55'),(28,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-19 11:10:44'),(29,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-19 15:12:56'),(30,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-21 11:21:21'),(31,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-21 18:25:52'),(32,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-24 10:34:48'),(33,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-24 10:47:41'),(34,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-24 11:00:04'),(35,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-24 14:10:50'),(36,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-25 10:35:15'),(37,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-25 15:24:31'),(38,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-26 10:00:04'),(39,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-26 10:00:33'),(40,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-26 10:00:51'),(41,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-26 10:20:42'),(42,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-26 10:57:03'),(43,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-26 13:36:53'),(44,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-26 13:43:35'),(45,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-26 14:38:15'),(46,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-26 14:38:44'),(47,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-26 14:47:45'),(48,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-26 14:48:22'),(49,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-26 17:28:22'),(50,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-27 14:41:22'),(51,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-31 10:05:18'),(52,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-31 10:12:03'),(53,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-31 10:12:47'),(54,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-31 10:28:01'),(55,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-31 11:20:07'),(56,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-31 11:20:21'),(57,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-31 14:41:10'),(58,'test','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-31 14:48:05'),(59,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-31 14:48:31'),(60,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-31 15:13:57'),(61,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-31 17:47:33'),(62,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-01 09:45:29'),(63,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-01 09:55:10'),(64,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-01 11:01:23'),(65,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-01 13:33:15'),(66,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-02 14:51:49'),(67,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-02 16:29:32'),(68,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-03 10:20:00'),(69,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-04 11:25:46'),(70,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-07 10:35:02'),(71,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','失败','密码错误','2021-06-07 15:20:32'),(72,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-07 15:20:37'),(73,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-08 11:20:45'),(74,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-08 11:21:30'),(75,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-08 14:31:04'),(76,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-08 14:33:02'),(77,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','失败','密码错误','2021-06-08 15:32:42'),(78,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-08 15:32:50'),(79,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-08 15:34:52'),(80,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-08 15:36:16'),(81,'xuzhiwei','10.100.45.192','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-08 15:48:14'),(82,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-09 09:28:32'),(83,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-10 13:57:10'),(84,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-10 13:57:29'),(85,'xuzhiwei','10.0.1.252','114.240.17.23','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','失败','密码错误','2021-06-13 17:34:56'),(86,'xuzhiwei','10.0.1.252','114.240.17.23','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-13 17:35:01'),(87,'admin','10.0.1.252','114.240.17.23','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-13 17:37:23'),(88,'orange','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','失败','用户名无效','2021-06-17 10:26:58'),(89,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-17 14:46:47'),(90,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-18 14:35:27'),(91,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-22 14:22:10'),(92,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-22 14:25:21'),(93,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-22 14:36:07'),(94,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-22 16:08:41'),(95,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-23 10:15:33'),(96,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-23 14:59:33'),(97,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-25 13:57:58'),(98,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-25 14:35:41'),(99,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-28 14:58:17'),(100,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-29 10:24:58'),(101,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-06-30 14:20:07'),(102,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-07-01 13:48:27'),(103,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-07-01 15:32:02'),(104,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-07-01 15:40:07'),(105,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-07-01 15:48:48'),(106,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-07-02 09:54:52'),(107,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-07-02 14:01:00'),(108,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-07-06 09:48:36'),(109,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-07-06 13:58:46'),(110,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-07-06 17:13:13'),(111,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-07-07 09:46:07'),(112,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-07-08 10:32:52');
/*!40000 ALTER TABLE `t_login_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_settings`
--

DROP TABLE IF EXISTS `t_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `login_time` int(5) NOT NULL,
  `register_status` varchar(5) NOT NULL,
  `color_matching` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_settings`
--

LOCK TABLES `t_settings` WRITE;
/*!40000 ALTER TABLE `t_settings` DISABLE KEYS */;
INSERT INTO `t_settings` VALUES (1,'admin',3,'off','black');
/*!40000 ALTER TABLE `t_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_sys_user`
--

DROP TABLE IF EXISTS `t_sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_sys_user` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `alias` varchar(30) NOT NULL,
  `host_user` varchar(25) NOT NULL,
  `host_password` varchar(25) NOT NULL,
  `agreement` varchar(10) NOT NULL,
  `nums` int(5) NOT NULL,
  `remarks` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_sys_user`
--

LOCK TABLES `t_sys_user` WRITE;
/*!40000 ALTER TABLE `t_sys_user` DISABLE KEYS */;
INSERT INTO `t_sys_user` VALUES (1,'运维root用户','0','amxiMTIz','ssh',7,'管理用户');
/*!40000 ALTER TABLE `t_sys_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user`
--

DROP TABLE IF EXISTS `t_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(24) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(24) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mail` varchar(24) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user`
--

LOCK TABLES `t_user` WRITE;
/*!40000 ALTER TABLE `t_user` DISABLE KEYS */;
INSERT INTO `t_user` VALUES (20,'admin','YWRtaW4=','18301022797@163.com'),(27,'xuzhiwei','b3Jhbmdl','954157605@qq.com');
/*!40000 ALTER TABLE `t_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-08 11:45:35
