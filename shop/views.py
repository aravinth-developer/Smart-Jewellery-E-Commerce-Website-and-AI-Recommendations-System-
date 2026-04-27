from django.http import JsonResponse
from django.shortcuts import render, redirect
from shop.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .services.gemini_service import generate_response
import joblib
import os
from .models import WastagePrediction
from google import genai
from django.db.models import Q
from django.utils import timezone
from shop.recommendation_service import send_ai_recommendations
from shop.ai_recommendation import get_ai_recommendations
import urllib.parse
from django.shortcuts import redirect

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})

def favviewpage(request):
   if request.user.is_authenticated:
      fav=Favourite.objects.filter(user=request.user)
      return render(request,"shop/fav.html",{"fav":fav})
   else:
      return redirect("/home")
   
def remove_fav(request,fid):
   item=Favourite.objects.get(id=fid)
   item.delete()
   return redirect("/favviewpage")
   

def cart_page(request):
   if request.user.is_authenticated:
      cart=Cart.objects.filter(user=request.user)
      return render(request,"shop/cart.html",{"cart":cart})
   else:
      return redirect("/home")

def remove_cart(request,cid):
   cartitem=Cart.objects.get(id=cid)
   cartitem.delete()
   return redirect("/cart")

def fav_page(request):

    if request.method == "POST":

        if request.user.is_authenticated:

            data = json.loads(request.body)
            product_id = data.get('pid')

            try:
                product_status = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({'status': 'Product Not Found'})

            if Favourite.objects.filter(user=request.user, product_id=product_id).exists():
                return JsonResponse({'status': 'Product Already in Favourite'})
            else:

                Favourite.objects.create(user=request.user, product_id=product_id)

                # ⭐ Save Favourite History
                FavoriteHistory.objects.create(
                    user=request.user,
                    product_id=product_id
                )

                return JsonResponse({'status': 'Product Added to Favourite'})

        else:
            return JsonResponse({'status': 'Login to Add Favourite'})

    return JsonResponse({'status': 'Invalid Access'})



def add_to_cart(request):

    if request.method == "POST":

        if request.user.is_authenticated:

            data = json.loads(request.body)
            product_qty = int(data.get('product_qty'))
            product_id = data.get('pid')

            try:
                product_status = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({'status': 'Product Not Found'})

            if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                return JsonResponse({'status': 'Product Already in Cart'})

            if product_status.quantity >= product_qty:

                Cart.objects.create(
                    user=request.user,
                    product_id=product_id,
                    product_qty=product_qty
                )

                # ⭐ Save Cart History
                CartHistory.objects.create(
                    user=request.user,
                    product_id=product_id
                )

                return JsonResponse({'status': 'Product Added to Cart'})

            else:
                return JsonResponse({'status': 'Product Stock Not Available'})

        else:
            return JsonResponse({'status': 'Login to Add Cart'})

    return JsonResponse({'status': 'Invalid Access'})


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Loggged Out Successfully")
    return redirect("/home")    

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/home")

    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=name, password=pwd)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect("/home")
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect("/login")

    return render(request, "shop/login.html")

def register(request):
    if request.user.is_authenticated:
        return redirect("/home")   # Prevent logged-in users from accessing register

    form = CustomUserForm()

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Success! You Can Login Now.")
            return redirect("/login")

    return render(request, "shop/register.html", {'form': form})

def collections(request):
    catagory=Catagory.objects.all()
    return render(request,"shop/collections.html",{"catagory":catagory})

def collectionsview(request, name):
    category = Catagory.objects.filter(name=name, status=False).first()

    if category:
        products = Product.objects.filter(Catagory=category)
        return render(
            request,
            "shop/products/index.html",
            {
                "products": products,
                "category_name": category.name
            }
        )
    else:
        messages.warning(request, "No Such Category Found")
        return redirect('collections')

def product_details(request, cname, pname):

    category = Catagory.objects.filter(name=cname, status=False).first()

    if not category:
        messages.error(request, "No Such Category Found")
        return redirect('collections')

    product = Product.objects.filter(
        Catagory=category,
        name=pname,
        status='available'
    ).first()

    if not product:
        messages.error(request, "No Such Product Found")
        return redirect('collections')

    return render(
        request,
        "shop/products/product_details.html",
        {"products": product}
    )


from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Cart, Order, OrderItem


