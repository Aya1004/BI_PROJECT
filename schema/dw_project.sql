CREATE TABLE `dim_customer` (
  `customer_key` int(11) NOT NULL,
  `customer_id` varchar(50) DEFAULT NULL,
  `customer_zip_code_prefix` varchar(20) DEFAULT NULL,
  `customer_city` varchar(100) DEFAULT NULL,
  `customer_state` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE `dim_product` (
  `product_key` int(11) NOT NULL,
  `product_id` varchar(50) DEFAULT NULL,
  `product_category_name` varchar(100) DEFAULT NULL,
  `product_weight_g` int(11) DEFAULT NULL,
  `product_length_cm` int(11) DEFAULT NULL,
  `product_height_cm` int(11) DEFAULT NULL,
  `product_width_cm` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE `dim_seller` (
  `seller_key` int(11) NOT NULL,
  `seller_id` varchar(50) DEFAULT NULL,
  `seller_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE `dim_time` (
  `date_key` int(11) NOT NULL,
  `full_date` date NOT NULL,
  `day` int(11) DEFAULT NULL,
  `month` int(11) DEFAULT NULL,
  `year` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE `fact_sales` (
  `sales_key` int(11) NOT NULL,
  `customer_key` int(11) DEFAULT NULL,
  `product_key` int(11) DEFAULT NULL,
  `seller_key` int(11) DEFAULT NULL,
  `purchase_date_key` int(11) DEFAULT NULL,
  `order_id` varchar(50) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `shipping_charges` int(11) DEFAULT NULL,
  `sales_amount` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
ALTER TABLE `dim_customer`
  ADD PRIMARY KEY (`customer_key`);

--
-- Index pour la table `dim_product`
--
ALTER TABLE `dim_product`
  ADD PRIMARY KEY (`product_key`),
  ADD UNIQUE KEY `uq_product` (`product_id`);

--
-- Index pour la table `dim_seller`
--
ALTER TABLE `dim_seller`
  ADD PRIMARY KEY (`seller_key`),
  ADD UNIQUE KEY `uq_seller` (`seller_id`);

--
-- Index pour la table `dim_time`
--
ALTER TABLE `dim_time`
  ADD PRIMARY KEY (`date_key`);

--
-- Index pour la table `fact_sales`
--
ALTER TABLE `fact_sales`
  ADD PRIMARY KEY (`sales_key`),
  ADD KEY `fk_fact_customer` (`customer_key`),
  ADD KEY `fk_fact_product` (`product_key`),
  ADD KEY `fk_fact_seller` (`seller_key`),
  ADD KEY `fk_fact_time` (`purchase_date_key`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `dim_customer`
--
ALTER TABLE `dim_customer`
  MODIFY `customer_key` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=119294;

--
-- AUTO_INCREMENT pour la table `dim_product`
--
ALTER TABLE `dim_product`
  MODIFY `product_key` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27452;

--
-- AUTO_INCREMENT pour la table `dim_seller`
--
ALTER TABLE `dim_seller`
  MODIFY `seller_key` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2930;

--
-- AUTO_INCREMENT pour la table `dim_time`
--
ALTER TABLE `dim_time`
  MODIFY `date_key` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3651;

--
-- AUTO_INCREMENT pour la table `fact_sales`
--
ALTER TABLE `fact_sales`
  MODIFY `sales_key` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=95288;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `fact_sales`
--
ALTER TABLE `fact_sales`
  ADD CONSTRAINT `fk_fact_customer` FOREIGN KEY (`customer_key`) REFERENCES `dim_customer` (`customer_key`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_fact_product` FOREIGN KEY (`product_key`) REFERENCES `dim_product` (`product_key`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_fact_seller` FOREIGN KEY (`seller_key`) REFERENCES `dim_seller` (`seller_key`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_fact_time` FOREIGN KEY (`purchase_date_key`) REFERENCES `dim_time` (`date_key`) ON DELETE SET NULL;