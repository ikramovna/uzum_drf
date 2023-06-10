from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import (ListCreateAPIView, RetrieveAPIView, get_object_or_404, CreateAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import (ModelViewSet)

from apps.products.models import (Product, Category, Wishlist, Order, ViewedProduct)
from apps.products.serializers import (ProductModelSerializer, CategoryModelSerializer, WishListModelSerializer,
                                       OrderModelSerializer, ViewedProductSerializer)


# Product
class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    pagination_class = PageNumberPagination

    # Similar products
    @action(detail=True, methods=['GET'])
    def similar_products(self, request, pk=None):
        product = self.get_object()
        similar_products = Product.objects.filter(category=product.category)[:5]
        serializer = ProductModelSerializer(similar_products, many=True)
        return Response(serializer.data)

    # Products viewed
    @action(detail=True, methods=['POST'])
    def mark_viewed(self, request, pk=None):
        product = self.get_object()

        user = request.user

        viewed_product = ViewedProduct(user=user, product=product)
        viewed_product.save()

        serializer = ViewedProductSerializer(viewed_product)
        return Response(serializer.data)

    # discount
    @action(detail=True, methods=['POST'])
    def add_discount(self, request, pk=None):
        product = self.get_object()
        discount = request.data.get('discount')

        product.price -= discount
        product.save()

        serializer = self.get_serializer(product)
        return Response(serializer.data)

    # cache
    def list(self, request, *args, **kwargs):
        if cache.get('data') is None:
            cache.set('data', self.get_queryset(), timeout=60)
            return Response(self.get_serializer(self.get_queryset(), many=True).data)
        else:
            return Response(self.get_serializer(cache.get('data'), many=True).data)


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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(product_id=kwargs.get('pk'), user=request.user)
        instance = get_object_or_404(queryset)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class OrderCreateView(CreateAPIView):
    serializer_class = OrderModelSerializer
    queryset = Order.objects.all()




