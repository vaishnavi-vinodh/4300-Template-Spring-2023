-- MySQL dump 10.13  Distrib 8.0.32, for macos13.0 (x86_64)
--
-- Host: localhost    Database: kardashiandb
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `kardashiandb`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `kardashiandb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `kardashiandb`;

--
-- Table structure for table `recipes`
--

DROP TABLE IF EXISTS `recipes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipes` (
  `name` varchar(107) DEFAULT NULL,
  `image_url` varchar(227) DEFAULT NULL,
  `description` varchar(980) DEFAULT NULL,
  `cuisine` varchar(25) DEFAULT NULL,
  `course` varchar(22) DEFAULT NULL,
  `diet` varchar(28) DEFAULT NULL,
  `prep_time` varchar(15) DEFAULT NULL,
  `ingredients` varchar(2235) DEFAULT NULL,
  `instructions` varchar(3529) DEFAULT NULL,
  `image_available` bit(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipes`
--

LOCK TABLES `recipes` WRITE;
/*!40000 ALTER TABLE `recipes` DISABLE KEYS */;
INSERT INTO `recipes` VALUES ('0','Doddapatre Tambuli Recipe (Karpooravalli Thayir Pachadi)','https://www.archanaskitchen.com/images/archanaskitchen/Indian_Raitas/Doddapatre_Tambuli_Recipe_Karuveppilai_Thayir_Pachadi-1.jpg','Doddapatre Tambuli Recipe','Indian','Side Dish','Vegetarian','Total in 30 M','-- 4 cups Indian borage (Doddapatre) | cleaned and washed -- 1/2 cup Curd (Dahi / Yogurt) -- 1 tablespoon Cumin seeds (Jeera) -- 1/2 teaspoon Whole Black Peppercorns -- 1/4 cup Dessicated Coconut --Salt | to taste -- 2 tablespoons Ghee -',_binary ''),('1','Fish Tandoori Recipe','https://www.archanaskitchen.com/images/archanaskitchen/1-Author/poojanadkarni/Fish_Tandoori.jpg','Have you ever tried out f','North Indian Recipes','Appetizer','High Protein No','Total in 80 M','-- 1 Fish | nicely washed with bones on (I used Pompano) -For marination-- 2 tablespoons Curd (Dahi / Yogurt) -- 1/4 cup Onions | finely chopped -- 2 Green Chillies | chopped -- 1 tablespoon Tandoori masala -- 1 teaspoon Ginger Garlic Paste -- 1 teaspoon Red Chilli powder -- 1 teaspoon Garam masala powder -- 1 teaspoon Coriander Powder (Dhania) -- 1/2 teaspoon Cumin powder (Jeera) -- 1 tablespoon Coriander (Dhania) Leaves | finely chopped -- 1 tablespoon Oil --Salt | to taste -',_binary ''),('2','Arbi Shimla Mirch Sabzi Recipe – Colocasia Capsicum Sabzi','https://www.archanaskitchen.com/images/archanaskitchen/1-Author/sibyl-archanaskitchen.com/Simla_Mirchi_Arbi_Sabzi_Recipe__Capsicum__Colocasia_Dry_Curry_.jpg','Arbi Shimla Mirch Sabzi R','North Indian Recipes','Main Course','No Onion No Gar','Total in 55 M','-- 300 grams Colocasia root (Arbi) -- 1 Green Bell Pepper (Capsicum) | diced -- 1 Tomato | chopped -- 1 inch Ginger | grated -- 1 teaspoon Coriander Powder (Dhania) -- 1/2 teaspoon Turmeric powder (Haldi) -- 1/2 teaspoon Red Chilli powder -- 1 teaspoon Garam masala powder --Salt | according to taste --Oil | for cooking -',_binary ''),('3','Ambur Style Brinjal Curry Recipe','https://www.archanaskitchen.com/images/archanaskitchen/1-Author/happytrioexplains-gmail.com/Brinjal_curry_for_Biryani.jpg','Brinjal Curry is prepared','Indian','Lunch','Vegetarian','Total in 20 M','-- 5 Brinjal (Baingan / Eggplant) -- 1 Onion -- 2 Tomatoes -- 1 tablespoon Ginger Garlic Paste -- 2 teaspoon Red Chilli powder -- 1/4 teaspoon Turmeric powder (Haldi) -- 1/2 teaspoon Coriander Powder (Dhania) --Salt | as needed -- 20 grams Tamarind | size of a small gooseberry -- 2 tablespoon Gingelly oil -- sprig Curry leaves -- 1/2 teaspoon Mustard seeds (Rai/ Kadugu) -- 4 Whole Black Peppercorns -To Roast and Grind:-- 2 tablespoons Roasted Peanuts (Moongphali) -- 1 tablespoon Sesame seeds (Til seeds) -- 1 tablespoon Fresh coconut -',_binary ''),('4','Mavinakayi Menasinakai Curry Recipe  - Raw Mango Coconut Curry','https://www.archanaskitchen.com/images/archanaskitchen/0-Archanas-Kitchen-Recipes/2019/Raw_Mango_Coconut_Curry__Mavinakayi_Menasinakai_Curry_Recipe_11_1600.jpg','Mangalorean Mavinakayi Me','Mangalorean','Side Dish','Vegetarian','Total in 35 M','-- 1 cup Mango (Raw) | diced -- 2 tablespoons Jaggery -- 1/4 teaspoon Turmeric powder (Haldi) -- 1/4 cup Tamarind Water --Salt | to taste -For Ground Masala-- 1 cup Fresh coconut | grated -- 2 teaspoons White Urad Dal (Split) -- 1 teaspoon Chana dal (Bengal Gram Dal) -- 1/4 teaspoon Methi Seeds (Fenugreek Seeds) -- 1/2 teaspoon Cumin seeds (Jeera) -- 2 teaspoons Sesame seeds (Til seeds) -- 4 Dry Red Chillies | (adjust) -For Tempering:-- 2 teaspoons Coconut Oil -- 1/4 teaspoon SSP Asafoetida (Hing) -- 1 teaspoon Mustard seeds (Rai/ Kadugu) --Curry leaves | a few -',_binary ''),('5','Cabbage And Carrot Thoran Recipe','https://www.archanaskitchen.com/images/archanaskitchen/1-Author/Karthika_Gopalakrishnan/Cabbage_and_Carrot_Thoran.jpg','Cabbage and Carrot Thoran','Kerala Recipes','Lunch','Vegetarian','Total in 40 M','-- 3 Carrots (Gajjar) | grated -- 1/2 Cabbage (Patta Gobi/ Muttaikose) | finely chopped -- 1 Onion | finely chopped -- 4 Green Chillies | slit -- 1/2 teaspoon Turmeric powder (Haldi) -- 1 teaspoon Cumin powder (Jeera) -- 1 tablespoon Oil -- 1/2 teaspoon Mustard seeds (Rai/ Kadugu) -- 1/2 cup Fresh coconut | grated -- 6 Curry leaves --Salt | as required -',_binary ''),('6','Konkani Style Mooga Ghushi Recipe-Sprouted Whole Green Gram In Tangy Coconut Gravy','https://www.archanaskitchen.com/images/archanaskitchen/0-Archanas-Kitchen-Recipes/2017/19-april/Mooga_Ghushi_Recipe_sprouted_green_mong_in_coocnut_curry-1.jpg','‘Mooga Ghushi’ is a sprou','Konkan','Lunch','Vegetarian','Total in 30 M','-- 1/2 cup Green Moong Dal (Whole) -For the coconut masala-- 1/2 cup Fresh coconut | grated -- 2 Dry Red Chilli | lightly roasted -- 1/4 teaspoon Tamarind Paste | or 1 small gooseberry sized tamarind (remove seeds and fibre if any) -- 2 teaspoons Coconut Oil -- 1 teaspoon Mustard seeds (Rai/ Kadugu) -- 1 sprig Curry leaves --Salt | to taste -',_binary '');

/*!40000 ALTER TABLE `recipes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-27 19:50:03
