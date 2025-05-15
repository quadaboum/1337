# 📦 Gestion de la base de données

Ce projet utilise PostgreSQL pour stocker les utilisateurs, les codes d’invitation et les dons.

---

## 🔧 `init_db.py`

Ce script initialise la base avec les tables nécessaires :

- `users`
- `invitation_codes`
- `donations`

### Utilisation :
```bash
python init_db.py
```

⚠️ Il nécessite que les variables d’environnement suivantes soient définies :

- `PGHOST`
- `PGUSER`
- `PGPASSWORD`
- `PGDATABASE`
- `PGPORT` *(optionnel, par défaut : 5432)*

---

## 💣 `reset_db.py`

Ce script supprime proprement toutes les tables créées.

### Utilisation :
```bash
python reset_db.py
```

Utilise-le avec précaution : **toutes les données seront perdues**.

---

🧪 Ces scripts sont utiles pour initialiser ou réinitialiser ta base lors d’un déploiement local ou sur Railway.
