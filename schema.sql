-- Schéma de base de données pour La Voie de l'Éclipse

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    pseudo TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    niveau INTEGER DEFAULT 1,
    prestige INTEGER DEFAULT 0,
    argent INTEGER DEFAULT 0,
    dons INTEGER DEFAULT 0,
    ip_address TEXT,
    user_agent TEXT
);

CREATE TABLE IF NOT EXISTS invitation_codes (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    used_by_user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
