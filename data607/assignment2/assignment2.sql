--
-- Create database `ippolito-films`
--
CREATE DATABASE IF NOT EXISTS `ippolito-films`;
use `ippolito-films`;

--
-- Create `films` table
--
DROP TABLE IF EXISTS `films`;
CREATE TABLE `films` (
	`film_id` int(11) NOT NULL,
	`film_title` varchar(255) NOT NULL,
	PRIMARY KEY (`film_id`)
);

--
-- Insert data into `film` table
--

LOCK TABLES `films` WRITE;
INSERT INTO `films` VALUES
	(1, 'The Outpost'),
	(2, 'The Invisible Man'),
	(3, 'The Platform (El Hoyo)'),
	(4, 'Mulan'),
	(5, 'Parasite'),
	(6, 'Uncut Gems');
UNLOCK TABLES;

--
-- Create `ratings` table
--
DROP TABLE IF EXISTS `ratings`;
CREATE TABLE `ratings` (
	`rating_id` int(11) NOT NULL,
	`rating_text` varchar(255) NOT NULL,
	PRIMARY KEY (`rating_id`)
);

--
-- Insert data into `film` table
--

LOCK TABLES `ratings` WRITE;
INSERT INTO `ratings` VALUES
	(0, 'I didn\'t see this film.'),
	(1, 'What\'s the strongest word for hate?'),
	(2, 'Boo. :('),
	(3, 'Meh, take it or leave it.'),
	(4, 'Not too shabby!'),
	(5, 'I love it so much!');
UNLOCK TABLES;

--
-- Create `respondents` table
--
DROP TABLE IF EXISTS `respondents`;
CREATE TABLE `respondents` (
	`respondent_id` int(11) NOT NULL,
	`started_at` timestamp NOT NULL,
	`sec_taken` int(11) NOT NULL,
	`min_delay` dec(8,1) NOT NULL,
	PRIMARY KEY (`respondent_id`)
);

--
-- Insert data into `respondents` table
--

LOCK TABLES `respondents` WRITE;
INSERT INTO `respondents` VALUES
	(1, '2021-02-09 22:22:43', 38, 1.7),
	(2, '2021-02-09 22:22:41', 102, 1.7),
	(3, '2021-02-09 22:54:24', 89, 33.4),
	(4, '2021-02-09 23:13:28', 359, 52.5),
	(5, '2021-02-10 00:07:17', 38, 106.3),
	(6, '2021-02-10 05:05:48', 38, 404.8),
	(7, '2021-02-10 05:51:49', 45, 450.8),
	(8, '2021-02-10 06:21:53', 59, 480.9),
	(9, '2021-02-10 07:38:08', 37, 557.1),
	(10, '2021-02-10 07:42:28', 28, 561.5),
	(11, '2021-02-10 08:06:31', 38, 585.5),
	(12, '2021-02-10 08:35:19', 29, 614.3),
	(13, '2021-02-10 08:43:09', 29, 622.1),
	(14, '2021-02-10 09:08:07', 64, 647.1),
	(15, '2021-02-10 09:24:02', 103, 663),
	(16, '2021-02-10 09:55:18', 22, 694.3),
	(17, '2021-02-10 10:05:33', 26, 704.6),
	(18, '2021-02-10 11:40:02', 207, 799),
	(19, '2021-02-10 12:13:10', 103, 832.2),
	(20, '2021-02-10 12:52:30', 54, 871.5),
	(21, '2021-02-11 05:51:48', 380, 1890.8);
UNLOCK TABLES;

--
-- Create `genres` table
--
DROP TABLE IF EXISTS `genres`;
CREATE TABLE `genres` (
	`genre_id` int(11) NOT NULL,
	`genre` varchar(255) NOT NULL,
	PRIMARY KEY (`genre_id`)
);

--
-- Insert data into `genres` table
--

LOCK TABLES `genres` WRITE;
INSERT INTO `genres` VALUES
	(1, 'comedy'),
	(2, 'mystery and thriller'),
	(3, 'drama'),
	(4, 'war'),
	(5, 'aventure'),
	(6, 'action'),
	(7, 'sci fi'),
	(8, 'horror');
UNLOCK TABLES;

--
-- Create `film_genres` table
--
DROP TABLE IF EXISTS `film_genres`;
CREATE TABLE `film_genres` (
	`film_genre_id` int(11) NOT NULL,
	`film_fk` int(11) NOT NULL,
	`genre_fk` int(11) NOT NULL,
	PRIMARY KEY (`film_genre_id`)
);

--
-- Insert data into `film_genres` table
--

LOCK TABLES `film_genres` WRITE;
INSERT INTO `film_genres` VALUES
	(1, 1, 4),
	(2, 1, 3),
	(3, 2, 8),
	(4, 2, 2),
	(5, 3, 7),
	(6, 3, 2),
	(7, 4, 5),
	(8, 4, 6),
	(9, 5, 1),
	(10, 5, 2),
	(11, 5, 3),
	(12, 6, 1),
	(13, 6, 2);
UNLOCK TABLES;

