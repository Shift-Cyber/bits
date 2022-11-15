USE hack_a_bit;

CREATE TABLE IF NOT EXISTS `email_tokens` (
    `token` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `issued_epoch` varchar(255) NOT NULL,
  PRIMARY KEY (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `discord_association` (
    `email` varchar(255) NOT NULL,
    `discord_id` varchar(255) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
