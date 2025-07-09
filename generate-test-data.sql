-- Insert test users
INSERT INTO users (username, email, password_hash) VALUES
('johnsmith', 'john.smith@example.com', 'hashed_password123'),
('sarahjones', 'sarah.jones@example.com', 'hashed_password456'),
('mikebrown', 'mike.brown@example.com', 'hashed_password789');

-- Insert test business listings
INSERT INTO business_listings (owner_id, business_name, street1, city, state, zip_code, business_type, fulltime_min_age, parttime_min_age, verified) VALUES
(1, 'Happy Burger', '123 Main St', 'Anytown', 'CA', '90210', 'food', 16, 14, true),
(1, 'TechGenius', '456 Tech Ave', 'Silicon Valley', 'CA', '94025', 'tech', 18, 16, true),
(2, 'BookWorms', '789 Library Ln', 'Booktown', 'NY', '10001', 'retail', 16, 14, false),
(3, 'Green Garden', '321 Plant St', 'Greenville', 'FL', '32301', 'gardening', 18, 16, true);

-- Insert listing verifications
INSERT INTO listing_verifications (user_id, listing_id, thumbs_up, comment) VALUES
(2, 1, true, 'Great place to work!'),
(3, 1, true, 'Good management team.'),
(1, 2, true, 'Modern tech company with lots of opportunities.'),
(2, 3, false, 'Not enough teen-friendly positions.'),
(3, 4, true, 'Beautiful work environment.');

-- Insert password reset tokens (with expired and valid tokens)
INSERT INTO password_reset_tokens (user_id, token, expires_at, used) VALUES
(1, 'token123', '2025-07-05 12:00:00', true),
(2, 'token456', '2025-07-06 12:00:00', false),
(3, 'token789', '2025-07-07 12:00:00', false);
