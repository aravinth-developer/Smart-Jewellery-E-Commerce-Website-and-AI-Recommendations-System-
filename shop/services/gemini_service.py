from google import genai # Note the change here
from django.conf import settings
from shop.models import Product

# ✅ Gold Rate Function (you can later connect real API)
def get_gold_rate():
    # Dummy rate (you can replace with live API)
    return "₹14560 Gold per gram (22K)" \
           "₹270 Silver per gram (925)"


def generate_response(user_message):
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        user_message_lower = user_message.lower()

        # ✅ 1. If user asks gold rate
        if "gold rate" in user_message_lower or "today gold" in user_message_lower:
            return f"Today's gold rate is {get_gold_rate()} 💰"

        # ✅ 2. If user asking about product types
        keywords = ["ring", "necklace", "chain", "bracelet", "earring"]
        matched_products = []

        for word in keywords:
            if word in user_message_lower:
                matched_products = Product.objects.filter(name__icontains=word)[:5]
                break

        product_text = ""
        if matched_products:
            product_text = "\n".join(
                [f"{p.name} - ₹{p.price_add_wastage}" for p in matched_products]
            )

        prompt = f"""
You are Selvi, a professional jewellery AI assistant.
Only show products if user is asking about jewellery items.
If question is general, respond normally without listing products.

Available matching products:
{product_text}

Customer Question:
{user_message}
"""

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return "Sorry, I’m facing technical issues. Please try again later."
