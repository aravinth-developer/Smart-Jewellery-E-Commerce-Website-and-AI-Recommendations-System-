from django.contrib import admin
from .models import *   


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description')

class MarketRateAdmin(admin.ModelAdmin):
    list_display = ('gold_price', 'silver_price', 'created_at')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "quantity",
        "price",
        "total",
        "customer_name",
        "customer_address",
        "payment_status",
    )

    def customer_name(self, obj):
        return obj.order.full_name

    def customer_address(self, obj):
        return obj.order.address


    

admin.site.register(Catagory, CategoryAdmin)
admin.site.register(Product)
admin.site.register(MarketRate, MarketRateAdmin)
admin.site.register(OrderItem, OrderItemAdmin)