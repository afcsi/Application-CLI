# Application-CLI

Bienvenue dans la documentation du gestionnaire de tâches en ligne de commande.

## Guide rapide

> Exécute ces commandes depuis la racine du dépôt.

```bash
# Ajouter une tâche
python src/task_manager.py add --title "Rapport" --desc "Section tests" --priority 1 --due 2025-01-20

# Lister (tri)
python src/task_manager.py list --sort priority
python src/task_manager.py list --sort date

# Filtres de rappel
python src/task_manager.py list --overdue
python src/task_manager.py list --due-in 3

# Modifier / Supprimer
python src/task_manager.py edit --id 1 --title "Rapport final" --priority 2
python src/task_manager.py delete --id 1
```

```{toctree}
:maxdepth: 1
:caption: Référence

api
```
