"""CLI de gestion de tâches personnelles.

Ce module fournit un petit gestionnaire de tâches en ligne de commande (Option A) :
- CRUD partiel : add, list (avec tri et filtres de rappel), edit, delete
- Persistance JSON (``tasks.json`` à la racine du dépôt)
- Validations basiques (priorité / date)
- Exécutable via ``python src/task_manager.py <commande>``

Les fonctions exposées sont pensées pour être testées avec ``unittest``.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import date, datetime, timedelta
from typing import Any, Dict, List

# Fichier de persistance (à la racine du repo)
TASKS_FILE = os.path.join(os.path.dirname(__file__), "..", "tasks.json")
DATE_FMT = "%Y-%m-%d"


# ---------- Helpers ----------
def parse_date(text: str) -> date:
    """Convertit une chaîne ``YYYY-MM-DD`` en objet :class:`datetime.date`.

    Args:
        text: Date au format ``YYYY-MM-DD``.

    Returns:
        Un objet :class:`datetime.date`.

    Raises:
        ValueError: Si le format n'est pas valide.
    """
    return datetime.strptime(text, DATE_FMT).date()


def validate_due(due: str) -> None:
    """Valide la date d'échéance.

    Args:
        due: Date au format ``YYYY-MM-DD``.

    Raises:
        ValueError: Si la date n'a pas le bon format.
    """
    try:
        parse_date(due)
    except ValueError as exc:
        raise ValueError("Format de date invalide, attendu YYYY-MM-DD") from exc


def validate_priority(priority: int) -> None:
    """Valide la priorité (1 à 5).

    Args:
        priority: Priorité numérique où 1 est haute et 5 est basse.

    Raises:
        ValueError: Si la priorité n'est pas comprise entre 1 et 5.
    """
    if priority < 1 or priority > 5:
        raise ValueError("La priorité doit être comprise entre 1 (haute) et 5 (basse)")


def is_overdue(due_str: str) -> bool:
    """Indique si la tâche est en retard.

    Args:
        due_str: Date d'échéance au format ``YYYY-MM-DD``.

    Returns:
        True si la date est strictement antérieure à aujourd'hui, sinon False.
    """
    return parse_date(due_str) < date.today()


def is_due_within(due_str: str, days: int) -> bool:
    """Indique si l'échéance est dans *days* jours au plus.

    Args:
        due_str: Date d'échéance au format ``YYYY-MM-DD``.
        days: Nombre de jours maximum avant l'échéance.

    Returns:
        True si ``today <= due <= today + days``.
    """
    d_day = parse_date(due_str)
    return date.today() <= d_day <= date.today() + timedelta(days=days)


def status_flag(task: Dict[str, Any]) -> str:
    """Retourne un petit indicateur visuel pour l'affichage.

    Args:
        task: Dictionnaire représentant la tâche.

    Returns:
        Une chaîne vide, ``"⚠️ OVERDUE"`` si en retard, ou ``"⏳ soon"`` si <= 3 jours.
    """
    try:
        if is_overdue(task["due"]):
            return "⚠️ OVERDUE"
        if is_due_within(task["due"], 3):
            return "⏳ soon"
    except Exception:
        # On évite de casser l'affichage si un champ est manquant/mal formé.
        pass
    return ""


# ---------- I/O JSON ----------
def load_tasks() -> List[Dict[str, Any]]:
    """Charge la liste des tâches depuis le fichier JSON.

    Returns:
        Une liste de dictionnaires représentant les tâches.
    """
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Sauvegarde la liste des tâches dans le fichier JSON.

    Args:
        tasks: Liste de tâches à persister.
    """
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


