# 🧮 Calculatrice API — Projet Pédagogique

Projet progressif en 3 étapes pour apprendre :
**FastAPI → Docker → Tests → CI/CD**

---

## 📁 Structure du projet

```
calculator-api/
├── app/
│   ├── __init__.py       # Indique que "app" est un package Python
│   └── main.py           # L'API FastAPI (routes + logique)
├── tests/
│   ├── __init__.py       # Indique que "tests" est un package Python
│   └── test_api.py       # Tests automatiques pytest
├── .github/
│   └── workflows/
│       └── ci.yml        # Pipeline CI GitHub Actions
├── Dockerfile            # Recette pour construire l'image Docker
├── docker-compose.yml    # Orchestration des conteneurs
├── requirements.txt      # Dépendances Python
└── README.md             # Ce fichier
```

---

## 🌿 Branches Git par étape

| Branche         | Contenu                          |
|-----------------|----------------------------------|
| `etape-1-api`   | API + Dockerfile + docker-compose |
| `etape-2-tests` | Étape 1 + tests pytest            |
| `etape-3-ci`    | Étape 2 + GitHub Actions CI       |

```bash
# Voir une étape spécifique
git checkout etape-1-api

# Voir les différences entre deux étapes
git diff etape-1-api etape-2-tests
```

---

## 🚀 Étape 1 — Lancer l'API

### Option A : Directement avec Python

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
uvicorn app.main:app --reload --port 8000
```

### Option B : Avec Docker Compose (recommandé)

```bash
# Construire et lancer le conteneur
docker compose up --build

# Lancer en arrière-plan
docker compose up --build -d

# Arrêter
docker compose down
```

### Tester l'API manuellement

Ouvrir dans le navigateur : **http://localhost:8000/docs**

FastAPI génère automatiquement une interface de test visuelle (Swagger UI) !

---

## 🧪 Étape 2 — Lancer les tests

```bash
# Lancer tous les tests
pytest tests/

# Mode verbose (voir chaque test)
pytest tests/ -v

# Avec résumé des erreurs
pytest tests/ -v --tb=short
```

**Résultat attendu :**
```
tests/test_api.py::test_home PASSED
tests/test_api.py::test_addition_nombres_positifs PASSED
tests/test_api.py::test_division_par_zero PASSED
...
15 passed in 0.5s
```

---

## ⚙️ Étape 3 — CI GitHub Actions

La pipeline se déclenche automatiquement à chaque `git push`.

**Voir les résultats :** GitHub → repo → onglet **Actions**

---

## 📡 Routes de l'API

| Méthode | Route       | Exemple d'entrée          | Résultat  |
|---------|-------------|---------------------------|-----------|
| GET     | `/`         | —                         | Message de bienvenue |
| POST    | `/add`      | `{"a": 5, "b": 3}`        | `8`       |
| POST    | `/multiply` | `{"a": 4, "b": 7}`        | `28`      |
| POST    | `/divide`   | `{"a": 10, "b": 2}`       | `5.0`     |
| POST    | `/divide`   | `{"a": 10, "b": 0}`       | ❌ Erreur 400 |
