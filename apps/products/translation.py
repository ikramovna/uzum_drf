from modeltranslation.translator import register, TranslationOptions

from apps.products.models import Category, Product


@register(Category)
class NewTranslationOption(TranslationOptions):
    fields = ('name',)


@register(Product)
class NewTranslationOption(TranslationOptions):
    fields = ('title', 'long_description', 'short_description')
