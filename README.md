Version : v2.5b

# Voie de l'Éclipse

Site fictif ésotérique cyberpunk avec :
- 666 niveaux (dont 665 accessibles)
- Dashboard admin Topaz
- Missions, boutique, dons, offrandes, statistiques
- Protection par session utilisateur
- Interface responsive compatible PC, iPhone, Android
- Design sombre avec effets glitchs

## Démarrage

### Installation

### ✅ En local (VPS, Linux, macOS, WSL...)

1. **Cloner le dépôt :**
   ```bash
   git clone <ton_repo_git>
   cd ton_repo_git
   ```

2. **Créer un environnement virtuel et l’activer :**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l’application Flask :**
   ```bash
   python app.py
   ```
   Accède à l’application sur [http://localhost:5000](http://localhost:5000)

---

### ☁️ Sur Railway

1. **Créer un nouveau projet Railway :** [https://railway.app](https://railway.app)

2. **Déployer un projet depuis GitHub.**

3. **Configurer les variables d’environnement :**
   - `FLASK_ENV=production`
   - (Autres variables personnalisées selon besoin)

4. **Railway détectera automatiquement :**
   - `requirements.txt` (Python)
   - `Procfile` avec :  
     ```
     web: python app.py
     ```

5. **Connexion PostgreSQL** *(si utilisé)* :
   - Ajoute Railway PostgreSQL à ton projet
   - Récupère les variables `PGHOST`, `PGUSER`, `PGPASSWORD`, etc.
   - Configure la chaîne de connexion dans `app.py`

---

🎉 Tu peux maintenant accéder à ton site déployé depuis Railway, ou en local sur ton VPS.
### Initialiser la base (optionnel si déjà existante) :
```
python init_db.py
```

### Lancer le serveur :
```
python app.py
```

## Déploiement (ex. Railway, Heroku)

Ajoutez vos variables d’environnement :
- `PGHOST`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGPORT`
- `SECRET_KEY`

## Accès
- `/` → page d’accueil
- `/login` / `/register` → avec code d’invitation
- `/menu` → menu général
- `/dashboard` → réservé à Topaz


## Changelog
### v3.0
- Refactor complet du code
- Décorateur admin mutualisé
- Injection version/footer/warning centralisée
- Templates unifiés et sécurisés
- README, scripts, et logique PostgreSQL propres


### v2.5b
- Lecture dynamique de la version via `version.txt`
- Interface `/set_version` pour Topaz
- Badge de version affiché sur toutes les pages HTML
- Menu latéral restreint à l’admin Topaz uniquement
- Option de création de codes d’invitation via interface


## Version 3.1b
- Sécurisation complète de l'accès admin
- Ajout d'une page unauthorized.html
- Redirection propre vers login si non connecté
- Nettoyage et commentaires dans app.py
- CSS global appliqué


## Version v3.1c
- Suppression du footer redondant dans disclaimer
- Footer dynamique avec version dans toutes les pages
- Ajout des liens : 'Revenir au menu principal' et 'Bafouer son honneur'
- dashboard.html réparé et fonctionnel
- Uniformisation du style CSS sauf menu latéral


## Version v3.1d
- Uniformisation du footer sur toutes les pages
- Ajout automatique de la version depuis version.txt dans le pied de page
- Liens cohérents selon les pages (publique : "Bafouer son honneur", privée : "Revenir au menu principal")


## Version v3.1d
- Footer uniformisé dans toutes les pages (publiques et privées)
- Ajout automatique du lien vers le menu ou vers le disclaimer
- Footer affichant version.txt et année 2025 à chaque fois
