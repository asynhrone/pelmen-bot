-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Фев 27 2024 г., 17:01
-- Версия сервера: 10.4.32-MariaDB
-- Версия PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `bot`
--

-- --------------------------------------------------------

--
-- Структура таблицы `reports`
--

CREATE TABLE `reports` (
  `author` int(255) NOT NULL,
  `text` text NOT NULL,
  `created` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(25) NOT NULL,
  `bot_id` int(25) NOT NULL,
  `nickname` varchar(255) NOT NULL,
  `balance` bigint(20) DEFAULT NULL,
  `status` varchar(255) NOT NULL,
  `farm-count` bigint(20) DEFAULT NULL,
  `farm-type` int(25) DEFAULT NULL,
  `bitcoin` bigint(255) DEFAULT NULL,
  `last_mining_time` datetime DEFAULT NULL,
  `exp` bigint(20) DEFAULT NULL,
  `fishing_rob_level` int(25) DEFAULT NULL,
  `last_bonus_time` datetime DEFAULT NULL,
  `last_fishing_time` datetime DEFAULT NULL,
  `flat` int(10) DEFAULT NULL,
  `car` int(10) DEFAULT NULL,
  `yacht` int(10) DEFAULT NULL,
  `last_taxi_time` datetime DEFAULT NULL,
  `cups` bigint(255) DEFAULT NULL,
  `last_race_time` datetime DEFAULT NULL,
  `bank_balance` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`bot_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `bot_id` int(25) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
