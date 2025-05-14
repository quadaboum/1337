
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
