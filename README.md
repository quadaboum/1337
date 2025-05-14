
# La Voie de l’Éclipse – Déploiement Railway

Ce dépôt contient une application Flask ésotérico-cyberpunk avec :

- Authentification (pseudo, mot de passe, code d’invitation)
- 666 niveaux de progression, prestige et dons
- Interface spéciale pour l’utilisateur `Topaz`
- Redirection automatique de `/` vers `/disclaimer`

## 🚀 Déploiement sur Railway

### 1. Créer un projet Railway

Va sur [https://railway.app](https://railway.app), crée un projet, et connecte ton repo GitHub.

### 2. Variables d’environnement

Ajoute les variables suivantes :

- `DATABASE_URL` : (URL PostgreSQL fournie par Railway)
- `SECRET_KEY` : une chaîne secrète (ex : `1s3cr3t4key!`)
- `FLASK_ENV` : `production`

### 3. Fichiers importants

- `app.py` : Application principale
- `schema.sql` : Base de données (utilise dans PostgreSQL)
- `requirements.txt` : Dépendances (Flask, psycopg2-binary, etc.)
- `Procfile` : Démarrage automatique avec `web: python app.py`

### 4. Initialisation de la base

Depuis Railway > PostgreSQL > **Query**, copie-colle le contenu de `schema.sql` et exécute.

---

## 🧠 Accès spécial

L’utilisateur `Topaz` est le demi-dieu unique, avec accès complet au dashboard.

---

Déployé avec ❤️ par toi, maître de la Voie.
