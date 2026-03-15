"""
Deprecated: prefer `medical_rules.json` + `apps.core.chatbot.expert_rules`.

This module remains only to avoid accidental import errors if referenced.
"""

SYMPTOM_RULES = [
    {
        "symptoms": ["fever", "headache"],
        "condition": "Viral fever (example)",
        "advice": "Monitor and seek care if symptoms worsen.",
        "doctor": "General Physician",
    }
]