def order_summary(request, cart_id=None):

    if not request.user.is_authenticated:
        return redirect("login")

    # 🔹 SINGLE PRODUCT CHECKOUT
    if cart_id:
        cart_items = Cart.objects.filter(id=cart_id, user=request.user)

    # 🔹 MULTI PRODUCT CHECKOUT (from session)
    else:
        selected_ids = request.session.get('selected_cart_ids', [])
        cart_items = Cart.objects.filter(id__in=selected_ids, user=request.user)

    if not cart_items.exists():
        messages.error(request, "No Items Selected")
        return redirect("cart")

    total = sum(item.total_cost for item in cart_items)

    if request.method == "POST":

        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            country=request.POST.get("country"),
            total_amount=total,
        )

        # ✅ SAVE ORDER ITEMS BEFORE DELETING CART
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.product_qty,
                price=item.product.price_add_wastage,
                total=item.total_cost,
                ordered_date=timezone.now(),
                payment_status="Confirmed"
            )

        # ✅ DELETE CART ITEMS
        cart_items.delete()

        # ✅ CLEAR SESSION
        request.session['selected_cart_ids'] = []

        messages.success(request, "Order Placed Successfully!")
        return redirect("my_orders")

    return render(request, "shop/order_summary.html", {
        "cart_items": cart_items,
        "total": total
    })

def my_orders(request):
    if not request.user.is_authenticated:
        return redirect("login")

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # 🧠 AI Recommendations
    recommendations = get_ai_recommendations(request.user)

    context = {
        "orders": orders,
        "recommendations": recommendations
    }

    return render(request, "shop/my_orders.html", context)


@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')

        reply = generate_response(message)

        return JsonResponse({'reply': reply})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def services(request):
    return render(request, "shop/services.html")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "shop", "ml_model", "wastage_model.pkl")
data = joblib.load(model_path)

model = data["model"]
le_jewel = data["le_jewel"]
le_design = data["le_design"]
le_stone = data["le_stone"]

def wastage_prediction(request):
    result = None

    if request.method == "POST":
        jewel = request.POST["jewel"]
        karat = int(request.POST["karat"])
        design = request.POST["design"]
        stone = request.POST["stone"]
        gold = float(request.POST["gold"])
        final = float(request.POST["final"])

        weight_diff = gold - final

        jewel_enc = le_jewel.transform([jewel])[0]
        design_enc = le_design.transform([design])[0]
        stone_enc = le_stone.transform([stone])[0]

        prediction = model.predict([[
            jewel_enc,
            karat,
            design_enc,
            stone_enc,
            gold,
            final,
            weight_diff
        ]])

        result = round(prediction[0], 2)

        WastagePrediction.objects.create(
            jewel_type=jewel,
            karat=karat,
            design_type=design,
            stone_included=(stone == "Yes"),
            gold_given_weight=gold,
            final_weight=final,
            predicted_wastage=result
        )

    return render(request, "shop/wastage_prediction.html", {"result": result})


def product_search(request):

    query = request.GET.get('q')
    products = []

    if query:

        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

        # ⭐ Save search history
        if request.user.is_authenticated:
            SearchHistory.objects.create(
                user=request.user,
                query=query
            )

    return render(request, "shop/search_results.html", {
        "query": query,
        "products": products
    })


def multi_order_summary(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        selected_ids = request.POST.getlist('cart_ids')

        if not selected_ids:
            messages.error(request, "Please select at least one item.")
            return redirect("cart")

        # ✅ STORE IDS IN SESSION
        request.session['selected_cart_ids'] = selected_ids

        return redirect("order_summary")

    return redirect("cart")

def get_market_rates(request):
    rate = MarketRate.objects.first()

    if rate:
        data = {
            "gold": rate.gold_price,
            "silver": rate.silver_price
        }
    else:
        data = {
            "gold": 0,
            "silver": 0
        }

    return JsonResponse(data)



def place_order(request):

    if request.method == "POST":

        order = Order.objects.create(
            user=request.user,
            total_price=item.product.price_add_wastage
        )

        cart_items = Cart.objects.filter(user=request.user)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        cart_items.delete()

        # 🔹 AI Recommendation Trigger
        send_ai_recommendations(request.user)

        return redirect("my_orders")


def about_page(request):
    return render(request, "shop/about.html")

def contact_page(request):
    return render(request, "shop/contact.html")

def faq_page(request):
    return render(request, "shop/faq.html")


def gold_price_chart(request):

    rates = MarketRate.objects.order_by('-created_at')[:7]
    rates = list(rates)[::-1]   # reverse order

    labels = []
    prices = []

    for r in rates:
        labels.append(r.created_at.strftime("%a"))
        prices.append(r.gold_price)

    return JsonResponse({
        "labels": labels,
        "prices": prices
    })