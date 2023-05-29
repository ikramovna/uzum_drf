from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, RetrieveAPIView, get_object_or_404)
from rest_framework.response import Response
from rest_framework.viewsets import (ModelViewSet)

from apps.products.models import (Product, Category, Wishlist)
from apps.products.serializers import (ProductModelSerializer, CategoryModelSerializer, WishListModelSerializer)


# Product
class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


class ProductDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


# Category
class CategoryCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


# WishList
class WishListModelViewSet(ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishListModelSerializer



