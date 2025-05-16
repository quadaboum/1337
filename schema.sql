-- Schéma SQL pour Voie de l'Éclipse

CREATE TABLE IF NOT EXISTS user (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    pseudo TEXT UNIQUE,
    password TEXT,
    niveau INTEGER DEFAULT 1,
    prestige INTEGER DEFAULT 0,
    argent INTEGER DEFAULT 0,
    dons INTEGER DEFAULT 0,
    ip_address TEXT,
    user_agent TEXT,
    used_invitation_code TEXT,
    token VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS invitation_codes (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE,
    used BOOLEAN DEFAULT FALSE,
    used_by_user_id INTEGER REFERENCES user(id),
    token VARCHAR(64)
);