CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    level INTEGER DEFAULT 1,
    prestige INTEGER DEFAULT 0,
    last_ip VARCHAR(100),
    user_agent VARCHAR(300),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_admin BOOLEAN DEFAULT FALSE,
    money INTEGER DEFAULT 0,
    invite_code VARCHAR(16) UNIQUE,
    donations INTEGER DEFAULT 0
);

CREATE TABLE invite_code (
    id SERIAL PRIMARY KEY,
    code VARCHAR(16) UNIQUE NOT NULL,
    created_by INTEGER REFERENCES "user"(id)
);