# ---------- Opérations (utilisées par la CLI et les tests) ----------
def add_task(args: argparse.Namespace) -> None:
    """Ajoute une nouvelle tâche.

    Args:
        args: Arguments de la CLI. Attendus : ``title``, ``desc``, ``priority``, ``due``.
    """
    tasks = load_tasks()
    validate_priority(args.priority)
    validate_due(args.due)

    next_id = max([t["id"] for t in tasks], default=0) + 1
    task = {
        "id": next_id,
        "title": args.title,
        "desc": args.desc,
        "priority": args.priority,
        "due": args.due,
        "created": datetime.now().isoformat(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Tâche ajoutée (ID {next_id})")


def list_tasks(args: argparse.Namespace) -> None:
    """Affiche les tâches triées, avec filtres de rappel.

    Args:
        args: Arguments de la CLI. Attendus : ``sort``, ``overdue`` (bool),
            ``due_in`` (int ou None).
    """
    tasks = load_tasks()
    filtered = list(tasks)

    # Filtres de rappel
    if getattr(args, "overdue", False):
        filtered = [t for t in filtered if t.get("due") and is_overdue(t["due"])]
    elif getattr(args, "due_in", None) is not None:
        n = int(args.due_in)
        filtered = [t for t in filtered if t.get("due") and is_due_within(t["due"], n)]

    # Tri
    if args.sort == "priority":
        filtered.sort(key=lambda t: int(t.get("priority", 5)))
    else:
        def key_date(t: Dict[str, Any]) -> date:
            try:
                return parse_date(t.get("due", "9999-12-31"))
            except Exception:
                return date.max
        filtered.sort(key=key_date)

    if not filtered:
        print("Aucune tâche à afficher.")
        return

    for t in filtered:
        flag = status_flag(t)
        flag = f" {flag}" if flag else ""
        print(f"[{t['id']}] {t['title']} (Priorité: {t['priority']} – Due: {t['due']}){flag}")


def delete_task(args: argparse.Namespace) -> None:
    """Supprime une tâche par ID.

    Args:
        args: Arguments de la CLI. Attendu : ``id`` (int).
    """
    tasks = load_tasks()
    filtered = [t for t in tasks if t["id"] != args.id]
    if len(filtered) == len(tasks):
        print(f"Aucune tâche trouvée avec l'ID {args.id}")
    else:
        save_tasks(filtered)
        print(f"Tâche {args.id} supprimée.")


def edit_task(args: argparse.Namespace) -> None:
    """Modifie une tâche existante (seuls les champs fournis sont mis à jour).

    Args:
        args: Arguments de la CLI. Attendus : ``id`` et, optionnellement,
            ``title``, ``desc``, ``priority``, ``due``.
    """
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == args.id:
            if args.title is not None:
                task["title"] = args.title
            if args.desc is not None:
                task["desc"] = args.desc
            if args.priority is not None:
                validate_priority(args.priority)
                task["priority"] = args.priority
            if args.due is not None:
                validate_due(args.due)
                task["due"] = args.due
            save_tasks(tasks)
            print(f"Tâche {args.id} mise à jour.")
            return
    print(f"Aucune tâche trouvée avec l'ID {args.id}")


# ---------- CLI ----------
def main() -> None:
    """Point d'entrée de l'application CLI."""
    parser = argparse.ArgumentParser(description="Gestionnaire de tâches CLI")
    subparsers = parser.add_subparsers(title="Commandes", dest="command")

    # add
    p_add = subparsers.add_parser("add", help="Ajouter une nouvelle tâche")
    p_add.add_argument("--title", required=True, help="Titre de la tâche")
    p_add.add_argument("--desc", required=True, help="Description de la tâche")
    p_add.add_argument("--priority", type=int, required=True, help="Priorité (1=haute,5=basse)")
    p_add.add_argument("--due", required=True, help="Date limite (YYYY-MM-DD)")
    p_add.set_defaults(func=add_task)

    # list
    p_list = subparsers.add_parser("list", help="Lister les tâches")
    p_list.add_argument("--sort", choices=["priority", "date"], default="priority", help="Tri")
    mg = p_list.add_mutually_exclusive_group()
    mg.add_argument("--overdue", action="store_true", help="Afficher uniquement les tâches en retard")
    mg.add_argument("--due-in", type=int, metavar="JOURS", help="Afficher les tâches à échéance ≤ N jours")
    p_list.set_defaults(func=list_tasks)

    # delete
    p_del = subparsers.add_parser("delete", help="Supprimer une tâche")
    p_del.add_argument("--id", type=int, required=True, help="ID de la tâche")
    p_del.set_defaults(func=delete_task)

    # edit
    p_edit = subparsers.add_parser("edit", help="Modifier une tâche existante")
    p_edit.add_argument("--id", type=int, required=True, help="ID de la tâche")
    p_edit.add_argument("--title", help="Nouveau titre")
    p_edit.add_argument("--desc", help="Nouvelle description")
    p_edit.add_argument("--priority", type=int, help="Nouvelle priorité (1-5)")
    p_edit.add_argument("--due", help="Nouvelle date (YYYY-MM-DD)")
    p_edit.set_defaults(func=edit_task)

    args = parser.parse_args()
    if hasattr(args, "func"):
        try:
            args.func(args)
        except ValueError as exc:
            print(f"Erreur: {exc}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
