from django.contrib import admin

from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'updated']
    list_filter = ['available', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'paid', 'created']
    list_filter = ['paid', 'created']
    inlines = [OrderItemInline]
