from modeltranslation.translator import register, TranslationOptions

from apps.products.models import Category, Product


@register(Category)
class CategoryTranslationOption(TranslationOptions):
    fields = ('name',)


@register(Product)
class ProductTranslationOption(TranslationOptions):
    fields = ('title', 'long_description', 'short_description')
