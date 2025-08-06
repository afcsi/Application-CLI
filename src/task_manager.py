import argparse
import json
import os
from datetime import datetime

TASKS_FILE = os.path.join(os.path.dirname(__file__), '..', 'tasks.json')

def load_tasks():
    """Charge la liste des tâches depuis le fichier JSON."""
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    """Sauvegarde la liste des tâches dans le fichier JSON."""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def add_task(args):
    """Ajoute une nouvelle tâche."""
    tasks = load_tasks()
    next_id = max([t['id'] for t in tasks], default=0) + 1
    task = {
        'id': next_id,
        'title': args.title,
        'desc': args.desc,
        'priority': args.priority,
        'due': args.due,
        'created': datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Tâche ajoutée (ID {next_id})")

def list_tasks(args):
    """Affiche la liste des tâches triées."""
    tasks = load_tasks()
    key = 'priority' if args.sort == 'priority' else 'due'
    tasks_sorted = sorted(tasks, key=lambda t: t[key])
    if not tasks_sorted:
        print("Aucune tâche à afficher.")
        return
    for t in tasks_sorted:
        print(f"[{t['id']}] {t['title']} (Priorité: {t['priority']} – Due: {t['due']})")

def delete_task(args):
    """Supprime une tâche existante."""
    tasks = load_tasks()
    filtered = [t for t in tasks if t['id'] != args.id]
    if len(filtered) == len(tasks):
        print(f"Aucune tâche trouvée avec l'ID {args.id}")
    else:
        save_tasks(filtered)
        print(f"Tâche {args.id} supprimée.")

def main():
    parser = argparse.ArgumentParser(description="Gestionnaire de tâches CLI")
    subparsers = parser.add_subparsers(title="Commandes", dest="command")

    # add
    p = subparsers.add_parser('add', help="Ajouter une nouvelle tâche")
    p.add_argument('--title', required=True, help="Titre de la tâche")
    p.add_argument('--desc', required=True, help="Description de la tâche")
    p.add_argument('--priority', type=int, required=True, help="Priorité (1=haute,5=basse)")
    p.add_argument('--due', required=True, help="Date limite (YYYY-MM-DD)")
    p.set_defaults(func=add_task)

    # list
    p = subparsers.add_parser('list', help="Lister les tâches")
    p.add_argument('--sort', choices=['priority', 'date'], default='priority',
                   help="Tri des tâches")
    p.set_defaults(func=list_tasks)

    # delete
    p = subparsers.add_parser('delete', help="Supprimer une tâche")
    p.add_argument('--id', type=int, required=True, help="ID de la tâche")
    p.set_defaults(func=delete_task)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
