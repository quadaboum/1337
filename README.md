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

### Installation des dépendances :
```
pip install -r requirements.txt
```

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

### v2.5b
- Lecture dynamique de la version via `version.txt`
- Interface `/set_version` pour Topaz
- Badge de version affiché sur toutes les pages HTML
- Menu latéral restreint à l’admin Topaz uniquement
- Option de création de codes d’invitation via interface
