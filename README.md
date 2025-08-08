# Application-CLI

[![CI](https://github.com/afcsi/Application-CLI/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/afcsi/Application-CLI/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-brightgreen)](https://afcsi.github.io/Application-CLI/)
![Python](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10-blue)

Gestionnaire de tâches en ligne de commande (Option A – `argparse`).

## Installation
```bash
python -m pip install -r requirements.txt
```

## Utilisation (depuis la racine du dépôt)
```bash
# Ajouter une tâche
python src/task_manager.py add --title "Rapport" --desc "Section tests" --priority 1 --due 2025-01-20

# Lister (tri)
python src/task_manager.py list --sort priority
python src/task_manager.py list --sort date

# Rappels
python src/task_manager.py list --overdue
python src/task_manager.py list --due-in 3

# Modifier / Supprimer
python src/task_manager.py edit --id 1 --title "Rapport final" --priority 2
python src/task_manager.py delete --id 1
```

## Qualité & CI
- Tests `unittest` **coverage ≥ 95%** (bloquant)
- **pylint ≥ 9.0** (bloquant)
- Doc Sphinx (MyST) publiée : https://afcsi.github.io/Application-CLI/

## Structure du dépôt
```
.
├─ src/task_manager.py
├─ tests/
│  ├─ test_task_manager.py
│  ├─ test_reminders_and_edit.py
│  ├─ test_validations_and_errors.py
│  ├─ test_cli_integration.py
│  └─ test_extra_coverage.py
├─ docs/
│  ├─ conf.py
│  ├─ index.md
│  └─ api.rst
├─ .github/workflows/ci.yml
├─ requirements.txt
└─ README.md
```

## Licence
Projet pédagogique.
