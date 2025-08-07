import argparse
import json
import os
from datetime import datetime, date, timedelta  # <— ajouté

TASKS_FILE = os.path.join(os.path.dirname(__file__), '..', 'tasks.json')
DATE_FMT = "%Y-%m-%d"

def parse_date(s):
    return datetime.strptime(s, DATE_FMT).date()

def validate_due(due):
    try:
        parse_date(due)
    except ValueError:
        raise ValueError("Format de date invalide, attendu YYYY-MM-DD")

def validate_priority(p):
    if p < 1 or p > 5:
        raise ValueError("La priorité doit être comprise entre 1 (haute) et 5 (basse)")

def load_tasks():
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def add_task(args):
    tasks = load_tasks()
    validate_priority(args.priority)
    validate_due(args.due)
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
    tasks = load_tasks()

    # Filtrages (overdue/due-in arriveront étape 2 ; ici on ne les utilise pas encore)
    filtered = list(tasks)

    # Tri robuste
    if args.sort == 'priority':
        filtered.sort(key=lambda t: int(t.get('priority', 5)))
    else:  # 'date'
        def key_date(t):
            try:
                return parse_date(t.get('due', '9999-12-31'))
            except Exception:
                return date.max
        filtered.sort(key=key_date)

    if not filtered:
        print("Aucune tâche à afficher.")
        return

    for t in filtered:
        print(f"[{t['id']}] {t['title']} (Priorité: {t['priority']} – Due: {t['due']})")

def delete_task(args):
    tasks = load_tasks()
    filtered = [t for t in tasks if t['id'] != args.id]
    if len(filtered) == len(tasks):
        print(f"Aucune tâche trouvée avec l'ID {args.id}")
    else:
        save_tasks(filtered)
        print(f"Tâche {args.id} supprimée.")

def edit_task(args):
    """Modifie une tâche existante par ID. Seuls les champs fournis sont modifiés."""
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == args.id:
            if args.title is not None:
                t['title'] = args.title
            if args.desc is not None:
                t['desc'] = args.desc
            if args.priority is not None:
                validate_priority(args.priority)
                t['priority'] = args.priority
            if args.due is not None:
                validate_due(args.due)
                t['due'] = args.due
            save_tasks(tasks)
            print(f"Tâche {args.id} mise à jour.")
            return
    print(f"Aucune tâche trouvée avec l'ID {args.id}")

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
    p.add_argument('--sort', choices=['priority', 'date'], default='priority', help="Tri des tâches")
    p.set_defaults(func=list_tasks)

    # delete
    p = subparsers.add_parser('delete', help="Supprimer une tâche")
    p.add_argument('--id', type=int, required=True, help="ID de la tâche")
    p.set_defaults(func=delete_task)

    # edit  <— NOUVEAU
    p = subparsers.add_parser('edit', help="Modifier une tâche existante")
    p.add_argument('--id', type=int, required=True, help="ID de la tâche")
    p.add_argument('--title', help="Nouveau titre")
    p.add_argument('--desc', help="Nouvelle description")
    p.add_argument('--priority', type=int, help="Nouvelle priorité (1-5)")
    p.add_argument('--due', help="Nouvelle date (YYYY-MM-DD)")
    p.set_defaults(func=edit_task)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        try:
            args.func(args)
        except ValueError as e:
            print(f"Erreur: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
