import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SETTINGS_FILE = BASE_DIR / 'settings.json'
LEADERBOARD_FILE = BASE_DIR / 'leaderboard.json'

DEFAULT_SETTINGS = {
    'sound': True,
    'car_color': 'blue',
    'difficulty': 'normal'
}


def _read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        with path.open('r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def _write_json(path: Path, data):
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_settings():
    data = _read_json(SETTINGS_FILE, DEFAULT_SETTINGS.copy())
    merged = DEFAULT_SETTINGS.copy()
    if isinstance(data, dict):
        merged.update(data)
    else:
        merged.update(DEFAULT_SETTINGS)
    return merged



def save_settings(settings):
    merged = DEFAULT_SETTINGS.copy()
    merged.update(settings)
    _write_json(SETTINGS_FILE, merged)



def load_leaderboard():
    data = _read_json(LEADERBOARD_FILE, [])
    return data if isinstance(data, list) else []



def save_leaderboard(entries):
    _write_json(LEADERBOARD_FILE, entries[:10])



def add_score(entry):
    entries = load_leaderboard()
    entries.append(entry)
    entries.sort(key=lambda item: (-int(item.get('score', 0)), -int(item.get('distance', 0))))
    save_leaderboard(entries[:10])
    return entries[:10]
