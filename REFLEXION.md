# Document de réflexion

## Introduction
- **Sujet** : Option A — Application CLI (`argparse`).
- **Objectifs** : CRUD des tâches (add/list/edit/delete), persistance JSON, rappels (retard et proches de l’échéance), documentation Sphinx, tests unitaires, et pipeline CI/CD professionnel.
- **Organisation Git** : branches `feature/*` pour chaque fonctionnalité, intégration en `develop`, publication via `main` (déploiement des docs).

## Développement
### Étapes principales
1. **Structure CLI & dépôt** : arborescence `src/`, `tests/`, workflow CI de base, README initial.
2. **Persistance JSON** : `load_tasks()`/`save_tasks()` avec fichier `tasks.json` à la racine (chemin relatif stable).
3. **Fonctionnalités** : `add`, `list` (tri priorité/date), `delete`, puis `edit` (mise à jour sélective des champs).
4. **Rappels** : indicateurs `⚠️ OVERDUE` (date passée) et `⏳ soon` (≤ N jours), filtres `--overdue` et `--due-in`.
5. **Docstrings** : format PEP257/Google sur 100 % du module pour l’autodoc Sphinx.
6. **Documentation Sphinx** : MyST pour la page d’accueil (`index.md`) + `api.rst` pour l’API ; publication GitHub Pages.
7. **Durcissement CI** : seuils bloquants `coverage --fail-under=95` et `pylint --fail-under=9.0` sur 3 versions de Python.

### Problèmes rencontrés & solutions
- **Découverte de tests en CI** : erreurs d’import ⇒ ajout de `PYTHONPATH=${{ github.workspace }}/src` et `tests/__init__.py`.
- **Couverture insuffisante (<95%)** : ajout de tests ciblés : intégration CLI (`main()`/`argparse`), cas limites (aide sans args, `due` vide, indicateur `⏳`). Passage à 95 %+.
- **YAML Actions invalide / étapes fragiles** : réécriture propre de `.github/workflows/ci.yml`, cache `pip`, jobs séparés (test / deploy-doc).
- **Qualité pylint** : suppression des `except Exception`, renommage de variables, petites refactorisations.

## Pipeline CI/CD
- **build-and-test** (3.8/3.9/3.10) : installation deps, exécution `unittest` avec `coverage` (seuil ≥95), `pylint` (seuil ≥9.0).
- **deploy-doc** (sur `main` uniquement) : build Sphinx (`myst-parser`, thème RTD), publication GitHub Pages (`gh-pages`).
- **Artefacts/optimisations** : cache pip, rapport coverage texte (et possibilité d’HTML/artefact).

## Conclusion & auto‑évaluation
- **Réussites** : fonctionnalités complètes et testables, docstrings 100 %, documentation en ligne, CI stricte multi‑Python.
- **À améliorer** : packaging (`pyproject.toml`) + entrée `console_scripts`, plus de commandes (recherche, export CSV), tests supplémentaires de chemins d’erreur.
- **Apprentissages** : bonnes pratiques Git (branches/PR), GitHub Actions, écriture de tests orientés couverture, Sphinx/MyST, respect PEP8/PEP257.
