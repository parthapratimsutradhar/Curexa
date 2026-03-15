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


# def _doctor_directory_for_recommendation(recommended_doctor: str) -> dict | None:
#     """
#     Attempts to map the triage 'recommended_doctor' label to the platform's
#     Department -> Specialization taxonomy, then returns doctors + availability.

#     Returns None if the database/models are unavailable (e.g. during non-Django use).
#     """
#     try:
#         from django.db.models import Q
#         from django.utils.timezone import localdate

#         from apps.doctors.models.department_model import Department
#         from apps.doctors.models.specialization_model import Specialization
#         from apps.doctors.services import doctor_services
#     except Exception:
#         return None

#     normalized = _normalize_clinician_label(recommended_doctor)
#     if not normalized:
#         return None

#     def score(candidate: str) -> int:
#         c = _normalize_clinician_label(candidate)
#         if not c:
#             return 0
#         if c == normalized:
#             return 100
#         if c in normalized:
#             return 70
#         if normalized in c:
#             return 60
#         c_words = set(c.split())
#         n_words = set(normalized.split())
#         overlap = len(c_words & n_words)
#         if overlap:
#             return 40 + (overlap * 5)
#         return 0

#     # Prefer matching Specialization first (it already points to Department)
#     spec_candidates = list(
#         Specialization.objects.select_related("department").filter(
#             Q(name__iexact=recommended_doctor)
#             | Q(name__iexact=normalized)
#             | Q(name__icontains=normalized)
#             | Q(name__icontains=recommended_doctor)
#         )[:25]
#     )
#     best_spec = None
#     if spec_candidates:
#         best_spec = sorted(spec_candidates, key=lambda s: score(s.name), reverse=True)[0]
#         if score(best_spec.name) == 0:
#             best_spec = None

#     best_dept = best_spec.department if best_spec and best_spec.department else None

#     if not best_dept:
#         dept_candidates = list(
#             Department.objects.filter(
#                 Q(name__iexact=recommended_doctor)
#                 | Q(name__iexact=normalized)
#                 | Q(name__icontains=normalized)
#                 | Q(name__icontains=recommended_doctor)
#             )[:25]
#         )
#         if dept_candidates:
#             best_dept = sorted(dept_candidates, key=lambda d: score(d.name), reverse=True)[0]
#             if score(best_dept.name) == 0:
#                 best_dept = None

#     selected_date = localdate()
#     qs = doctor_services.doctor_queryset(date=selected_date.isoformat()).filter(doctor__is_active=True)

#     if best_spec:
#         qs = qs.filter(specialization=best_spec)
#     elif best_dept:
#         qs = qs.filter(specialization__department=best_dept)
#     else:
#         # No taxonomy match; don't dump the whole directory from chatbot.
#         return {
#             "date": str(selected_date),
#             "recommended_label": recommended_doctor,
#             "matched_department": None,
#             "matched_specialization": None,
#             "available_doctors": [],
#             "other_doctors": [],
#             "note": "No matching department/specialization found for this recommendation.",
#         }

#     doctors = doctor_services.doctor_list_data(qs[:30])

#     def has_open_slot(d: dict) -> bool:
#         slots = d.get("available_slots") or []
#         return any(bool(s.get("is_available")) for s in slots)

#     available = []
#     other = []
#     for d in doctors:
#         item = {
#             "id": d.get("id"),
#             "name": d.get("name"),
#             "department": d.get("department"),
#             "specialization": d.get("specialization"),
#             "consultation_fee": d.get("consultation_fee"),
#             "experience_years": d.get("experience_years"),
#             "clinic_address": d.get("clinic_address"),
#             "contact_number": d.get("contact_number"),
#             "is_available_today": bool(d.get("is_available")),
#             "has_open_slot": has_open_slot(d),
#             "available_slots": (d.get("available_slots") or [])[:4],
#         }
#         (available if item["has_open_slot"] else other).append(item)

#     return {
#         "date": str(selected_date),
#         "recommended_label": recommended_doctor,
#         "matched_department": best_dept.name if best_dept else None,
#         "matched_specialization": best_spec.name if best_spec else None,
#         "available_doctors": available[:6],
#         "other_doctors": other[:6],
#         "total_found": len(doctors),
#     }


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
