# apps/core/context_processors.py
from apps.medistore.services import cart_services
from apps.accounts.services import patient_services

def cart_context(request):
    """
    Adds cart count and user id to all templates using JWT-authenticated users.
    """
    cart_count = 0
    user_id = None

    if hasattr(request, "user") and request.user.is_authenticated:        
        patient = patient_services.get_patient(request.user.id)
        if patient:
            cart_count = cart_services.cart_count(patient.id)

    return {
        "cart_count": cart_count,
        "user_id": user_id,
    }