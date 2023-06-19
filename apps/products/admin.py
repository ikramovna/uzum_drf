from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.products.models import Category, Product, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Comment, CommentAdmin)


@admin.register(Category)
class NewAdmin(TranslationAdmin):
    pass


@admin.register(Product)
class NewAdmin(TranslationAdmin):
    pass
