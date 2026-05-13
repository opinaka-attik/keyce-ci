# =============================================================================
# FICHIER : Dockerfile
# RÔLE    : Recette pour construire une image Docker de notre application.
#
# QU'EST-CE QUE DOCKER ?
#   Docker permet d'emballer une application et tout son environnement
#   (Python, bibliothèques, config) dans un "conteneur" portable.
#   → L'app fonctionnera identiquement sur n'importe quelle machine.
#
# VOCABULAIRE :
#   Image   = la "recette" construite à partir de ce fichier
#   Conteneur = une instance en cours d'exécution de cette image
#
# COMMANDES UTILES :
#   Construire l'image  : docker build -t calculator-api .
#   Lancer le conteneur : docker run -p 8000:8000 calculator-api
# =============================================================================


# -----------------------------------------------------------------------------
# ÉTAPE 1 : Image de base
# -----------------------------------------------------------------------------
# On part d'une image officielle Python 3.11 version "slim" (légère).
# "slim" = sans outils inutiles → image plus petite et plus sécurisée.
FROM python:3.11-slim


# -----------------------------------------------------------------------------
# ÉTAPE 2 : Répertoire de travail
# -----------------------------------------------------------------------------
# Tous les fichiers de l'app seront placés dans /app à l'intérieur du conteneur.
# C'est comme faire "cd /app" → les commandes suivantes s'exécutent ici.
WORKDIR /app


# -----------------------------------------------------------------------------
# ÉTAPE 3 : Copier et installer les dépendances
# -----------------------------------------------------------------------------
# On copie UNIQUEMENT requirements.txt en premier (avant le reste du code).
# Pourquoi ? Optimisation du cache Docker :
#   Si on ne modifie que le code (pas les dépendances),
#   Docker réutilise le cache de cette étape → build beaucoup plus rapide !
COPY requirements.txt .

# Installer les bibliothèques Python listées dans requirements.txt
# --no-cache-dir = ne pas stocker le cache pip → image plus légère
RUN pip install --no-cache-dir -r requirements.txt


# -----------------------------------------------------------------------------
# ÉTAPE 4 : Copier le code source
# -----------------------------------------------------------------------------
# On copie maintenant tout le reste du projet dans /app.
# Le "." signifie "tout le dossier courant" (depuis la machine hôte).
COPY . .


# -----------------------------------------------------------------------------
# ÉTAPE 5 : Exposer le port
# -----------------------------------------------------------------------------
# On indique que le conteneur utilisera le port 8000.
# EXPOSE est documentaire (ne publie pas réellement le port → c'est docker run -p qui le fait).
EXPOSE 8000


# -----------------------------------------------------------------------------
# ÉTAPE 6 : Commande de démarrage
# -----------------------------------------------------------------------------
# Commande exécutée quand le conteneur démarre.
# uvicorn  : serveur web ASGI pour FastAPI
# app.main : module Python à charger (fichier app/main.py)
# :app     : variable FastAPI dans ce fichier (notre objet "app")
# --host 0.0.0.0  : écouter sur toutes les interfaces réseau (pas juste localhost)
# --port 8000     : port d'écoute
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
