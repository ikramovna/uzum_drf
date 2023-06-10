from django.contrib.auth.models import User
from django.db.models import Model, CharField, IntegerField, TextField, ForeignKey, CASCADE, ImageField, DateTimeField, \
    Index, PositiveIntegerField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    name = CharField(max_length=150)
    parent = TreeForeignKey('self', CASCADE, 'children', null=True, blank=True)

    class Meta:
        indexes = [
            Index(fields=['name'])
        ]

    def __str__(self):
        return self.name


class ProductImage(Model):
    image = ImageField(upload_to='products/images/')
    products = ForeignKey('Product', CASCADE)

    def __str__(self):
        return self.products.title


class Product(Model):
    title = CharField(max_length=150)
    price = IntegerField()
    short_description = TextField(blank=True, null=True)
    long_description = TextField(blank=True, null=True)
    discount = IntegerField(null=True, blank=True)
    quantity = IntegerField()
    created_at = DateTimeField(auto_now_add=True)
    views = IntegerField(default=0)
    category = ForeignKey('Category', CASCADE)
    owner = ForeignKey('auth.User', CASCADE)

    class Meta:
        indexes = [
            Index(fields=['title', 'long_description', 'short_description'])
        ]

    @property
    def discount_price(self):
        return self.price - self.price * self.discount // 100


class Wishlist(Model):
    product = ForeignKey('Product', CASCADE)
    user = ForeignKey('auth.User', CASCADE)
    created_at = DateTimeField(auto_now=True)


class Order(Model):
    user = ForeignKey('auth.User', CASCADE)
    product = ForeignKey(Product, CASCADE, 'order')
    quantity = IntegerField(default=1)


class Basket(Model):
    product = ForeignKey(Product, CASCADE, 'baskets')
    quantity = IntegerField(default=1)
    user = ForeignKey('auth.User', on_delete=CASCADE)

    def __str__(self):
        return self.product


class City(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class ViewedProduct(Model):
    user = ForeignKey('auth.User', CASCADE)
    product = ForeignKey('Product', CASCADE)
    timestamp = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Comment(Model):
    name = CharField(max_length=100)
    rate = ForeignKey('Rating', CASCADE)
    description = TextField()
    image = ImageField(upload_to='comments/images/')

    def __str__(self):
        return self.name


class Rating(Model):
    user = ForeignKey('auth.User', CASCADE)
    product = ForeignKey('Product', CASCADE)
    rating = PositiveIntegerField()
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user



