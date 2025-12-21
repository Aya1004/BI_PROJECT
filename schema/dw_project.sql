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
--
ALTER TABLE `dim_customer`
  ADD PRIMARY KEY (`customer_key`);

--
-- Index pour la table `dim_order`
--
ALTER TABLE `dim_order`
  ADD PRIMARY KEY (`order_key`);

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
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `dim_customer`
--
ALTER TABLE `dim_customer`
  MODIFY `customer_key` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38280;

--
-- AUTO_INCREMENT pour la table `dim_order`
--
ALTER TABLE `dim_order`
  MODIFY `order_key` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89317;

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
COMMIT;