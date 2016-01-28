CREATE TABLE IF NOT EXISTS `error_scarer_user` (
  `id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS `error_scarer_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `level` varchar(140),
  `os` varchar(140),
  `message` text,
  `created_at` bigint(20),
  `device` varchar(140),
  `app_version` varchar(140),
  `page` varchar(140),
  `page_type` varchar(140),
  `buzz_id` bigint(20),
  `buzz` varchar(255),
  `stack` text,
  PRIMARY KEY (`id`),
  KEY `error_scarer_log_level` (`level`),
  KEY `error_scarer_log_created_at` (`created_at`),
  KEY `error_scarer_log_buzz_id` (`buzz_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE IF NOT EXISTS `error_scarer_userlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `log_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
