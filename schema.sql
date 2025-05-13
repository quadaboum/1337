
-- Table des utilisateurs avec adresse IP
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nom TEXT NOT NULL,
    pseudo TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    niveau INTEGER DEFAULT 1,
    prestige INTEGER DEFAULT 0,
    argent INTEGER DEFAULT 0,
    ip_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des codes d'invitation
CREATE TABLE invitation_codes (
    id SERIAL PRIMARY KEY,
    code CHAR(16) UNIQUE NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    used_by_user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des missions
CREATE TABLE missions (
    id SERIAL PRIMARY KEY,
    titre TEXT NOT NULL,
    description TEXT,
    prix_prestige INTEGER,
    prix_argent INTEGER
);

-- Table des objets (boutique)
CREATE TABLE objets (
    id SERIAL PRIMARY KEY,
    nom TEXT NOT NULL,
    description TEXT,
    prix INTEGER
);
