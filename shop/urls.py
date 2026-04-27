from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('home',views.home,name="home"),
    path('register',views.register,name="register"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('cart',views.cart_page,name="cart"),
    path('fav',views.fav_page,name="fav"),
    path('favviewpage',views.favviewpage,name="favviewpage"),
    path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('collections',views.collections,name="collections"),
    path('collections/<str:name>',views.collectionsview,name="collections"),
    path('collections/<str:cname>/<str:pname>',views.product_details,name="product_details"),
    path('addtocart',views.add_to_cart,name="addtocart"),
    path('order-summary/', views.order_summary, name='order_summary'),
    path('order-summary/<int:cart_id>/', views.order_summary, name='order_summary'),
    path('my-orders', views.my_orders, name="my_orders"),
    path("chatbot-api/", views.chatbot_api, name="chatbot_api"),
    path("services/", views.services, name="services"),
    path("wastage-prediction/", views.wastage_prediction, name="wastage_prediction"),
    path('search/', views.product_search, name='product_search'),
    path('multi-order-summary/', views.multi_order_summary, name='multi_order_summary'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='shop/password_reset.html'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='shop/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='shop/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='shop/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('get-market-rates/', views.get_market_rates, name='get_market_rates'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('faq/', views.faq_page, name='faq'),

    path("gold-chart/", views.gold_price_chart, name="gold_chart"),
]
