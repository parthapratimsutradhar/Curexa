from .expert_rules import EXPERT_RULES

def diagnose(symptoms):

    symptoms = [s.lower() for s in symptoms]

    for rule in EXPERT_RULES:

        if all(symptom in symptoms for symptom in rule["symptoms"]):

            return {
                "possible_condition": rule["condition"],
                "advice": rule["advice"],
                "doctor": rule["doctor"]
            }

    return {
        "possible_condition": "Unknown",
        "advice": "Consult a doctor for proper diagnosis"
    }