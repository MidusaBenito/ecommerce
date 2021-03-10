from django.contrib import admin

# Register your models here.
from .models import *
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'phone']
@admin.register(Sandle)
class SandleAdmin(admin.ModelAdmin):
    list_display = ['name','category', 'image', 'price', 'digital']
    list_filter = ['created', 'updated', 'category']
    prepopulated_fields = {'slug': ('name',)}
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date_ordered', 'complete', 'transaction_id']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display =['size']
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['sandle', 'order','size', 'quantity', 'date_added']
@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order', 'county', 'town', 'address','transaction_id', 'date_added']
