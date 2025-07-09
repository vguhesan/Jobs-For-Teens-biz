-- Create Users table
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL
);

-- Create Business Listings table
CREATE TABLE business_listing (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES users(id),
    business_name VARCHAR(120) NOT NULL,
    street1 VARCHAR(120) NOT NULL,
    street2 VARCHAR(120),
    city VARCHAR(120) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    phone VARCHAR(20),
    business_type VARCHAR(50) NOT NULL,
    fulltime_min_age INTEGER,
    parttime_min_age INTEGER,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Listing Verifications table
CREATE TABLE listing_verification (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    listing_id INTEGER NOT NULL REFERENCES business_listings(id),
    thumbs_up BOOLEAN NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Password Reset Tokens table
CREATE TABLE password_reset_token (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    token VARCHAR(32) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes for better query performance
CREATE INDEX idx_business_listing_owner ON business_listing(owner_id);
CREATE INDEX idx_business_listing_verified ON business_listing(verified);
CREATE INDEX idx_listing_verification_user ON listing_verification(user_id);
CREATE INDEX idx_listing_verification_listing ON listing_verification(listing_id);
CREATE INDEX idx_password_reset_token_user ON password_reset_token(user_id);
CREATE INDEX idx_password_reset_token_token ON password_reset_token(token);
CREATE INDEX idx_password_reset_token_expires ON password_reset_token(expires_at);
