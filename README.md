# Projet Topaz – v3.0_a

**La Voie de l'Éclipse** – Un site Flask ritualiste, interactif et progressif, entièrement compatible Railway.

## Fonctionnalités principales

- Authentification avec pseudonyme et invitation
- Tableau de bord unique pour l'utilisateur `Topaz`
- Système de progression avec missions, boutique, dons et offrandes
- Sécurité renforcée : redirection automatique si non connecté
- Interface stylisée à partir de `disclaimer.html` pour toutes les pages
- Accès restreint au panel admin avec une page `unauthorized.html` dédiée

## Variables d’environnement requises

```
PGHOST=
PGDATABASE=
PGUSER=
PGPASSWORD=
PGPORT=5432
SECRET_KEY=topaz_secret_key
PORT=5000
```

## Déploiement sur Railway

1. Uploadez tous les fichiers de cette archive
2. Configurez les variables d’environnement ci-dessus
3. Initialisez la base PostgreSQL avec `schema.sql`

## Changements récents
## Modifications préparatoires à la version 3.2c
- Ajout d’une page `unauthorized.html` pour empêcher l'accès au dashboard si non-Topaz.
- Sécurisation de la route `/dashboard`.
- Préparation au nettoyage final et sécurité générale.