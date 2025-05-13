
# 🌑 La Voie de l’Éclipse — v1 (Flask + PostgreSQL)

> Projet fictif et immersif à but artistique — tout est inventé, rien n’est réel.  
> Cette plateforme Flask est prête à déployer sur Railway avec PostgreSQL.

---

## 🔧 Technologies utilisées

- Python 3.x
- Flask
- PostgreSQL (via Railway)
- psycopg2
- HTML / CSS
- Déploiement : Railway + GitHub

---

## 🚀 Installation (local ou Railway)

### 🔹 Déploiement Railway

1. Crée un dépôt GitHub avec ces fichiers
2. Va sur [railway.app](https://railway.app) > **New Project**
3. Sélectionne ton dépôt
4. Ajoute un plugin **PostgreSQL**
5. Dans l’onglet **Variables**, ajoute :

```
DATABASE_URL = (valeur donnée par Railway dans PostgreSQL > Connect)
```

6. Ouvre la console Railway > tape :
```
python init_db.py
```

---

### 🔹 Utilisation locale

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
set DATABASE_URL=postgresql://user:pass@host:port/db
python init_db.py
python app.py
```

---

## 📁 Arborescence

```
.
├── app.py
├── init_db.py
├── schema.sql
├── requirements.txt
├── Procfile
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
```

---

## ❗ Avertissement

Ce projet est un **jeu narratif**. Toute ressemblance avec la réalité est fortuite.
