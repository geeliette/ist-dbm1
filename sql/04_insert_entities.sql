INSERT INTO Customer (CustomerID)
SELECT DISTINCT CustomerID
FROM raw_data
WHERE CustomerID IS NOT NULL;

INSERT INTO Category (CategoryName)
SELECT DISTINCT Category
FROM raw_data
WHERE Category IS NOT NULL;

INSERT INTO PaymentMethod (MethodName)
SELECT DISTINCT PaymentMethod
FROM raw_data
WHERE PaymentMethod IS NOT NULL;

INSERT INTO Location (LocationName)
SELECT DISTINCT Location
FROM raw_data
WHERE Location IS NOT NULL;

INSERT INTO Transaction (TransactionID, CustomerID, TransactionDate, PaymentMethodID, LocationID, DiscountApplied)
SELECT
    rd.TransactionID,
    rd.CustomerID,
    rd.TransactionDate ::date,
    pm.PaymentMethodID,
    l.LocationID,
    CASE WHEN rd.DiscountApplied ='True' THEN TRUE
         WHEN rd.DiscountApplied ='False' THEN FALSE
         ELSE NULL
    END
FROM raw_data rd
LEFT JOIN PaymentMethod pm
    ON rd.PaymentMethod = pm.MethodName
LEFT JOIN Location l
    ON rd.Location = l.LocationName; 

INSERT INTO Product (ItemName, CategoryID, DefaultPrice)
SELECT
    rd.Item,
    c.CategoryID,
    rd.PricePerUnit
FROM raw_data rd
JOIN Category c
    ON rd.Category = c.CategoryName
WHERE rd.Item IS NOT NULL;
    
INSERT INTO TransactionLine (TransactionID, ProductID, Quantity, PricePerUnit, TotalSpent)
SELECT
    rd.TransactionID,
    p.ProductID,
    rd.Quantity,
    rd.PricePerUnit,
    rd.TotalSpent
FROM raw_data rd
JOIN Product p
    ON rd.Item = p.ItemName;
