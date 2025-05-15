# Topaz – Voie de l'Éclipse v3.3

Projet artistique/expérimental de site sectaire fictif basé sur Flask + PostgreSQL, dark mode complet, ultra sécurisé et avec sidebar dynamique.
Compatible Railway, Docker, ou local (SQLite possible mais non recommandé).

---

## 🚀 Déploiement Railway (PostgreSQL only)

1. Clone ou télécharge le projet
2. Configure Railway :
   - Ajoute une variable d'environnement `DATABASE_URL` (PostgreSQL fourni par Railway)
   - Ajoute une variable d'environnement `SECRET_KEY` (random ou laisse vide pour auto-génération)
3. Déploie
   - Railway détecte le `Procfile` → `web: gunicorn app:app`
   - Les dépendances sont dans `requirements.txt`
   - Initialise la base avec le contenu de `schema.sql` (à exécuter une seule fois)
4. Premier accès :
   - Va sur `/register` pour créer un user avec un code d'invitation généré dans le dashboard admin.
   - Le user "Topaz" est l’admin principal (mot de passe à changer !).

---

## 🗃️ Structure du projet

    app.py
    /templates/
        login.html
        register.html
        menu.html
        missions.html
        boutique.html
        don.html
        offrandes.html
        statistique.html
        dashboard.html
        404.html
        500.html
        unauthorized.html
        disclaimer.html
        sidebar.html
    /static/
        style.css
    requirements.txt
    Procfile
    schema.sql
    README.md

---

## 👾 Easter eggs inclus

- Konami code (↑↑↓↓←→←→BA) sur le menu : pop-up “Topaz t’observe 👁️”, effet glitch.
- Double clic sur le titre : “Le vrai gourou, c’est toi, iGz.” apparaît.
- 404/500 : Clique 5x sur “Ne risque pas la punition divine” → secret débloqué.
- CSS : Un message caché dans `style.css`.
- Admin sidebar : Garde la souris sur "Dashboard" → citation mystique de Topaz.
- Mode Ultra-Dark : Tape “666” sur la page menu → mode secret activé.

*Modifie ou désactive les easter eggs dans les templates ou le JS selon tes envies.*

---

## 🛡️ Sécurité et sessions

- Pages protégées : accès uniquement si connecté (sauf `/`, `/disclaimer`, `/login`, `/register`).
- Dashboard : réservé à l'admin (user `is_admin = True`)
- Déconnexion : bouton accessible partout via la sidebar.
- Protection Topaz : Impossible de supprimer ou downgrader le compte admin principal.

---

## 📦 Commandes utiles (pour développement local)

Lancer en local (SQLite) :

    pip install -r requirements.txt
    export FLASK_APP=app.py
    flask run

Initialiser la base (si besoin) :

    sqlite3 db.sqlite3 < schema.sql

---

## ✨ Modifications & personnalisation

- Tu peux modifier tous les easter eggs dans les fichiers HTML/JS.
- Sidebar, missions, boutique, progression, tout est personnalisable depuis la base ou les templates.
- Ajoute tes propres rituels, objets, paliers et animations dans les fichiers correspondants.

---

Projet fictif, à ne pas prendre au sérieux. Toute ressemblance avec la réalité serait purement fortuite.

---

iGz / Topaz 2025
