# =============================================================================
# FICHIER : app/main.py
# RÔLE    : Point d'entrée de l'API. Définit les routes et la logique métier.
# AUTEUR  : Projet pédagogique - Calculatrice API
# =============================================================================
#
# QU'EST-CE QUE FASTAPI ?
#   FastAPI est un framework Python pour créer des APIs web rapidement.
#   Une API (Application Programming Interface) permet à des programmes
#   de communiquer entre eux via HTTP (comme un navigateur web).
#
# COMMENT TESTER MANUELLEMENT ?
#   Une fois l'app lancée, ouvrez : http://localhost:8000/docs
#   FastAPI génère automatiquement une interface de test visuelle !
# =============================================================================

# --- Imports (bibliothèques dont on a besoin) ---

# FastAPI : le framework principal pour créer notre API
from fastapi import FastAPI, HTTPException

# BaseModel : permet de définir la structure des données attendues (JSON)
from pydantic import BaseModel


# =============================================================================
# CRÉATION DE L'APPLICATION
# =============================================================================

# On crée l'application FastAPI.
# title et description apparaissent dans la doc automatique (/docs)
app = FastAPI(
    title="Calculatrice API",
    description="Une API simple pour apprendre : addition, multiplication, division.",
    version="1.0.0"
)


# =============================================================================
# MODÈLES DE DONNÉES (ce que l'utilisateur doit envoyer)
# =============================================================================

# BaseModel définit la structure JSON attendue dans les requêtes.
# Pydantic valide automatiquement les types (ex: erreur si on envoie du texte).
class OperationInput(BaseModel):
    """
    Modèle de données pour une opération mathématique.
    L'utilisateur doit envoyer un JSON avec deux nombres :
    {
        "a": 10,
        "b": 5
    }
    """
    a: float  # Premier nombre (float = accepte les décimaux comme 3.14)
    b: float  # Deuxième nombre


# =============================================================================
# ROUTES DE L'API
# =============================================================================
# Une "route" = une URL que l'API écoute.
# @app.post("/url") = on attend une requête HTTP de type POST à cette URL.
# POST est utilisé quand on envoie des données au serveur (ici, les nombres).


# -----------------------------------------------------------------------------
# ROUTE 1 : Page d'accueil
# -----------------------------------------------------------------------------
@app.get("/")
def home():
    """
    Route racine - juste pour vérifier que l'API fonctionne.
    GET / → retourne un message de bienvenue.
    """
    return {"message": "Bienvenue sur la Calculatrice API ! Voir /docs pour la documentation."}


# -----------------------------------------------------------------------------
# ROUTE 2 : Addition
# -----------------------------------------------------------------------------
@app.post("/add")
def addition(data: OperationInput):
    """
    Additionne deux nombres.

    Entrée  : { "a": 5, "b": 3 }
    Sortie  : { "operation": "addition", "a": 5, "b": 3, "result": 8 }
    """
    # On effectue le calcul
    result = data.a + data.b

    # On retourne un dictionnaire → FastAPI le convertit automatiquement en JSON
    return {
        "operation": "addition",
        "a": data.a,
        "b": data.b,
        "result": result
    }


# -----------------------------------------------------------------------------
# ROUTE 3 : Multiplication
# -----------------------------------------------------------------------------
@app.post("/multiply")
def multiplication(data: OperationInput):
    """
    Multiplie deux nombres.

    Entrée  : { "a": 4, "b": 7 }
    Sortie  : { "operation": "multiplication", "a": 4, "b": 7, "result": 28 }
    """
    result = data.a * data.b

    return {
        "operation": "multiplication",
        "a": data.a,
        "b": data.b,
        "result": result
    }


# -----------------------------------------------------------------------------
# ROUTE 4 : Division
# -----------------------------------------------------------------------------
@app.post("/divide")
def division(data: OperationInput):
    """
    Divise deux nombres. Gère le cas de la division par zéro.

    Entrée  : { "a": 10, "b": 2 }
    Sortie  : { "operation": "division", "a": 10, "b": 2, "result": 5.0 }

    Cas d'erreur : si b = 0 → retourne une erreur HTTP 400 (Bad Request)
    """
    # Vérification : on ne peut pas diviser par zéro (règle mathématique)
    if data.b == 0:
        # HTTPException envoie une erreur HTTP avec un code et un message
        # 400 = "Bad Request" : l'utilisateur a envoyé des données invalides
        raise HTTPException(
            status_code=400,
            detail="Erreur : Division par zéro impossible."
        )

    # Si b != 0, on effectue la division normalement
    result = data.a / data.b

    return {
        "operation": "division",
        "a": data.a,
        "b": data.b,
        "result": result
    }
