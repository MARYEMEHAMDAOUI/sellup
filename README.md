# Sellup — Gestion Commerciale (Python / Streamlit)

Application de gestion commerciale entièrement en Python avec Streamlit.

---

## 🚀 Démarrage en 3 commandes

### 1. Installer Python
Télécharger Python 3.10+ → https://www.python.org/downloads/
(cocher "Add to PATH" lors de l'installation)

### 2. Installer les dépendances
Ouvrir un terminal dans le dossier `sellup_py` puis :
```bash
pip install -r requirements.txt
```

### 3. Lancer l'application
```bash
streamlit run app.py
```
L'application s'ouvre automatiquement sur http://localhost:8501

---

## 🔐 Comptes de démonstration

| Identifiant | Mot de passe | Rôle           |
|-------------|-------------|----------------|
| admin       | admin123    | Administrateur |
| vendeur1    | pass123     | Vendeur        |
| manager     | mgr123      | Manager        |

---

## 📁 Structure du projet

```
sellup_py/
├── app.py                  ← Application principale (login + navigation)
├── data.py                 ← Données initiales (utilisateurs, produits, clients, ventes)
├── requirements.txt        ← Dépendances Python
├── modules/
│   ├── __init__.py
│   ├── pg_dashboard.py     ← Tableau de bord
│   ├── pg_new_sale.py      ← Nouvelle vente (3 étapes)
│   ├── pg_sales.py         ← Historique des ventes
│   ├── pg_livraisons.py    ← Suivi des livraisons
│   ├── pg_clients.py       ← Gestion clients
│   ├── pg_products.py      ← Catalogue et stocks
│   ├── pg_reports.py       ← Rapports & analyses
│   ├── pg_users.py         ← Gestion utilisateurs (admin)
│   └── pg_profile.py       ← Mon profil
└── README.md
```

---

## 💡 Conseils VSCode

Installer l'extension **Python** (Microsoft) pour :
- Coloration syntaxique
- Autocomplétion
- Débogage intégré

Raccourci terminal : `Ctrl + \``

---

## ⚠️ Note sur les données

Les données sont stockées en mémoire (session Streamlit).
Elles se réinitialisent à chaque redémarrage de l'application.
Pour persister les données, connectez une base SQLite ou PostgreSQL.
