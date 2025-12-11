BEGIN;

-- Insert customer only if not exists
INSERT INTO Customer(customer_id)
VALUES ('C123')
ON CONFLICT DO NOTHING;

-- Insert transaction
INSERT INTO Transaction(transaction_id, customer_id, transaction_date)
VALUES ('T987', 'C123', '2024-01-01');
ON CONFLICT (transaction_id) DO NOTHING;

-- Insert item
INSERT INTO Item(item_name, category_id, price_per_unit)
VALUES ('Apple', 1, 5.00)
ON CONFLICT (item_name) DO NOTHING;

-- Insert into bridge table
INSERT INTO Transaction_Item(transaction_id, item_id, quantity, total_spent)
VALUES ('T987', 5, 3, 15.00);

COMMIT;
