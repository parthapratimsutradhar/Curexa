import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set


ALLOWED_SEVERITIES: Set[str] = {"self_care", "routine", "urgent", "emergency", "unknown"}


def _fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    sys.exit(1)


def _load(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        _fail(f"File not found: {path}")
    except json.JSONDecodeError as e:
        _fail(f"Invalid JSON: {e}")

    if not isinstance(data, dict):
        _fail("Top-level JSON must be an object with a 'rules' list")
    if not isinstance(data.get("rules"), list):
        _fail("Top-level object must contain a 'rules' list")

    return data


def _is_non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _ensure_list_of_str(value: Any, field: str, rule_id: str) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        _fail(f"Rule '{rule_id}' field '{field}' must be a list")
    out: List[str] = []
    for i, item in enumerate(value):
        if not _is_non_empty_str(item):
            _fail(f"Rule '{rule_id}' field '{field}' item[{i}] must be a non-empty string")
        out.append(item.strip())
    return out


def validate(data: Dict[str, Any]) -> None:
    rules = data["rules"]
    seen_ids: Set[str] = set()

    if len(rules) == 0:
        _fail("Rules list is empty")

    for idx, rule in enumerate(rules):
        if not isinstance(rule, dict):
            _fail(f"Rule at index {idx} must be an object")

        rule_id = rule.get("id")
        if not _is_non_empty_str(rule_id):
            _fail(f"Rule at index {idx} missing non-empty 'id'")
        rule_id = rule_id.strip()
        if rule_id in seen_ids:
            _fail(f"Duplicate rule id: '{rule_id}'")
        seen_ids.add(rule_id)

        match = rule.get("match")
        if not isinstance(match, dict):
            _fail(f"Rule '{rule_id}' missing 'match' object")

        all_list = _ensure_list_of_str(match.get("all"), "match.all", rule_id)
        any_list = _ensure_list_of_str(match.get("any"), "match.any", rule_id)
        none_list = _ensure_list_of_str(match.get("none"), "match.none", rule_id)

        if rule_id != "fallback_unknown" and not (all_list or any_list):
            _fail(f"Rule '{rule_id}' must define at least one of match.all or match.any")

        severity = rule.get("severity")
        if not _is_non_empty_str(severity):
            _fail(f"Rule '{rule_id}' missing non-empty 'severity'")
        severity_norm = severity.strip().lower()
        if severity_norm not in ALLOWED_SEVERITIES:
            _fail(f"Rule '{rule_id}' severity '{severity}' not in {sorted(ALLOWED_SEVERITIES)}")

        for field in ("condition", "advice", "doctor"):
            if not _is_non_empty_str(rule.get(field)):
                _fail(f"Rule '{rule_id}' missing non-empty '{field}'")

        followups = rule.get("followup_questions")
        if followups is not None:
            _ensure_list_of_str(followups, "followup_questions", rule_id)

        if "priority" in rule:
            pr = rule.get("priority")
            if not isinstance(pr, int):
                _fail(f"Rule '{rule_id}' priority must be an integer")
            if pr < -1000 or pr > 1000:
                _fail(f"Rule '{rule_id}' priority out of range (-1000..1000)")

        # Simple guardrails against accidental prescribing content.
        advice = str(rule.get("advice") or "").lower()
        banned = ["mg", "tablet", "capsule", "antibiotic", "azithro", "amoxic", "ibuprofen", "paracetamol", "acetaminophen"]
        if any(word in advice for word in banned):
            _fail(f"Rule '{rule_id}' advice contains medication/dose-like content; keep advice non-prescriptive")

    print(f"OK: {len(rules)} rules validated")


def main() -> None:
    rules_path = Path(__file__).resolve().parents[1] / "medical_rules.json"
    data = _load(rules_path)
    validate(data)


if __name__ == "__main__":
    main()

