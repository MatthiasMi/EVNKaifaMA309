CREATE TABLE `tab` (
  `time` datetime NOT NULL,
  `consume` float NOT NULL,
  `supply` float NOT NULL,
  `power` int(11) NOT NULL,
  `U_L1` float NOT NULL,
  `U_L2` float NOT NULL,
  `U_L3` float NOT NULL,
  `I_L1` float NOT NULL,
  `I_L2` float NOT NULL,
  `I_L3` float NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_unicode_ci;