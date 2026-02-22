from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
import os

def send_email_template(
    subject: str,
    recipient_email: str,
    template_name: str,
    context: dict,
    from_email=None,
    pdf_path: str = None,
    ics_path: str = None
):
    """
    Send an HTML email using a reusable template with optional PDF or calendar (ICS) attachment.

    context: dictionary containing template variables like user_name, message_content, otp, etc.
    pdf_path: optional path to a PDF file to attach
    ics_path: optional path to an ICS calendar file to attach
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    # Default template context variables
    context.setdefault("current_date", timezone.now().strftime("%d %b, %Y"))
    context.setdefault("current_year", timezone.now().year)
    context.setdefault(
        "logo_url",
        "https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1663574980688_114990/archisketch-logo"
    )
    context.setdefault("company_name", "Archisketch Company")
    context.setdefault("company_address", "Address 540, City, State")
    context.setdefault("social_icons", [
        {"url": "#", "img": "https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661502815169_682499/email-template-icon-facebook", "alt": "Facebook"},
        {"url": "#", "img": "https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661504218208_684135/email-template-icon-instagram", "alt": "Instagram"},
        {"url": "#", "img": "https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661503043040_372004/email-template-icon-twitter", "alt": "Twitter"},
        {"url": "#", "img": "https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661503195931_210869/email-template-icon-youtube", "alt": "Youtube"},
    ])

    # Render HTML email
    html_content = render_to_string(template_name, context)
    msg = EmailMultiAlternatives(subject, "", from_email, [recipient_email])
    msg.attach_alternative(html_content, "text/html")

    # Attach PDF if provided
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as pdf_file:
            filename = os.path.basename(pdf_path)
            msg.attach(filename, pdf_file.read(), "application/pdf")

    # Attach ICS (calendar event) if provided
    if ics_path and os.path.exists(ics_path):
        with open(ics_path, "rb") as ics_file:
            filename = os.path.basename(ics_path)
            msg.attach(filename, ics_file.read(), "text/calendar")

    # Send email
    msg.send(fail_silently=False)
    print(f"[DEBUG] Email sent to {recipient_email} | PDF: {pdf_path} | ICS: {ics_path}")