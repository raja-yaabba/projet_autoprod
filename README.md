# TP CI/CD — Spring Boot + Flask + Docker + GitHub Actions

Ce dépôt contient :
- `springboot-app/` : service Java Spring Boot (MySQL)
- `flask-app/` : votre projet Flask importé (port 5000)
- `docker-compose.yml` : pour lancer les services localement
- `.github/workflows/ci-cd.yml` : pipeline GitHub Actions (build/test + images Docker)
- `Dockerfile` dans chaque service

## Lancer en local (sans CI/CD)

```bash
docker compose up --build
```
- Spring Boot: http://localhost:8080/api/users
- MySQL: port 3306 (user `root` / password `root`)
- Flask: http://localhost:5000

> NB: Si votre point d'entrée Flask n'est pas `app.py`, modifiez la ligne `CMD` dans `flask-app/Dockerfile` pour cibler votre fichier (ex: `python main.py`). Détection auto trouvée: web_flask/controller.py.

## Créer le dépôt GitHub et pousser le code

### Option A — via l'interface web
1. Allez sur GitHub → **New repository** → nommez-le (ex: `tp-ci-cd`), laissez public ou privé.
2. En local :
   ```bash
   cd TP-CICD
   git init
   git add .
   git commit -m "TP CI/CD init"
   git branch -M main
   git remote add origin https://github.com/<votre-user>/<votre-repo>.git
   git push -u origin main
   ```

### Option B — via GitHub CLI (gh)
1. Installez `gh` et connectez-vous : `gh auth login`
2. Depuis le dossier `TP-CICD` :
   ```bash
   git init
   git add .
   git commit -m "TP CI/CD init"
   git branch -M main
   gh repo create <votre-repo> --source=. --public --push
   ```

## Docker Hub (pour la pipeline)
- Dans GitHub → Settings → Secrets and variables → **Actions** → **New repository secret** :
  - `DOCKER_USERNAME` = votre identifiant Docker Hub
  - `DOCKER_PASSWORD` = votre mot de passe/token Docker Hub

La pipeline construira et poussera deux images :
- `${ secrets.DOCKER_USERNAME }/springboot-app:latest`
- `${ secrets.DOCKER_USERNAME }/flask-app:latest`

## Tests
- Spring Boot : `mvn test` (exécuté aussi par Actions)
- Flask : ajoutez des tests `pytest`/`unittest` si besoin (adapter la step dans le workflow).

## Déploiement (exemple VM de prod)
```bash
docker pull <docker-user>/springboot-app:latest
docker pull <docker-user>/flask-app:latest
# Ou via docker compose si vous utilisez ce repo en prod
```

Bon TP 🚀
