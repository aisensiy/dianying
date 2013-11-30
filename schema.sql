-- Create syntax for TABLE 'follow'
CREATE TABLE IF NOT EXISTS `follow` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `src_account_id` int(10) unsigned DEFAULT NULL,
  `dst_account_id` int(10) unsigned DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create syntax for TABLE 'message'
CREATE TABLE IF NOT EXISTS `message` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `src_user_id` int(10) unsigned DEFAULT NULL,
  `dst_user_id` int(10) unsigned DEFAULT NULL,
  `content` varchar(128) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `src_user_id` (`src_user_id`),
  KEY `dst_user_id` (`dst_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create syntax for TABLE 'movie'
CREATE TABLE IF NOT EXISTS `movie` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `mid` int(10) unsigned DEFAULT NULL,
  `type` tinyint(4) DEFAULT NULL,
  `params` text,
  `is_latest` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create syntax for TABLE 'user'
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create syntax for TABLE 'user_account'
CREATE TABLE IF NOT EXISTS `user_account` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned DEFAULT NULL,
  `account_id` varchar(20) DEFAULT NULL,
  `access_token` varchar(32) DEFAULT NULL,
  `params` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create syntax for TABLE 'user_token'
CREATE TABLE IF NOT EXISTS `user_token` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned DEFAULT NULL,
  `token` varchar(32) DEFAULT NULL,
  `expire_time` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user_view` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `src_user_id` int(10) unsigned DEFAULT NULL,
  `dst_user_id` int(10) unsigned DEFAULT NULL,
  `viewed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`src_user_id`, `dst_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
