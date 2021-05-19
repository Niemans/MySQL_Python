CREATE DATABASE  IF NOT EXISTS `dzielnica` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `dzielnica`;
-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: dzielnica
-- ------------------------------------------------------
-- Server version	8.0.23

CREATE USER 'adm'@'localhost' IDENTIFIED BY 'asdf';
grant ALL PRIVILEGES on dzielnica.* TO 'adm'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'user'@'localhost' IDENTIFIED BY 'asdf';
grant SELECT on dzielnica.* TO 'user'@'localhost';
FLUSH PRIVILEGES;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `budynek`
--

DROP TABLE IF EXISTS `budynek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `budynek` (
  `NRB` smallint unsigned NOT NULL AUTO_INCREMENT,
  `l_mieszkan` tinyint unsigned DEFAULT '0',
  `l_wolnych` tinyint unsigned DEFAULT '0',
  `ulica` varchar(50) NOT NULL,
  `dzielnica` varchar(50) NOT NULL,
  `kod_pocztowy` varchar(6) NOT NULL,
  PRIMARY KEY (`NRB`,`ulica`,`dzielnica`)
) ENGINE=InnoDB AUTO_INCREMENT=3454 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `budynek`
--

LOCK TABLES `budynek` WRITE;
/*!40000 ALTER TABLE `budynek` DISABLE KEYS */;
INSERT INTO `budynek` VALUES (2,3,1,'Krowia','Praga','03-711'),(3,20,16,'Stalowa','Praga','03-427'),(7,10,10,'Krowia','Praga','03-711'),(8,7,3,'Szwedzka','Praga','03-419'),(53,5,5,'Szwedzka','Praga','03-420');
/*!40000 ALTER TABLE `budynek` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `bf_del_bud` BEFORE DELETE ON `budynek` FOR EACH ROW begin
	DELETE FROM mieszkanie
    WHERE mieszkanie.dzielnica = old.dzielnica
    AND mieszkanie.ulica = old.ulica
    AND mieszkanie.NRB = old.NRB;
    
    DELETE FROM miejsce_pracy
	WHERE  miejsce_pracy.dzielnica = old.dzielnica
    AND  miejsce_pracy.ulica = old.ulica
    AND  miejsce_pracy.NRB = old.NRB;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `miejsce_pracy`
--

DROP TABLE IF EXISTS `miejsce_pracy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `miejsce_pracy` (
  `IDP` smallint unsigned NOT NULL,
  `NRB` smallint unsigned NOT NULL,
  `ulica` varchar(50) NOT NULL,
  `dzielnica` varchar(50) NOT NULL,
  `data_zatrudnienia` date NOT NULL,
  `data_zwolnienia` date DEFAULT NULL,
  KEY `IDP` (`IDP`),
  KEY `FK_miejsce_pracy` (`NRB`,`ulica`,`dzielnica`),
  CONSTRAINT `FK_miejsce_pracy` FOREIGN KEY (`NRB`, `ulica`, `dzielnica`) REFERENCES `budynek` (`NRB`, `ulica`, `dzielnica`),
  CONSTRAINT `miejsce_pracy_ibfk_1` FOREIGN KEY (`IDP`) REFERENCES `pracownik` (`IDP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `miejsce_pracy`
--

LOCK TABLES `miejsce_pracy` WRITE;
/*!40000 ALTER TABLE `miejsce_pracy` DISABLE KEYS */;
INSERT INTO `miejsce_pracy` VALUES (3,2,'Krowia','Praga','1998-12-23',NULL),(3,7,'Krowia','Praga','1985-11-14',NULL),(6,8,'Szwedzka','Praga','2004-03-07',NULL),(6,53,'Szwedzka','Praga','2013-06-30','2021-05-15'),(11,3,'Stalowa','Praga','2017-10-28',NULL),(5,3,'Stalowa','Praga','1978-01-16',NULL),(9,3,'Stalowa','Praga','1993-08-25',NULL),(10,2,'Krowia','Praga','1985-03-17',NULL),(10,7,'Krowia','Praga','1886-05-30',NULL),(10,8,'Szwedzka','Praga','2008-02-29',NULL),(10,53,'Szwedzka','Praga','2013-06-30',NULL),(9,8,'Szwedzka','Praga','2004-03-07',NULL),(5,2,'Krowia','Praga','2003-09-12',NULL),(5,7,'Krowia','Praga','2002-07-07',NULL),(1,3,'Stalowa','Praga','2018-09-30',NULL),(7,3,'Stalowa','Praga','1984-03-31',NULL),(2,3,'Stalowa','Praga','1999-01-01',NULL),(8,3,'Stalowa','Praga','1999-01-01','2006-07-31'),(12,7,'Krowia','Praga','2017-04-22',NULL),(12,2,'Krowia','Praga','2021-10-15',NULL),(4,53,'Szwedzka','Praga','2000-02-02',NULL);
/*!40000 ALTER TABLE `miejsce_pracy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mieszkanie`
--

DROP TABLE IF EXISTS `mieszkanie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mieszkanie` (
  `NRM` tinyint unsigned NOT NULL,
  `NRB` smallint unsigned NOT NULL,
  `ulica` varchar(50) NOT NULL,
  `dzielnica` varchar(50) NOT NULL,
  `metraz` smallint unsigned NOT NULL,
  `koszt` mediumint unsigned NOT NULL,
  `stan` varchar(8) DEFAULT 'puste',
  `liczba_rezydentow` tinyint unsigned DEFAULT '0',
  `IDM` mediumint NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`IDM`),
  KEY `mieszkanie_FK` (`NRB`,`ulica`,`dzielnica`),
  CONSTRAINT `mieszkanie_FK` FOREIGN KEY (`NRB`, `ulica`, `dzielnica`) REFERENCES `budynek` (`NRB`, `ulica`, `dzielnica`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mieszkanie`
--

LOCK TABLES `mieszkanie` WRITE;
/*!40000 ALTER TABLE `mieszkanie` DISABLE KEYS */;
INSERT INTO `mieszkanie` VALUES (1,2,'Krowia','Praga',10,123456,'kupione',4,1),(2,2,'Krowia','Praga',12,234567,'puste',0,2),(1,3,'Stalowa','Praga',14,345678,'kupione',1,3),(2,3,'Stalowa','Praga',16,234565,'puste',0,4),(3,3,'Stalowa','Praga',18,345676,'puste',0,5),(4,3,'Stalowa','Praga',20,123453,'puste',0,6),(5,3,'Stalowa','Praga',22,453621,'puste',0,7),(6,3,'Stalowa','Praga',24,342515,'puste',0,8),(7,3,'Stalowa','Praga',26,222343,'puste',0,9),(8,3,'Stalowa','Praga',28,345212,'puste',0,10),(9,3,'Stalowa','Praga',30,523412,'kupione',1,11),(10,3,'Stalowa','Praga',15,434123,'kupione',1,12),(11,3,'Stalowa','Praga',17,123424,'puste',0,13),(12,3,'Stalowa','Praga',19,674236,'puste',0,14),(13,3,'Stalowa','Praga',21,657823,'kupione',2,15),(14,3,'Stalowa','Praga',23,583741,'puste',0,16),(15,3,'Stalowa','Praga',24,537812,'puste',0,17),(16,3,'Stalowa','Praga',25,982347,'puste',0,18),(17,3,'Stalowa','Praga',27,561242,'puste',0,19),(18,3,'Stalowa','Praga',29,123672,'puste',0,20),(19,3,'Stalowa','Praga',31,461273,'puste',0,21),(20,3,'Stalowa','Praga',15,764521,'puste',0,22),(1,7,'Krowia','Praga',16,263513,'kupione',2,23),(2,7,'Krowia','Praga',14,273647,'kupione',1,24),(3,7,'Krowia','Praga',15,273461,'puste',0,25),(4,7,'Krowia','Praga',16,123874,'puste',0,26),(5,7,'Krowia','Praga',14,273612,'wynajęte',1,27),(6,7,'Krowia','Praga',17,782361,'puste',0,28),(7,7,'Krowia','Praga',18,123412,'puste',0,29),(8,7,'Krowia','Praga',21,342123,'puste',0,30),(9,7,'Krowia','Praga',23,523412,'puste',0,31),(10,7,'Krowia','Praga',23,125123,'kupione',1,32),(1,8,'Szwedzka','Praga',24,152321,'puste',0,33),(2,8,'Szwedzka','Praga',24,200000,'puste',0,34),(3,8,'Szwedzka','Praga',26,123120,'puste',0,35),(4,8,'Szwedzka','Praga',27,423012,'puste',0,36),(5,8,'Szwedzka','Praga',25,234010,'puste',0,37),(6,8,'Szwedzka','Praga',25,500000,'puste',0,38),(7,8,'Szwedzka','Praga',17,231000,'puste',0,39),(1,53,'Szwedzka','Praga',12,234100,'puste',0,40),(2,53,'Szwedzka','Praga',10,523000,'puste',0,41),(3,53,'Szwedzka','Praga',13,234002,'puste',0,42),(4,53,'Szwedzka','Praga',14,523400,'puste',0,43),(5,53,'Szwedzka','Praga',15,503120,'puste',0,44),(3,2,'Krowia','Praga',12,234567,'kupione',2,45);
/*!40000 ALTER TABLE `mieszkanie` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `af_ins_miesz` AFTER INSERT ON `mieszkanie` FOR EACH ROW begin
    UPDATE budynek
    SET l_wolnych = l_wolnych + 1,
    l_mieszkan = l_mieszkan + 1
    WHERE budynek.NRB IN 
		(SELECT NRB
        FROM mieszkanie
        WHERE IDM  = new.IDM)
	AND budynek.dzielnica IN
		(SELECT dzielnica
        FROM mieszkanie
        WHERE IDM  = new.IDM)
	AND budynek.ulica IN
		(SELECT ulica
        FROM mieszkanie
        WHERE IDM  = new.IDM);
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `bf_del_miesz` BEFORE DELETE ON `mieszkanie` FOR EACH ROW begin
	DELETE FROM osoba
    WHERE osoba.IDM = old. IDM;
    
    UPDATE budynek
    SET l_mieszkan = l_mieszkan - 1
    WHERE (dzielnica, ulica, NRB) IN
		(SELECT dzielnica, ulica, NRB
        FROM mieszkanie
        WHERE dzielnica = old.dzielnica
        AND ulica = old.ulica
        AND NRB = old.NRB);
        
	UPDATE budynek
    SET l_wolnych = l_wolnych - 1
    WHERE (dzielnica, ulica, NRB) IN
		(SELECT dzielnica, ulica, NRB
        FROM mieszkanie
        WHERE dzielnica = old.dzielnica
        AND ulica = old.ulica
        AND NRB = old.NRB
        AND old.liczba_rezydentow = 0);
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `osoba`
--

DROP TABLE IF EXISTS `osoba`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `osoba` (
  `IDO` mediumint unsigned NOT NULL AUTO_INCREMENT,
  `IDM` mediumint NOT NULL,
  `imie` varchar(30) NOT NULL,
  `nazwisko` varchar(30) NOT NULL,
  `nazwisko2` varchar(30) DEFAULT NULL,
  `telefon` int DEFAULT NULL,
  `owner` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`IDO`),
  KEY `osoba_FK2` (`IDM`),
  CONSTRAINT `osoba_FK2` FOREIGN KEY (`IDM`) REFERENCES `mieszkanie` (`IDM`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `osoba`
--

LOCK TABLES `osoba` WRITE;
/*!40000 ALTER TABLE `osoba` DISABLE KEYS */;
INSERT INTO `osoba` VALUES (1,1,'Rombert','Świermk',NULL,123456789,0),(2,45,'Mikołmaj','Molemda',NULL,987654321,1),(3,3,'Anna','Wesołowska','Mlecz',564738292,1),(4,32,'Wiktoria','Zygalska',NULL,347856473,1),(5,27,'Genowefa','Mruczyńska','Zygacz',435787282,1),(6,11,'Zbigniew','Koczulski',NULL,346572985,1),(7,23,'Natalia','Męczybuła',NULL,121212121,1),(8,1,'Olaf','Cimcimrimcim',NULL,234786823,1),(9,1,'Andrzej','Sokolowsky',NULL,823794562,0),(10,23,'Joanna','Kwiatkowska',NULL,524129845,0),(11,12,'Klementyna','Rozdziwikówna',NULL,435972912,1),(12,15,'Nataniel','Mikiewicz',NULL,589728395,1),(13,15,'Roman','Zupa',NULL,534897232,0),(14,24,'Łukasz','Łukaszek',NULL,345234523,1),(15,5,'Maciej','Baran',NULL,123456787,1),(22,45,'Ęward','Ącki',NULL,555555555,0);
/*!40000 ALTER TABLE `osoba` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `af_ins_os` AFTER INSERT ON `osoba` FOR EACH ROW begin
    update budynek
    set l_wolnych = l_wolnych - 1
    where budynek.NRB IN 
		(SELECT NRB
        FROM mieszkanie
        Where liczba_rezydentow = 0
        AND IDM IN 
			(SELECT IDM
            FROM osoba
            WHERE IDM = new.IDM))
	and budynek.dzielnica IN 
		(SELECT dzielnica
        FROM mieszkanie
        Where liczba_rezydentow = 0
        AND IDM IN 
			(SELECT IDM
            FROM osoba
            WHERE IDM = new.IDM))
	and budynek.ulica IN 
		(SELECT ulica
        FROM mieszkanie
        Where liczba_rezydentow = 0
        AND IDM IN 
			(SELECT IDM
            FROM osoba
            WHERE IDM = new.IDM));
            
	update mieszkanie
    set liczba_rezydentow = liczba_rezydentow + 1
    where mieszkanie.IDM IN 
		(SELECT osoba.IDM
		FROM osoba
        WHERE osoba.IDM = new.IDM); 
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `bf_up_os` BEFORE UPDATE ON `osoba` FOR EACH ROW begin
	IF old.IDM <> new.IDM
    THEN
    		update mieszkanie
		set liczba_rezydentow = liczba_rezydentow - 1
		where mieszkanie.IDM IN 
			(SELECT osoba.IDM
			FROM osoba
			WHERE osoba.IDM = old.IDM); 
            
		update budynek
		set l_wolnych = l_wolnych + 1
		where budynek.NRB IN 
			(SELECT NRB
			FROM mieszkanie
			Where liczba_rezydentow = 0
            AND IDM IN 
				(SELECT IDM
				FROM osoba
				WHERE IDM = old.IDM))
		and budynek.dzielnica IN 
			(SELECT dzielnica
			FROM mieszkanie
			Where liczba_rezydentow = 0
            AND IDM IN 
				(SELECT IDM
				FROM osoba
				WHERE IDM = old.IDM))
		and budynek.ulica IN 
			(SELECT ulica
			FROM mieszkanie
			Where liczba_rezydentow = 0
            AND IDM IN 
				(SELECT IDM
				FROM osoba
				WHERE IDM = old.IDM));
	end IF;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `af_up_os` AFTER UPDATE ON `osoba` FOR EACH ROW begin
	IF old.IDM <> new.IDM
    THEN
		update budynek
		set l_wolnych = l_wolnych - 1
		where budynek.NRB IN 
			(SELECT NRB
			FROM mieszkanie
			Where liczba_rezydentow = 0
			AND IDM IN 
				(SELECT IDM
				FROM osoba
				WHERE IDM = new.IDM))
		and budynek.dzielnica IN 
			(SELECT dzielnica
			FROM mieszkanie
			Where liczba_rezydentow = 0
			AND IDM IN 
				(SELECT IDM
				FROM osoba
				WHERE IDM = new.IDM))
		and budynek.ulica IN 
			(SELECT ulica
			FROM mieszkanie
			Where liczba_rezydentow = 0
			AND IDM IN 
				(SELECT IDM
				FROM osoba
				WHERE IDM = new.IDM));

        
		update mieszkanie
		set liczba_rezydentow = liczba_rezydentow + 1
		where mieszkanie.IDM IN 
			(SELECT osoba.IDM
			FROM osoba
			WHERE osoba.IDM = new.IDM); 
	end IF;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `pracownik`
--

DROP TABLE IF EXISTS `pracownik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pracownik` (
  `IDP` smallint unsigned NOT NULL AUTO_INCREMENT,
  `IDZ` smallint unsigned NOT NULL,
  `Imie` varchar(30) NOT NULL,
  `Nazwisko` varchar(30) NOT NULL,
  `Nazwisko2` varchar(30) DEFAULT NULL,
  `placa` decimal(12,2) NOT NULL,
  PRIMARY KEY (`IDP`),
  KEY `IDZ` (`IDZ`),
  CONSTRAINT `pracownik_ibfk_1` FOREIGN KEY (`IDZ`) REFERENCES `zawod` (`IDZ`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pracownik`
--

LOCK TABLES `pracownik` WRITE;
/*!40000 ALTER TABLE `pracownik` DISABLE KEYS */;
INSERT INTO `pracownik` VALUES (1,3,'Lucjan','Kisiel',NULL,3456.78),(2,4,'Magdalena','Sałata','Ogroszewska',9876.54),(3,1,'Tomasz','Mak',NULL,6591.54),(4,5,'Marek','Ymski',NULL,5976.11),(5,2,'Łucja','Zymska',NULL,2500.00),(6,1,'Natalia','Kot',NULL,11485.90),(7,4,'Szymon','Żuk',NULL,10000.00),(8,5,'Joanna','Kapucińska','Żuk',11500.00),(9,2,'Dariusz','Filipowicz',NULL,4805.00),(10,2,'Zuzanna','Micka',NULL,4999.99),(11,1,'Paulina','Mućmucińska',NULL,7000.15),(12,5,'Michał','Kapeć',NULL,8300.00);
/*!40000 ALTER TABLE `pracownik` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `bf_del_prac` BEFORE DELETE ON `pracownik` FOR EACH ROW begin
	DELETE FROM miejsce_pracy
    WHERE IDP IN 
		(SELECT IDP
        FROM pracownik 
        WHERE IDP = old.IDP);
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `zawod`
--

DROP TABLE IF EXISTS `zawod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zawod` (
  `IDZ` smallint unsigned NOT NULL AUTO_INCREMENT,
  `nazwa` varchar(30) DEFAULT NULL,
  `min_placa` mediumint NOT NULL,
  `max_placa` mediumint NOT NULL,
  PRIMARY KEY (`IDZ`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zawod`
--

LOCK TABLES `zawod` WRITE;
/*!40000 ALTER TABLE `zawod` DISABLE KEYS */;
INSERT INTO `zawod` VALUES (1,'zarządca',6000,13000),(2,'gospodarz budynku',2500,5000),(3,'śmieciarz',2500,5000),(4,'ochroniarz',3500,10500),(5,'administrator',4500,11500);
/*!40000 ALTER TABLE `zawod` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `bf_del_zaw` BEFORE DELETE ON `zawod` FOR EACH ROW begin
	DELETE FROM pracownik
    WHERE IDZ IN 
		(SELECT IDZ
        FROM zawod 
        WHERE IDZ = old.IDZ);
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Dumping events for database 'dzielnica'
--

--
-- Dumping routines for database 'dzielnica'
--
/*!50003 DROP PROCEDURE IF EXISTS `delete_bud` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_bud`(in dziel varchar(50), ul varchar(50), nr smallint unsigned)
    SQL SECURITY INVOKER
Begin
	DELETE FROM budynek
    WHERE dzielnica = dziel
    AND ulica = ul
    AND NRB = nr;
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `delete_miej` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_miej`(in dziel varchar(50), ul varchar(50), nr smallint unsigned, id_prac smallint unsigned)
    SQL SECURITY INVOKER
Begin
	delete from miejsce_pracy
	WHERE IDP = id_prac
    AND dzielnica = dziel
    AND ulica = ul
    AND NRB = nr;
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `delete_miesz` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_miesz`(in id_miesz mediumint)
    SQL SECURITY INVOKER
Begin
    DELETE FROM mieszkanie
    WHERE IDM = id_miesz;
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `delete_os` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_os`(in id_os mediumint)
    SQL SECURITY INVOKER
Begin
    DELETE FROM osoba
    WHERE IDO = id_os;
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `delete_prac` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_prac`(in id_prac smallint unsigned)
    SQL SECURITY INVOKER
Begin
    DELETE FROM pracownik
    WHERE IDP = id_prac;
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `delete_zaw` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_zaw`(in id_zaw smallint unsigned)
    SQL SECURITY INVOKER
Begin
	DELETE FROM zawod
	WHERE IDZ = id_zaw;
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_bud` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_bud`(in dziel varchar(50), ul varchar(50), nr smallint unsigned, kod varchar(6), liczba tinyint unsigned)
    SQL SECURITY INVOKER
Begin
	INSERT INTO budynek (dzielnica, ulica, NRB, kod_pocztowy, l_mieszkan, l_wolnych)
    VALUES (dziel, ul, nr, kod, liczba, liczba);
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_miej` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_miej`(in dziel varchar(50), ul varchar(50), nr smallint unsigned, id_prac smallint unsigned, data_zat DATE)
    SQL SECURITY INVOKER
Begin
	INSERT INTO miejsce_pracy (dzielnica, ulica, NRB, IDP, data_zatrudnienia)
    VALUES (dziel, ul, nr, id_prac, data_zat);
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_miesz` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_miesz`(in dziel varchar(50), ul varchar(50), nr smallint unsigned, nr_miesz tinyint unsigned, metr smallint unsigned, cost mediumint unsigned )
    SQL SECURITY INVOKER
Begin
	INSERT INTO mieszkanie (dzielnica, ulica, NRB, NRM, metraz, koszt)
    VALUES (dziel, ul, nr, nr_miesz, metr, cost);
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_os` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_os`(in id_miesz mediumint, im varchar(30), naz varchar(30), naz2 varchar(30), tel int, own tinyint(1))
    SQL SECURITY INVOKER
Begin
	IF naz2 = 'n'
    THEN
		INSERT INTO osoba (IDM, imie, nazwisko, telefon, owner)
		VALUES (id_miesz, im, naz, tel, own);
	ELSE
		INSERT INTO osoba (IDM, imie, nazwisko, nazwisko2, telefon, owner)
		VALUES (id_miesz, im, naz, naz2, tel, own);
	end IF;
    
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_prac` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_prac`(in im varchar(30), naz varchar(30), naz2 varchar(30), plac DECIMAL(12,2), id_zaw smallint unsigned)
    SQL SECURITY INVOKER
Begin
	IF (naz2 = 'n')
    THEN
		INSERT INTO pracownik(imie, nazwisko, placa, IDZ)
		VALUES (im, naz, plac, id_zaw);
	ELSE
		INSERT INTO pracownik(imie, nazwisko, nazwisko2,placa, IDZ)
		VALUES (im, naz, naz2, plac, id_zaw);
	end IF;
    
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_zaw` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_zaw`(in naz varchar(30), min mediumint, max mediumint)
    SQL SECURITY INVOKER
Begin
	INSERT INTO zawod (nazwa, min_placa, max_placa)
    VALUES (naz, min, max);
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `update_bud` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_bud`(in dziel varchar(50), ul varchar(50), nr smallint unsigned, new_nr smallint unsigned, kod varchar(6))
    SQL SECURITY INVOKER
Begin
	SET FOREIGN_KEY_CHECKS=0;	
	Update budynek
    Set NRB = new_nr, kod_pocztowy = kod
    WHERE dzielnica = dziel
    AND ulica = ul
    AND NRB = nr;
    
    Update miejsce_pracy
    set NRB = new_nr
    WHERE dzielnica = dziel
    AND ulica = ul
    AND NRB = nr;
    
    Update mieszkanie
    set NRB = new_nr
    WHERE dzielnica = dziel
    AND ulica = ul
    AND NRB = nr;
    SET FOREIGN_KEY_CHECKS=1;
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `update_miej` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_miej`(in dziel varchar(50), ul varchar(50), nr smallint unsigned, new_dziel varchar(50), new_ul varchar(50), new_nr smallint unsigned , id_prac smallint unsigned, data_zat DATE)
    SQL SECURITY INVOKER
Begin
	Update miejsce_pracy
	set dzielnica = new_dziel, ulica = new_ul, NRB = new_nr, data_zatrudnienia = data_zat
	WHERE IDP = id_prac
    AND dzielnica = dziel
    AND ulica = ul
    AND NRB = nr;
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `update_miej_zwolnienie` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_miej_zwolnienie`(in dziel varchar(50), ul varchar(50), nr smallint unsigned, id_prac smallint unsigned, data_zwol DATE)
    SQL SECURITY INVOKER
Begin
	Update miejsce_pracy
	set  data_zwolnienia = data_zwol
	WHERE IDP = id_prac
    AND dzielnica = dziel
    AND ulica = ul
    AND NRB = nr;
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `update_miesz` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_miesz`(in id_miesz mediumint, metr smallint unsigned, cost mediumint unsigned, n_stan varchar(8))
    SQL SECURITY INVOKER
Begin
    Update mieszkanie
    set metraz = metr, koszt = cost, stan = n_stan
    WHERE IDM = id_miesz;
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `update_os` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_os`(in id_os mediumint unsigned, id_miesz mediumint, im varchar(30), naz varchar(30), naz2 varchar(30), tel int, own tinyint(1))
    SQL SECURITY INVOKER
Begin
 	IF (naz2 = 'n')
    THEN
		Update osoba
		set IDM = id_miesz, imie = im, nazwisko = naz, telefon = tel, owner = own
		WHERE IDO = id_os;
	ELSE
		Update osoba
		set IDM = id_miesz, imie = im, nazwisko = naz, nazwisko2 = naz2 , telefon = tel, owner = own
		WHERE IDO = id_os;
    end IF;
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `update_prac` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_prac`(in id_prac smallint unsigned, id_zaw mediumint, im varchar(30), naz varchar(30), naz2 varchar(30), zarobek DECIMAL(12,2))
    SQL SECURITY INVOKER
Begin
 	IF (naz2 = 'n')
    THEN
		Update pracownik
		set IDZ = id_zaw, imie = im, nazwisko = naz, placa = zarobek
		WHERE IDP = id_prac;
	ELSE
		Update pracownik
		set IDZ = id_zaw, imie = im, nazwisko = naz, nazwisko2 = naz2, placa = zarobek
		WHERE IDP = id_prac;
    end IF;
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `update_zaw` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_zaw`(in naz varchar(30), min mediumint, max mediumint, id_zaw smallint unsigned)
    SQL SECURITY INVOKER
Begin
	UPDATE zawod
    SET nazwa = naz, min_placa = min, max_placa = max
	WHERE IDZ = id_zaw;
 end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-19 15:44:19
