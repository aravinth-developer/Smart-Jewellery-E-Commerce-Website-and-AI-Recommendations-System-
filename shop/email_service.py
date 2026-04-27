from django.core.mail import send_mail
from django.conf import settings

def send_recommendation_email(user,products):

    product_text="\n".join(
        [f"{p.name} - ₹{p.price_add_wastage}" for p in products]
    )

    message=f"""
Hello {user.username} 💎

Based on your interest we recommend:

{product_text}

Visit our jewellery store now!
"""

    send_mail(
        subject="AI Jewellery Recommendations 💎",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )