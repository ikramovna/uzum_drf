from rest_framework.serializers import ModelSerializer

from apps.products.models import Product, ProductImage, Category, Wishlist, Order, ViewedProduct, Comment, Rating, \
    Basket


class ProductImageModelSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductModelSerializer(ModelSerializer):
    images = ProductImageModelSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class WishListModelSerializer(ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        exclude = ('id',)


class ViewedProductSerializer(ModelSerializer):
    class Meta:
        model = ViewedProduct
        exclude = ()


class SearchModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'short_description')


class CommentModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ()


class RatingModelSerializer(ModelSerializer):
    class Meta:
        model = Rating
        exclude = ()


class BasketModelSerializer(ModelSerializer):
    class Meta:
        model = Basket
        exclude = ()
