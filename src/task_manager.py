import argparse

def add_task(args):
    """Ajoute une nouvelle tâche."""
    print(f"Ajout de la tâche : {args.title} | Priorité : {args.priority} | Date limite : {args.due}")
    # TODO: Implémenter la sauvegarde dans un fichier JSON

def list_tasks(args):
    """Affiche la liste des tâches triées."""
    print(f"Affichage des tâches triées par : {args.sort}")
    # TODO: Implémenter l'affichage des tâches depuis le fichier JSON

def delete_task(args):
    """Supprime une tâche existante."""
    print(f"Suppression de la tâche avec l'ID : {args.id}")
    # TODO: Implémenter la suppression dans le fichier JSON

def main():
    parser = argparse.ArgumentParser(description="Gestionnaire de tâches CLI")
    subparsers = parser.add_subparsers(title="Commandes", dest="command")

    # Commande : add
    parser_add = subparsers.add_parser('add', help="Ajouter une nouvelle tâche")
    parser_add.add_argument('--title', required=True, help="Titre de la tâche")
    parser_add.add_argument('--desc', required=True, help="Description de la tâche")
    parser_add.add_argument('--priority', type=int, required=True, help="Priorité de la tâche (1 = Haute, 5 = Basse)")
    parser_add.add_argument('--due', required=True, help="Date limite (YYYY-MM-DD)")
    parser_add.set_defaults(func=add_task)

    # Commande : list
    parser_list = subparsers.add_parser('list', help="Lister les tâches")
    parser_list.add_argument('--sort', choices=['priority', 'date'], default='priority', help="Tri des tâches")
    parser_list.set_defaults(func=list_tasks)

    # Commande : delete
    parser_delete = subparsers.add_parser('delete', help="Supprimer une tâche")
    parser_delete.add_argument('--id', type=int, required=True, help="ID de la tâche à supprimer")
    parser_delete.set_defaults(func=delete_task)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
