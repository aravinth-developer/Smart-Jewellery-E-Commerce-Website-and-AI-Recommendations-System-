from shop.ai_recommendation import get_ai_recommendations
from shop.email_service import send_recommendation_email
from shop.sms_service import send_sms

def send_ai_recommendations(user):

    products=get_ai_recommendations(user)

    text="\n".join(
        [f"{p.name} - ₹{p.price_add_wastage}" for p in products]
    )

    sms_message=f"""
Hi {user.username} 💎
Recommended Jewellery:

{text}
"""

    send_recommendation_email(user,products)
    send_sms(user.phone,sms_message)