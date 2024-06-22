from django.contrib import admin
from .models import Customer, Product, category_master, Cart, OrderPlaced


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'phone', 'locality', 'city')


@admin.register(category_master)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_name', 'status', 'create_date', 'image')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'selling_price', 'discounted_price', 'category', 'brand')


@admin.register(OrderPlaced)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer', 'product', 'quantity', 'ordered_date', 'status')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')
