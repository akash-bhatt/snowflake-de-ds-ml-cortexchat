CREATE OR REPLACE TRANSIENT TABLE GROCERY_DEMAND_DATA_STG (
    date DATE,
    product_id VARCHAR(100),
    product_category VARCHAR(50),
    is_perishable BOOLEAN,
    shelf_life NUMBER(5,0),
    temperature FLOAT,
    is_rainy BOOLEAN,
    is_weekend BOOLEAN,
    is_promotional BOOLEAN,
    discount_pct FLOAT,
    price DECIMAL(10,2),
    demand NUMBER(8,0),
    stock_level NUMBER(8,0),
    actual_sales NUMBER(8,0),
    waste NUMBER(8,0)
);