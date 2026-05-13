# =============================================================================
# FICHIER : tests/test_api.py
# RÔLE    : Tests automatiques de l'API avec Pytest.
# ÉTAPE   : 2 - Tests automatiques
#
# QU'EST-CE QUE PYTEST ?
#   Pytest est un framework Python pour écrire et exécuter des tests.
#   Un "test" vérifie automatiquement qu'une fonction retourne le bon résultat.
#   → Si on casse quelque chose, les tests le détectent immédiatement !
#
# POURQUOI TESTER ?
#   - Éviter les régressions (une modification qui casse ce qui marchait)
#   - Documenter le comportement attendu de l'API
#   - Déployer avec confiance
#
# COMMANDE POUR LANCER LES TESTS :
#   pytest tests/                    ← lance tous les tests
#   pytest tests/ -v                 ← mode verbose (affiche chaque test)
#   pytest tests/ -v --tb=short      ← affiche un résumé des erreurs
#
# CONVENTION DE NOMMAGE :
#   - Fichier de test  : doit commencer par "test_" (ex: test_api.py)
#   - Fonction de test : doit commencer par "test_" (ex: def test_addition)
#   → Pytest découvre automatiquement les tests grâce à cette convention !
# =============================================================================

# --- Imports ---

# pytest : framework de test
import pytest

# TestClient : client HTTP fourni par FastAPI pour tester l'API sans serveur réel
# Il simule des requêtes HTTP directement en mémoire → rapide et sans port !
from fastapi.testclient import TestClient

# On importe notre application FastAPI pour la tester
from app.main import app


# =============================================================================
# CONFIGURATION DU CLIENT DE TEST
# =============================================================================

# On crée un client de test lié à notre application.
# TestClient permet d'envoyer des requêtes HTTP (GET, POST...) à l'app
# sans avoir besoin de lancer un vrai serveur uvicorn.
client = TestClient(app)


# =============================================================================
# TESTS : PAGE D'ACCUEIL
# =============================================================================

def test_home():
    """
    Vérifie que la route d'accueil (GET /) répond correctement.
    C'est le test le plus simple : juste vérifier que l'API est vivante.
    """
    # On envoie une requête GET à "/"
    response = client.get("/")

    # assert = affirmer que quelque chose est vrai
    # Si l'assertion est fausse → le test échoue avec un message d'erreur

    # Vérifier que le code HTTP est 200 (= succès)
    assert response.status_code == 200

    # Vérifier que la réponse contient bien le mot "Bienvenue"
    assert "Bienvenue" in response.json()["message"]


# =============================================================================
# TESTS : ADDITION
# =============================================================================

def test_addition_nombres_positifs():
    """
    Test classique : additionner deux nombres positifs.
    5 + 3 doit retourner 8.
    """
    # On envoie une requête POST avec un corps JSON {"a": 5, "b": 3}
    response = client.post("/add", json={"a": 5, "b": 3})

    # Le code HTTP doit être 200 (succès)
    assert response.status_code == 200

    # On récupère le JSON de la réponse sous forme de dictionnaire Python
    data = response.json()

    # Vérifier que le résultat est bien 8
    assert data["result"] == 8

    # Vérifier que le nom de l'opération est correct
    assert data["operation"] == "addition"


def test_addition_avec_zero():
    """
    Cas limite : additionner avec zéro.
    0 + 7 doit retourner 7.
    """
    response = client.post("/add", json={"a": 0, "b": 7})
    assert response.status_code == 200
    assert response.json()["result"] == 7


def test_addition_nombres_negatifs():
    """
    Cas limite : additionner des nombres négatifs.
    -4 + (-6) doit retourner -10.
    """
    response = client.post("/add", json={"a": -4, "b": -6})
    assert response.status_code == 200
    assert response.json()["result"] == -10


def test_addition_decimaux():
    """
    Cas limite : additionner des nombres décimaux.
    1.5 + 2.5 doit retourner 4.0.
    """
    response = client.post("/add", json={"a": 1.5, "b": 2.5})
    assert response.status_code == 200
    assert response.json()["result"] == 4.0


# =============================================================================
# TESTS : MULTIPLICATION
# =============================================================================

def test_multiplication_classique():
    """
    Test classique : multiplier deux nombres.
    4 × 7 doit retourner 28.
    """
    response = client.post("/multiply", json={"a": 4, "b": 7})
    assert response.status_code == 200

    data = response.json()
    assert data["result"] == 28
    assert data["operation"] == "multiplication"


def test_multiplication_par_zero():
    """
    Cas limite : multiplier par zéro.
    Tout nombre × 0 = 0 (règle mathématique).
    """
    response = client.post("/multiply", json={"a": 999, "b": 0})
    assert response.status_code == 200
    assert response.json()["result"] == 0


def test_multiplication_nombres_negatifs():
    """
    Cas limite : multiplier un positif par un négatif.
    -3 × 5 doit retourner -15.
    """
    response = client.post("/multiply", json={"a": -3, "b": 5})
    assert response.status_code == 200
    assert response.json()["result"] == -15


# =============================================================================
# TESTS : DIVISION
# =============================================================================

def test_division_classique():
    """
    Test classique : diviser deux nombres.
    10 ÷ 2 doit retourner 5.0.
    """
    response = client.post("/divide", json={"a": 10, "b": 2})
    assert response.status_code == 200

    data = response.json()
    assert data["result"] == 5.0
    assert data["operation"] == "division"


def test_division_resultat_decimal():
    """
    Cas limite : division qui donne un résultat décimal.
    7 ÷ 2 doit retourner 3.5.
    """
    response = client.post("/divide", json={"a": 7, "b": 2})
    assert response.status_code == 200
    assert response.json()["result"] == 3.5


def test_division_par_zero():
    """
    CAS D'ERREUR CRITIQUE : division par zéro.
    L'API doit retourner une erreur HTTP 400 (Bad Request)
    et un message d'erreur explicite.

    C'est le test le plus important pour la division !
    On vérifie que l'API gère l'erreur proprement (pas un crash).
    """
    response = client.post("/divide", json={"a": 10, "b": 0})

    # On attend un code 400 (erreur côté client = données invalides)
    # et NON un 500 (erreur serveur = crash de l'app)
    assert response.status_code == 400

    # Vérifier que le message d'erreur parle bien de "zéro"
    assert "zéro" in response.json()["detail"].lower() or "zero" in response.json()["detail"].lower()


# =============================================================================
# TESTS : DONNÉES INVALIDES
# =============================================================================

def test_donnees_invalides_manquantes():
    """
    Cas d'erreur : envoyer des données incomplètes.
    Si on oublie le champ "b", l'API doit retourner une erreur 422
    (Unprocessable Entity = données mal formées).
    Pydantic gère cela automatiquement !
    """
    # On envoie {"a": 5} sans "b"
    response = client.post("/add", json={"a": 5})

    # 422 = FastAPI/Pydantic a détecté des données manquantes
    assert response.status_code == 422


def test_donnees_invalides_type():
    """
    Cas d'erreur : envoyer un texte au lieu d'un nombre.
    Pydantic doit rejeter la requête avec un code 422.
    """
    # "abc" n'est pas un nombre → erreur de validation
    response = client.post("/add", json={"a": "abc", "b": 3})
    assert response.status_code == 422
