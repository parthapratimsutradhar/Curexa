from typing import Any

from .expert_rules import EXPERT_RULES
from .rule_engine import pick_best_rule


def _format_followups(followups: Any) -> str:
    if not isinstance(followups, list):
        return ""

    cleaned = [str(x).strip() for x in followups if str(x).strip()]
    if not cleaned:
        return ""

    lines = "\n".join(f"- {q}" for q in cleaned[:3])
    return f"\n\nFollow-up questions:\n{lines}"


def diagnose_structured(message: str) -> dict:
    rule = pick_best_rule(message, EXPERT_RULES)
    if not rule:
        return {
            "matched": False,
            "severity": "unknown",
            "condition": "Unknown",
            "advice": (
                "I couldn't confidently match your symptoms. "
                "If symptoms are severe or worsening, seek in-person medical care. "
                "For life-threatening symptoms, call local emergency services immediately."
            ),
            "doctor": "General Physician",
            "followup_questions": [
                "What are your main symptoms (top 2–3) and how long have they been present?",
                "How severe is it (mild/moderate/severe) and is it getting worse?",
                "Any red flags like chest pain, trouble breathing, fainting, confusion, or weakness on one side?"
            ],
        }

    return {
        "matched": True,
        "severity": str(rule.get("severity") or "unknown").strip().lower(),
        "condition": str(rule.get("condition") or "Unknown").strip(),
        "advice": str(rule.get("advice") or "Consult a doctor for proper diagnosis.").strip(),
        "doctor": str(rule.get("doctor") or "General Physician").strip(),
        "followup_questions": rule.get("followup_questions") if isinstance(rule.get("followup_questions"), list) else [],
        "rule_id": str(rule.get("id") or "").strip(),
    }


def diagnose(message: str) -> str:
    data = diagnose_structured(message)
    condition = data["condition"]
    advice = data["advice"]
    doctor = data["doctor"]
    severity = data["severity"]
    followups = _format_followups(data.get("followup_questions"))
    return (
        f"Severity: {severity}\n\n"
        f"Possible Condition: {condition}\n\n"
        f"Advice:\n{advice}\n\n"
        f"Recommended Doctor: {doctor}"
        f"{followups}\n\n"
        "This is not a medical diagnosis. Please consult a qualified clinician."
    )
