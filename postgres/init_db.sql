-- Create and configure user
CREATE USER bear_vision_user WITH PASSWORD 'bear_vision_user_password';
GRANT ALL ON SCHEMA public TO bear_vision_user;
ALTER ROLE bear_vision_user SET client_encoding TO 'utf8';
ALTER ROLE bear_vision_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE bear_vision_user SET timezone TO 'UTC';

-- Create database
CREATE DATABASE bear_vision;

-- Grant database privileges to user
GRANT ALL PRIVILEGES ON DATABASE bear_vision TO bear_vision_user;

-- Figure out why the privileges on schema public don't solve the issue?
-- remove superuser privileges to see problem.
ALTER USER bear_vision_user WITH SUPERUSER;
