-- Test database initialization script
-- This script sets up the test database schema for integration tests

-- Create test tables
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255),
    date_of_birth DATE,
    address JSONB,
    preferences JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(100),
    sku VARCHAR(100) UNIQUE NOT NULL,
    in_stock BOOLEAN DEFAULT TRUE,
    quantity INTEGER DEFAULT 0,
    attributes JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(100) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    products JSONB NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    shipping_address JSONB,
    billing_address JSONB,
    payment_method VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);

-- Insert sample test data
INSERT INTO users (first_name, last_name, email, phone, username, address) VALUES
('John', 'Doe', 'john.doe@example.com', '+1234567890', 'johndoe', '{"street": "123 Main St", "city": "Anytown", "state": "CA", "zip": "12345"}'),
('Jane', 'Smith', 'jane.smith@example.com', '+1234567891', 'janesmith', '{"street": "456 Oak Ave", "city": "Somewhere", "state": "NY", "zip": "67890"}'),
('Bob', 'Johnson', 'bob.johnson@example.com', '+1234567892', 'bobjohnson', '{"street": "789 Pine Rd", "city": "Elsewhere", "state": "TX", "zip": "54321"}')
ON CONFLICT (email) DO NOTHING;

INSERT INTO products (name, description, price, category, sku, in_stock, quantity) VALUES
('Test Product 1', 'A test product for integration testing', 29.99, 'Electronics', 'TEST-001', TRUE, 100),
('Test Product 2', 'Another test product for integration testing', 49.99, 'Clothing', 'TEST-002', TRUE, 50),
('Test Product 3', 'Yet another test product for integration testing', 19.99, 'Books', 'TEST-003', FALSE, 0),
('Test Product 4', 'Premium test product for integration testing', 99.99, 'Electronics', 'TEST-004', TRUE, 25),
('Test Product 5', 'Budget test product for integration testing', 9.99, 'Accessories', 'TEST-005', TRUE, 200)
ON CONFLICT (sku) DO NOTHING;

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
