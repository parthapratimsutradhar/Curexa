# enduser/templatetags/cart_tags.py
from django import template
from apps.medistore.services import cart_services
from apps.core.utilities import get_user_from_jwt

register = template.Library()

@register.simple_tag(takes_context=True)
def get_cart_count(context):
    request = context.get('request')
    user = get_user_from_jwt(request) if request else None
    patient = getattr(user, "patient_profile", None)

    return cart_services.cart_count(patient) if patient else 0