from django.contrib import admin

from apps.products.models import ProductImage, Product, Category, Wishlist, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')


admin.site.register(Product, ProductAdmin)


class WishListAdmin(admin.ModelAdmin):
    list_display = ('product',)


admin.site.register(Wishlist, WishListAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


admin.site.register(Category, CategoryAdmin)


# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ['image', 'product']
#
#
# admin.site.register(ProductImage, ProductImageAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')


admin.site.register(Order, OrderAdmin)