--
-- Create `responses` table
--		response_id:		unique primary key
--		respondent_num:		survey respondent number
--		film_fk:			foreign key referencing `film_id` in the `films` table
--		rating_fk:			foreign key referencing `rating_id` in the `ratings` table
--
DROP TABLE IF EXISTS `responses`;
CREATE TABLE `responses` (
	`response_id` int(11) NOT NULL,
	`respondent_fk` int(11) NOT NULL,
	`film_fk` int(11) NOT NULL,
	`rating_fk` int(11),
	PRIMARY KEY (`response_id`)
);

--
-- Insert data into `responses` table
--

LOCK TABLES `responses` WRITE;
INSERT INTO `responses` VALUES
	(1, 1, 1, NULL),
	(2, 1, 2, NULL),
	(3, 1, 3, NULL),
	(4, 1, 4, NULL),
	(5, 1, 5, 5),
	(6, 1, 6, NULL),
	(7, 2, 1, NULL),
	(8, 2, 2, 4),
	(9, 2, 3, NULL),
	(10, 2, 4, 4),
	(11, 2, 5, NULL),
	(12, 2, 6, NULL),
	(13, 3, 1, NULL),
	(14, 3, 2, 2),
	(15, 3, 3, 5),
	(16, 3, 4, NULL),
	(17, 3, 5, 5),
	(18, 3, 6, 4),
	(19, 4, 1, NULL),
	(20, 4, 2, NULL),
	(21, 4, 3, NULL),
	(22, 4, 4, NULL),
	(23, 4, 5, 5),
	(24, 4, 6, 3),
	(25, 5, 1, NULL),
	(26, 5, 2, NULL),
	(27, 5, 3, NULL),
	(28, 5, 4, NULL),
	(29, 5, 5, NULL),
	(30, 5, 6, NULL),
	(31, 6, 1, NULL),
	(32, 6, 2, NULL),
	(33, 6, 3, NULL),
	(34, 6, 4, NULL),
	(35, 6, 5, 5),
	(36, 6, 6, NULL),
	(37, 7, 1, NULL),
	(38, 7, 2, NULL),
	(39, 7, 3, NULL),
	(40, 7, 4, 4),
	(41, 7, 5, NULL),
	(42, 7, 6, NULL),
	(43, 8, 1, NULL),
	(44, 8, 2, NULL),
	(45, 8, 3, NULL),
	(46, 8, 4, NULL),
	(47, 8, 5, NULL),
	(48, 8, 6, NULL),
	(49, 9, 1, NULL),
	(50, 9, 2, NULL),
	(51, 9, 3, NULL),
	(52, 9, 4, NULL),
	(53, 9, 5, NULL),
	(54, 9, 6, NULL),
	(55, 10, 1, 3),
	(56, 10, 2, 4),
	(57, 10, 3, 5),
	(58, 10, 4, NULL),
	(59, 10, 5, 4),
	(60, 10, 6, 4),
	(61, 11, 1, NULL),
	(62, 11, 2, NULL),
	(63, 11, 3, NULL),
	(64, 11, 4, 4),
	(65, 11, 5, NULL),
	(66, 11, 6, NULL),
	(67, 12, 1, NULL),
	(68, 12, 2, NULL),
	(69, 12, 3, NULL),
	(70, 12, 4, NULL),
	(71, 12, 5, NULL),
	(72, 12, 6, NULL),
	(73, 13, 1, NULL),
	(74, 13, 2, NULL),
	(75, 13, 3, NULL),
	(76, 13, 4, NULL),
	(77, 13, 5, 5),
	(78, 13, 6, NULL),
	(79, 14, 1, NULL),
	(80, 14, 2, NULL),
	(81, 14, 3, 4),
	(82, 14, 4, 3),
	(83, 14, 5, 5),
	(84, 14, 6, 5),
	(85, 15, 1, NULL),
	(86, 15, 2, 3),
	(87, 15, 3, NULL),
	(88, 15, 4, 4),
	(89, 15, 5, 5),
	(90, 15, 6, 2),
	(91, 16, 1, NULL),
	(92, 16, 2, NULL),
	(93, 16, 3, NULL),
	(94, 16, 4, 4),
	(95, 16, 5, NULL),
	(96, 16, 6, NULL),
	(97, 17, 1, NULL),
	(98, 17, 2, NULL),
	(99, 17, 3, NULL),
	(100, 17, 4, 4),
	(101, 17, 5, NULL),
	(102, 17, 6, NULL),
	(103, 18, 1, NULL),
	(104, 18, 2, NULL),
	(105, 18, 3, NULL),
	(106, 18, 4, NULL),
	(107, 18, 5, 5),
	(108, 18, 6, 5),
	(109, 19, 1, NULL),
	(110, 19, 2, NULL),
	(111, 19, 3, NULL),
	(112, 19, 4, NULL),
	(113, 19, 5, NULL),
	(114, 19, 6, NULL),
	(115, 20, 1, NULL),
	(116, 20, 2, NULL),
	(117, 20, 3, NULL),
	(118, 20, 4, NULL),
	(119, 20, 5, NULL),
	(120, 20, 6, NULL),
	(121, 21, 1, NULL),
	(122, 21, 2, NULL),
	(123, 21, 3, NULL),
	(124, 21, 4, NULL),
	(125, 21, 5, NULL),
	(126, 21, 6, NULL);
UNLOCK TABLES;
