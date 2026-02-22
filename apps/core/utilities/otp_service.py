import random
import re
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail

OTP_EXPIRY_SECONDS = 300  # 5 minutes
OTP_ATTEMPT_LIMIT = 5
OTP_SEND_LIMIT = 5
OTP_RESEND_COOLDOWN = 30  # seconds

def generate_otp():
    return str(random.randint(100000, 999999))

def is_valid_contact(contact):    
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    phone_regex = r'^\+?\d{10,15}$'
    return bool(re.match(email_regex, contact) or re.match(phone_regex, contact))
from apps.core.utilities.email import send_email_template


def send_otp_code(contact, purpose="login"):
    """
    Send an OTP code using the reusable HTML email template.
    
    contact: user's email address
    purpose: string describing purpose, e.g., login, password_reset
    """
    if not is_valid_contact(contact):
        return None, "Invalid contact"

    send_key = f"otp_send_count:{contact}:{purpose}"
    last_sent_key = f"otp_last_sent:{contact}:{purpose}"

    if cache.get(last_sent_key):
        return None, "Please wait before requesting another OTP."

    send_count = cache.get(send_key, 0)
    if send_count >= OTP_SEND_LIMIT:
        return None, "OTP send limit reached. Try later."

    # Generate OTP
    otp_code = generate_otp()

    # Save OTP and rate-limiting info in cache
    cache.set(f"otp:{contact}:{purpose}", otp_code, timeout=OTP_EXPIRY_SECONDS)
    cache.set(send_key, send_count + 1, timeout=3600)  # 1-hour limit
    cache.set(last_sent_key, True, timeout=OTP_RESEND_COOLDOWN)  # cooldown

    # Prepare email context
    context = {
        "user_name": contact.split("@")[0],  # use the local-part of email as username
        "title": "Your OTP Code",
        "message_content": f"Use the following OTP to complete the {purpose} process.",
        "otp": otp_code,
        "expiry_minutes": OTP_EXPIRY_SECONDS // 60
    }

    # Send using reusable template
    send_email_template(
        subject="Your OTP Code",
        recipient_email=contact,
        template_name="emails/base_template.html",
        context=context
    )

    print(f"[DEBUG] OTP for {contact} is {otp_code}")
    return otp_code, None


def verify_otp_code(contact, otp_code, purpose="login"):
    cache_key = f"otp:{contact}:{purpose}"
    stored_code = cache.get(cache_key)

    if not stored_code:
        return False, "OTP expired"

    attempt_key = f"otp_attempt:{contact}:{purpose}"
    attempts = cache.get(attempt_key, 0)
    if attempts >= OTP_ATTEMPT_LIMIT:
        return False, "Too many failed attempts"

    if stored_code == otp_code:
        cache.delete(cache_key)
        cache.delete(attempt_key)
        return True, None

    cache.set(attempt_key, attempts + 1, timeout=OTP_EXPIRY_SECONDS)
    return False, "Invalid OTP"
