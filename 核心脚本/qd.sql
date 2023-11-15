/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50726
Source Host           : localhost:3306
Source Database       : qd

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2023-09-19 16:19:06
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `uname` varchar(255) NOT NULL,
  `upwd` varchar(255) NOT NULL,
  `wz` varchar(255) DEFAULT NULL,
  `zb` varchar(255) DEFAULT NULL,
  `types` smallint(1) NOT NULL,
  `remaining_days` smallint(3) unsigned zerofill DEFAULT '000',
  PRIMARY KEY (`uname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------

