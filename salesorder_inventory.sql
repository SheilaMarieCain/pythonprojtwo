-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema salesorder_inventory_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `salesorder_inventory_schema` ;

-- -----------------------------------------------------
-- Schema salesorder_inventory_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `salesorder_inventory_schema` DEFAULT CHARACTER SET utf8 ;
USE `salesorder_inventory_schema` ;

-- -----------------------------------------------------
-- Table `salesorder_inventory_schema`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `salesorder_inventory_schema`.`users` ;

CREATE TABLE IF NOT EXISTS `salesorder_inventory_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salesorder_inventory_schema`.`items`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `salesorder_inventory_schema`.`items` ;

CREATE TABLE IF NOT EXISTS `salesorder_inventory_schema`.`items` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `description` VARCHAR(255) NULL,
  `unit_price` VARCHAR(45) NULL,
  `selling_price` VARCHAR(45) NULL,
  `reorder_level` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_items_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_items_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `salesorder_inventory_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salesorder_inventory_schema`.`customers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `salesorder_inventory_schema`.`customers` ;

CREATE TABLE IF NOT EXISTS `salesorder_inventory_schema`.`customers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `contact_no` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salesorder_inventory_schema`.`order_hdr`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `salesorder_inventory_schema`.`order_hdr` ;

CREATE TABLE IF NOT EXISTS `salesorder_inventory_schema`.`order_hdr` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `order_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `total_amount` DECIMAL NULL,
  `remarks` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `customer_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_order_hdr_customer1_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_order_hdr_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_order_hdr_customer1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `salesorder_inventory_schema`.`customers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_hdr_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `salesorder_inventory_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salesorder_inventory_schema`.`order_dtl`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `salesorder_inventory_schema`.`order_dtl` ;

CREATE TABLE IF NOT EXISTS `salesorder_inventory_schema`.`order_dtl` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `quantity` INT NULL,
  `unit_price` DECIMAL NULL,
  `amount` DECIMAL NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `order_hdr_id` INT NOT NULL,
  `item_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_order_dtl_order_hdr1_idx` (`order_hdr_id` ASC) VISIBLE,
  INDEX `fk_order_dtl_items1_idx` (`item_id` ASC) VISIBLE,
  CONSTRAINT `fk_order_dtl_order_hdr1`
    FOREIGN KEY (`order_hdr_id`)
    REFERENCES `salesorder_inventory_schema`.`order_hdr` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_dtl_items1`
    FOREIGN KEY (`item_id`)
    REFERENCES `salesorder_inventory_schema`.`items` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salesorder_inventory_schema`.`warehouse_maint`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `salesorder_inventory_schema`.`warehouse_maint` ;

CREATE TABLE IF NOT EXISTS `salesorder_inventory_schema`.`warehouse_maint` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `whs_name` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salesorder_inventory_schema`.`warehouse`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `salesorder_inventory_schema`.`warehouse` ;

CREATE TABLE IF NOT EXISTS `salesorder_inventory_schema`.`warehouse` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `stock_on_hand` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `whs_maintenance_id` INT NOT NULL,
  `item_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_warehouse_warehouse_maint1_idx` (`whs_maintenance_id` ASC) VISIBLE,
  INDEX `fk_warehouse_items1_idx` (`item_id` ASC) VISIBLE,
  CONSTRAINT `fk_warehouse_warehouse_maint1`
    FOREIGN KEY (`whs_maintenance_id`)
    REFERENCES `salesorder_inventory_schema`.`warehouse_maint` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_warehouse_items1`
    FOREIGN KEY (`item_id`)
    REFERENCES `salesorder_inventory_schema`.`items` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salesorder_inventory_schema`.`customer_has_item`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `salesorder_inventory_schema`.`customer_has_item` ;

CREATE TABLE IF NOT EXISTS `salesorder_inventory_schema`.`customer_has_item` (
  `customer_id` INT NOT NULL,
  `item_id` INT NOT NULL,
  PRIMARY KEY (`customer_id`, `item_id`),
  INDEX `fk_customer_has_item_item1_idx` (`item_id` ASC) VISIBLE,
  INDEX `fk_customer_has_item_customer1_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_customer_has_item_customer1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `salesorder_inventory_schema`.`customers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_customer_has_item_item1`
    FOREIGN KEY (`item_id`)
    REFERENCES `salesorder_inventory_schema`.`items` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salesorder_inventory_schema`.`stock_in`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `salesorder_inventory_schema`.`stock_in` ;

CREATE TABLE IF NOT EXISTS `salesorder_inventory_schema`.`stock_in` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `quantity` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `item_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_stock_in_item1_idx` (`item_id` ASC) VISIBLE,
  CONSTRAINT `fk_stock_in_item1`
    FOREIGN KEY (`item_id`)
    REFERENCES `salesorder_inventory_schema`.`items` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salesorder_inventory_schema`.`items_has_order_dtl`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `salesorder_inventory_schema`.`items_has_order_dtl` ;

CREATE TABLE IF NOT EXISTS `salesorder_inventory_schema`.`items_has_order_dtl` (
  `items_id` INT NOT NULL,
  `order_dtl_id` INT NOT NULL,
  PRIMARY KEY (`items_id`, `order_dtl_id`),
  INDEX `fk_items_has_order_dtl_order_dtl1_idx` (`order_dtl_id` ASC) VISIBLE,
  INDEX `fk_items_has_order_dtl_items1_idx` (`items_id` ASC) VISIBLE,
  CONSTRAINT `fk_items_has_order_dtl_items1`
    FOREIGN KEY (`items_id`)
    REFERENCES `salesorder_inventory_schema`.`items` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_items_has_order_dtl_order_dtl1`
    FOREIGN KEY (`order_dtl_id`)
    REFERENCES `salesorder_inventory_schema`.`order_dtl` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salesorder_inventory_schema`.`order_dtl_has_items`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `salesorder_inventory_schema`.`order_dtl_has_items` ;

CREATE TABLE IF NOT EXISTS `salesorder_inventory_schema`.`order_dtl_has_items` (
  `order_dtl_id` INT NOT NULL,
  `item_id` INT NOT NULL,
  PRIMARY KEY (`order_dtl_id`, `item_id`),
  INDEX `fk_order_dtl_has_items_items1_idx` (`item_id` ASC) VISIBLE,
  INDEX `fk_order_dtl_has_items_order_dtl1_idx` (`order_dtl_id` ASC) VISIBLE,
  CONSTRAINT `fk_order_dtl_has_items_order_dtl1`
    FOREIGN KEY (`order_dtl_id`)
    REFERENCES `salesorder_inventory_schema`.`order_dtl` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_dtl_has_items_items1`
    FOREIGN KEY (`item_id`)
    REFERENCES `salesorder_inventory_schema`.`items` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
