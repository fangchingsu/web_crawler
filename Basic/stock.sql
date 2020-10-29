# create database
CREATE DATABASE stock CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci ;
# delete database
DROP DATABASE stock;
# create table
CREATE TABLE stock.category (
  main_category VARCHAR(45) NOT NULL,
  sub_category VARCHAR(45),
  third_category VARCHAR(45),
  link VARCHAR(45) NOT NULL);
# delete table
DROP TABLE category;