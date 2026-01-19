LANG_OPTIONS = ("pl", "en")
DEFAULT_LANG = "pl"

TRANSLATIONS = {
    "pl": {
        "choose_language": "wybierz język:",
        "add_task_header": "Dodaj nowe zadanie",
        "task_input_label": "wpisz treść:",
        "add_button_label": "DODAJ",
        "task_list_header": "Lista zadań",
        "filter_label": "wyświetl:",
        "sort_label": "sortuj wg:",
        "empty_tasks_info": "Aktualnie nie masz żadnych zadań!",
        "created_at_label": "data utworzenia:",
        "clear_all_button_label": "WYCZYŚĆ WSZYSTKIE",
        "delete_icon_label": "🗑️",
        "filter_all": "wszystkie",
        "filter_done": "ukończone",
        "filter_not_done": "nieukończone",
        "sort_created_asc": "data utworzenia (rosnąco)",
        "sort_created_desc": "data utworzenia (malejąco)",
        "sort_desc_asc": "treść zadania (A-Z)",
        "sort_desc_desc": "treść zadania (Z-A)",
    },
    "en": {
        "choose_language": "choose language:",
        "add_task_header": "Add new task",
        "task_input_label": "enter task:",
        "add_button_label": "ADD",
        "task_list_header": "Task list",
        "filter_label": "show:",
        "sort_label": "sort by:",
        "empty_tasks_info": "You have no tasks yet!",
        "created_at_label": "created at:",
        "clear_all_button_label": "CLEAR ALL",
        "delete_icon_label": "🗑️",
        "filter_all": "all",
        "filter_done": "completed",
        "filter_not_done": "not completed",
        "sort_created_asc": "created (asc)",
        "sort_created_desc": "created (desc)",
        "sort_desc_asc": "task name (A-Z)",
        "sort_desc_desc": "task name (Z-A)",
    },
}


def t(lang: str, key: str) -> str:
    lang = lang if lang in LANG_OPTIONS else DEFAULT_LANG
    return TRANSLATIONS.get(lang, {}).get(key) or key
