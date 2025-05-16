-- Supprime la table user si elle existe déjà (et tout ce qui dépend d'elle)
DROP TABLE IF EXISTS "user" CASCADE;

-- Recrée la table user avec toutes les colonnes nécessaires (clé primaire id)
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    pseudo VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    level INT DEFAULT 1,
    prestige INT DEFAULT 0,
    last_ip VARCHAR(100),
    user_agent VARCHAR(300),
    created_at TIMESTAMP DEFAULT NOW(),
    is_admin BOOLEAN DEFAULT FALSE,
    money INT DEFAULT 0,
    invite_code VARCHAR(16) UNIQUE,
    donations INT DEFAULT 0,
    token VARCHAR(64)
);