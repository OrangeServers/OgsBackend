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
-- Table structure for table `t_acc_user`
--

DROP TABLE IF EXISTS `t_acc_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_acc_user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `alias` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `usrole` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mail` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `remarks` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_acc_user`
--

LOCK TABLES `t_acc_user` WRITE;
/*!40000 ALTER TABLE `t_acc_user` DISABLE KEYS */;
INSERT INTO `t_acc_user` VALUES (1,'管理员','admin','YWRtaW4=','admin','18301022797@163.com','超级管理员');
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
INSERT INTO `t_auth_host` VALUES (1,'所有权限','admin',NULL,'default,yace','管理员权限'),(3,'test','admin,xuzhiwei','','docker,yace,test','测试1');
/*!40000 ALTER TABLE `t_auth_host` ENABLE KEYS */;
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
-- Table structure for table `t_login_date`
--

DROP TABLE IF EXISTS `t_login_date`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_login_date` (
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_login_date`
--

LOCK TABLES `t_login_date` WRITE;
/*!40000 ALTER TABLE `t_login_date` DISABLE KEYS */;
INSERT INTO `t_login_date` VALUES (9,'saf','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36','失败','用户名无效','2021-05-11 11:29:04'),(10,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36','成功',NULL,'2021-05-11 11:30:10'),(11,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36','成功',NULL,'2021-05-11 14:55:47'),(12,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36','成功',NULL,'2021-05-12 09:59:18'),(13,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36','成功',NULL,'2021-05-12 11:31:44'),(14,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36','成功',NULL,'2021-05-12 15:52:33'),(15,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-13 10:09:42'),(16,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-13 14:44:20'),(17,'admin','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-14 11:27:07'),(18,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-14 14:46:45'),(19,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-17 10:02:55'),(20,'xuzhiwei','10.0.51.89','124.202.173.82','北京市','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','成功',NULL,'2021-05-17 14:04:26');
/*!40000 ALTER TABLE `t_login_date` ENABLE KEYS */;
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

-- Dump completed on 2021-05-17 15:33:58
