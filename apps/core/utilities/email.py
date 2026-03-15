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
        "https://res.cloudinary.com/dcfkxity4/image/upload/v1773589515/WhatsApp_Image_2026-03-15_at_8.57.47_PM_pjdlye.jpg"
    )
    context.setdefault("company_name", "Curexa Healthtech")
    context.setdefault("company_address", "Cooch Behar, West Bengal")
    context.setdefault("social_icons", [
        {
            "url": "www.linkedin.com/in/parthapratimsutradhar",
            "img": "https://res.cloudinary.com/dcfkxity4/image/upload/v1773589937/linkedin_p4zry0.png",
            "alt": "LinkedIn"
        },
        {
            "url": "https://x.com/Partha_Pratim_S",
            "img": "https://res.cloudinary.com/dcfkxity4/image/upload/v1773590138/x_hrezs4.png",
            "alt": "X"
        },
        {
            "url": "https://www.instagram.com/iamparthasutradhar/",
            "img": "https://res.cloudinary.com/dcfkxity4/image/upload/v1773589060/instagram_usvlf7.png",
            "alt": "Instagram"
        },
        {
            "url": "https://www.facebook.com/iamparthasutradhar/",
            "img": "https://res.cloudinary.com/dcfkxity4/image/upload/v1773588729/facebook_iyi6cn.png",
            "alt": "Facebook"
        },
        {
            "url": "https://github.com/parthapratimsutradhar",
            "img": "https://res.cloudinary.com/dcfkxity4/image/upload/v1773588792/github_dcqb3m.png",
            "alt": "Github"
        }
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