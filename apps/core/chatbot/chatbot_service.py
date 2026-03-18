from typing import Any
from apps.doctors.models import Department, Specialization, DoctorProfile
from django.utils.timezone import localdate
from apps.docbook.services.appointment_services import is_doctor_available_today
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

def _normalize_clinician_label(label: str) -> str:
    if not label:
        return ""

    lowered = str(label).strip().lower()
    lowered = lowered.replace("&", " and ")
    lowered = " ".join(lowered.split())

    # Common wording differences between triage labels and DB taxonomy
    synonyms = {
        "ent specialist": "ent",
        "general physician": "general medicine",
        "emergency medicine": "emergency",
        "orthopedic": "orthopedics",
        "dermatologist": "dermatology",
        "ophthalmologist": "ophthalmology",
        "pulmonologist": "pulmonology",
        "neurologist": "neurology",
    }
    lowered = synonyms.get(lowered, lowered)

    for suffix in (" specialist", " doctor", " physician"):
        if lowered.endswith(suffix):
            lowered = lowered[: -len(suffix)].strip()

    return lowered


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

    recommended_doctor = str(rule.get("doctor") or "General Physician").strip()
    response = {
        "matched": True,
        "severity": str(rule.get("severity") or "unknown").strip().lower(),
        "condition": str(rule.get("condition") or "Unknown").strip(),
        "advice": str(rule.get("advice") or "Consult a doctor for proper diagnosis.").strip(),
        "doctor": recommended_doctor,
        "followup_questions": rule.get("followup_questions") if isinstance(rule.get("followup_questions"), list) else [],
        "rule_id": str(rule.get("id") or "").strip(),
    }
    
    directory = get_doctors_by_department(recommended_doctor)
    if directory is not None:
        response["doctor_directory"] = directory

        # Frontend compatibility: the current chatbot UI only renders `reply.doctor`.
        # If we have doctors in `doctor_directory`, append a short summary to `doctor`.
        if isinstance(directory, list) and directory:
            available_names = [
                str(d.get("name") or "").strip()
                for d in directory
                if d.get("is_available_today") and str(d.get("name") or "").strip()
            ][:3]
            all_names = [
                str(d.get("name") or "").strip()
                for d in directory
                if str(d.get("name") or "").strip()
            ][:3]

            suffix = ""
            if available_names:
                suffix = f"Available today: {', '.join(available_names)}"
            elif all_names:
                suffix = f"Doctors: {', '.join(all_names)}"

            if suffix:
                response["doctor"] = f"{recommended_doctor} ({suffix})"

    return response


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



def get_doctors_by_department(department_name: str):
    """
    Department -> Specializations -> Doctors
    """

    dept = _normalize_clinician_label(department_name)

    department = Department.objects.filter(
        name__iexact=dept
    ).first()

    if not department:
        return []

    specializations = Specialization.objects.filter(
        department=department
    )

    if not specializations.exists():
        return []

    doctors = DoctorProfile.objects.select_related(
        "doctor",
        "specialization",
        "specialization__department"
    ).filter(
        specialization__in=specializations,
        doctor__is_active=True
    )

    # ✅ Convert to JSON-safe format
    doctor_list = []

    for doc in doctors:
        doctor_list.append({
            "id": doc.id,
            "name": doc.doctor.get_full_name(),
            "specialization": doc.specialization.name if doc.specialization else None,
            "department": doc.specialization.department.name if doc.specialization and doc.specialization.department else None,
            "experience_years": doc.experience_years,
            "consultation_fee": float(doc.consultation_fee),
            "clinic_address": doc.clinic_address,
            "contact_number": doc.contact_number,
            "profile_picture": doc.profile_picture,
            "is_available_today": is_doctor_available_today(doc.id, localdate()),
        })

    return doctor_list
