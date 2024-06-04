-- Dummy Data for Database
-- To insert type in CLI: "cat dummy_data.sql | sqlite3 data.db" "type dummy_data.sql | sqlite3 data.db" 

INSERT INTO USERS (key, user_type) VALUES ('a098fhAm', 'VIP');
INSERT INTO USERS (key, user_type) VALUES ('12TTawqm', 'Manager');
INSERT INTO USERS (key, user_type) VALUES ('a098fhAP', 'Staff');

INSERT INTO TABLES (table_number, occupied) VALUES (1, False);
INSERT INTO TABLES (table_number, occupied) VALUES (2, False);
INSERT INTO TABLES (table_number, occupied) VALUES (3, False);
INSERT INTO TABLES (table_number, occupied) VALUES (4, False);
INSERT INTO TABLES (table_number, occupied) VALUES (5, False);
INSERT INTO TABLES (table_number, occupied) VALUES (6, False);
INSERT INTO TABLES (table_number, occupied) VALUES (7, False);
INSERT INTO TABLES (table_number, occupied) VALUES (8, False);

INSERT INTO MENUITEMS (name, category, price, vip_price, description, image) VALUES ('Fish and Chips', 'Main', 13, 10, "Battered fish and hot chips.", 0);
INSERT INTO MENUITEMS (name, category, price, vip_price, description, image) VALUES ('Spaghetti', 'Main', 20, 15, "Spaghetti topped with bolognese sauce and parmesan cheese.", 1);
INSERT INTO MENUITEMS (name, category, price, vip_price, description, image) VALUES ('Steak and Potatoes', 'Main', 40, 30, "Grilled fillet steak with gravy and roasted potatoes.", 2);
INSERT INTO MENUITEMS (name, category, price, vip_price, description, image) VALUES ('Edamame', 'Entree', 8, 6, "Salted and boiled edamame (soybeans).", 3);
INSERT INTO MENUITEMS (name, category, price, vip_price, description, image) VALUES ('Takoyaki', 'Entree', 12, 9, "6 balls of octopus and batter fried and topped with mayonnaise.", 4);
INSERT INTO MENUITEMS (name, category, price, vip_price, description, image) VALUES ('Sashimi', 'Entree', 15, 11, "8 pieces of fresh salmon sashimi.", 5);
INSERT INTO MENUITEMS (name, category, price, vip_price, description, image) VALUES ('Vanilla Ice Cream', 'Dessert', 5, 3, "", 6);
INSERT INTO MENUITEMS (name, category, price, vip_price, description, image) VALUES ('Raspberry Ice Cream', 'Dessert', 6, 4, "", 7);
INSERT INTO MENUITEMS (name, category, price, vip_price, description, image) VALUES ('Chocolate Ice Cream', 'Dessert', 7, 5, "", 8);
INSERT INTO MENUITEMS (name, category, price, vip_price, description, image) VALUES ('Coke', 'Drink', 8, 6, "A Coca-Cola can.", 9);
INSERT INTO MENUITEMS (name, category, price, vip_price, description, image) VALUES ('Banana Milkshake', 'Drink', 12, 9, "Milkshake made with bananas and vanilla ice cream.", 10);
INSERT INTO MENUITEMS (name, category, price, vip_price, description, image) VALUES ('Sparkling Water', 'Drink', 5, 3, "A bottle of sparkling water.", 11);

INSERT INTO CATEGORIES (category_name) VALUES ('Main');
INSERT INTO CATEGORIES (category_name) VALUES ('Entree');
INSERT INTO CATEGORIES (category_name) VALUES ('Drink');
INSERT INTO CATEGORIES (category_name) VALUES ('Dessert');

-- INSERT INTO Feedbacks (customer_name, feedback_rating, feedback_comment) VALUES ('Jack', 5, "good food");
-- INSERT INTO Feedbacks (customer_name, feedback_rating, feedback_comment) VALUES ('Frank', 3, "great food");
-- INSERT INTO Feedbacks (customer_name, feedback_rating, feedback_comment) VALUES ('Bob', 3, "excellant food");
-- INSERT INTO Feedbacks (customer_name, feedback_rating, feedback_comment) VALUES ('Frog', 2, "bad food");
