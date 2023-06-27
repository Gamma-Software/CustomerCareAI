-- Création de la table des customers (clients)
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  phone VARCHAR(20),
  address VARCHAR(200)
);

-- Création de la table des orders (commandes)
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INTEGER REFERENCES customers(id),
  order_date DATE NOT NULL,
  total_amount DECIMAL(10,2) NOT NULL
);

-- Création de la table des pizzas
CREATE TABLE pizzas (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL,
  ingredients TEXT,
  intolerances TEXT,
  suitable TEXT
);

-- Création de la table de liaison pour les pizzas d'une commande
CREATE TABLE order_pizzas (
  order_id INTEGER REFERENCES orders(id),
  pizza_id INTEGER REFERENCES pizzas(id),
  quantity INTEGER NOT NULL,
  PRIMARY KEY (order_id, pizza_id)
);

-- Insert data into the customers table
INSERT INTO customers (name, phone, address)
VALUES
    ('John Doe', '1234567890', '123 Main St'),
    ('Jane Smith', '9876543210', '456 Elm St'),
    ('Michael Johnson', '5555555555', '789 Oak Ave');

-- Insert data into the pizzas table
INSERT INTO pizzas (name, description, price, ingredients, suitable)
VALUES
    ('Margherita', 'Classic tomato and mozzarella pizza', 9.99, 'Tomato, Mozzarella, Basil', 'Vegetarian'),
    ('Pepperoni', 'Traditional pizza topped with pepperoni slices', 11.99, 'Tomato, Mozzarella, Pepperoni', ''),
    ('Vegetarian', 'Loaded with various vegetables', 10.99, 'Tomato, Mozzarella, Bell peppers, Mushrooms, Onions, Olives', 'Vegetarian'),
    ('Hawaiian', 'Sweet and savory combination of ham and pineapple', 12.99, 'Tomato, Mozzarella, Ham, Pineapple', ''),
    ('Mushroom', 'Rich and earthy pizza topped with mushrooms', 10.99, 'Tomato, Mozzarella, Mushrooms', 'Vegetarian'),
    ('Veggie Supreme', 'A medley of fresh vegetables for veggie lovers', 12.99, 'Tomato, Mozzarella, Bell peppers, Mushrooms, Onions, Olives, Corn', 'Vegetarian'),
    ('BBQ Chicken', 'Tangy BBQ sauce with grilled chicken', 13.99, 'BBQ Sauce, Mozzarella, Chicken, Red onions, Cilantro', ''),
    ('Spinach and Feta', 'Delicious combination of spinach and feta cheese', 11.99, 'Tomato, Mozzarella, Spinach, Feta cheese', 'Vegetarian'),
    ('Gluten-Free Veggie', 'Gluten-free crust topped with fresh vegetables', 12.99, 'Tomato, Mozzarella, Bell peppers, Mushrooms, Onions, Olives', 'Gluten-Free, Vegetarian'),
    ('Vegan Supreme', 'Plant-based pizza loaded with vegan toppings', 13.99, 'Tomato, Vegan cheese, Bell peppers, Mushrooms, Onions, Olives', 'Vegan');

-- Insert data into the orders table
INSERT INTO orders (customer_id, order_date, total_amount)
VALUES
    (1, '2023-06-25', 29.98),
    (2, '2023-06-24', 23.99),
    (3, '2023-06-23', 33.98);

-- Insert data into the order_pizzas table
INSERT INTO order_pizzas (order_id, pizza_id, quantity)
VALUES
    (1, 1, 2),
    (1, 3, 1),
    (2, 2, 2),
    (3, 1, 1),
    (3, 4, 1);
