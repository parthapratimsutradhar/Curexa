import json
from pathlib import Path
from typing import Dict, List, Any


def _repo_root() -> Path:
    # apps/core/chatbot/expert_rules.py -> repo root is 3 parents up
    return Path(__file__).resolve().parents[3]


def load_rules() -> List[Dict[str, Any]]:
    rules_path = _repo_root() / "medical_rules.json"
    with rules_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        rules = data
    elif isinstance(data, dict) and isinstance(data.get("rules"), list):
        rules = data["rules"]
    else:
        raise ValueError("medical_rules.json must be a list or an object with a 'rules' list")

    if not all(isinstance(r, dict) for r in rules):
        raise ValueError("medical_rules.json rules must be objects")

    return rules


EXPERT_RULES = load_rules()
