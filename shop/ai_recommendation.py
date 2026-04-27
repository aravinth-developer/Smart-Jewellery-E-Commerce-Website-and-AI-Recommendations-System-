import time
from google import genai
from django.conf import settings
from django.core.cache import cache
from shop.models import Product, SearchHistory, CartHistory, FavoriteHistory, OrderItem

client = genai.Client(api_key=settings.GEMINI_RECOMMEND_KEY)

def get_ai_recommendations(user):

    # 🔹 1. Check cache first
    cache_key = f"ai_recommend_{user.id}"
    cached = cache.get(cache_key)

    if cached:
        return cached

    # 🔹 2. Collect user behaviour
    searches = list(SearchHistory.objects.filter(user=user).values_list("query", flat=True)[:5])
    cart = list(CartHistory.objects.filter(user=user).values_list("product__name", flat=True)[:5])
    fav = list(FavoriteHistory.objects.filter(user=user).values_list("product__name", flat=True)[:5])
    orders = list(OrderItem.objects.filter(order__user=user).values_list("product__name", flat=True)[:5])

    # 🔹 3. Limit products sent to AI
    products = list(Product.objects.values_list("name", flat=True)[:50])

    prompt = f"""
User search history: {searches}
Cart items: {cart}
Favourite items: {fav}
Order history: {orders}

Available jewellery products: {products}

Recommend 5 jewellery products the user will like.
Return ONLY product names exactly as given.
Do not number them.
One product per line.
"""

    retries = 3

    for attempt in range(retries):
        try:

            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )

            text = response.text.strip()

            names = [n.strip().replace("•", "").replace("-", "") for n in text.split("\n")]

            result = Product.objects.filter(name__in=names)

            # 🔹 4. Save result in cache for 10 minutes
            cache.set(cache_key, result, 600)

            return result

        except Exception as e:
            print("Gemini Retry Error:", e)
            time.sleep(2)

    # 🔹 5. Fallback if AI fails
    result = Product.objects.all()[:4]
    cache.set(cache_key, result, 600)

    return result