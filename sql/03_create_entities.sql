-- Customer table
CREATE TABLE Customer (
    CustomerID TEXT PRIMARY KEY
);

-- Category table
CREATE TABLE Category (
    CategoryID SERIAL PRIMARY KEY,
    CategoryName VARCHAR(100) UNIQUE
);

-- Product table
CREATE TABLE Product (
    ProductID SERIAL PRIMARY KEY,
    ItemName VARCHAR(255),
    CategoryID INT REFERENCES Category(CategoryID),
    DefaultPrice NUMERIC
);

-- Payment Method table
CREATE TABLE PaymentMethod (
    PaymentMethodID SERIAL PRIMARY KEY,
    MethodName VARCHAR(50) UNIQUE
);

-- Location table
CREATE TABLE Location (
    LocationID SERIAL PRIMARY KEY,
    LocationName VARCHAR(50) UNIQUE
);

-- Transaction table
CREATE TABLE Transaction (
    TransactionID VARCHAR(50) PRIMARY KEY,
    CustomerID TEXT REFERENCES Customer(CustomerID),
    TransactionDate DATE NOT NULL,
    PaymentMethodID INT REFERENCES PaymentMethod(PaymentMethodID),
    LocationID INT REFERENCES Location(LocationID),
    DiscountApplied BOOLEAN
);

-- TransactionLine table
CREATE TABLE TransactionLine (
    TransactionID VARCHAR(50) REFERENCES Transaction(TransactionID),
    ProductID INT REFERENCES Product(ProductID),
    Quantity INT,
    PricePerUnit NUMERIC,
    TotalSpent NUMERIC,
    PRIMARY KEY (TransactionID, ProductID)
);
