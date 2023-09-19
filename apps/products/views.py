from django.core.cache import cache
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (BasePermission, AllowAny, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.viewsets import (ModelViewSet)

from rest_framework.generics import (ListCreateAPIView, RetrieveAPIView, get_object_or_404, CreateAPIView, ListAPIView)
from apps.products.models import (Product, Category, Wishlist, Order, ViewedProduct, Comment, Rating, Basket)
from apps.products.serializers import (ProductModelSerializer, CategoryModelSerializer, WishListModelSerializer,
                                       OrderModelSerializer, ViewedProductSerializer, SearchModelSerializer,
                                       CommentModelSerializer, RatingModelSerializer, BasketModelSerializer)


# Permission
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user and request.user.is_staff


# Product
class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]

    # Popular product
    @action(detail=True, methods=['GET'])
    def popular_product(self, request, pk=None):
        popular_products = Product.objects.order_by('-popularity_score')[:10]  # Get top 10 products by popularity score
        serializer = ProductModelSerializer(popular_products, many=True)
        return Response(serializer.data)

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

    # cache
    def list(self, request, *args, **kwargs):
        if cache.get('data') is None:
            cache.set('data', self.get_queryset(), timeout=60)
            return Response(self.get_serializer(self.get_queryset(), many=True).data)
        else:
            return Response(self.get_serializer(cache.get('data'), many=True).data)

    # discount products
    @action(detail=True, methods=['post'])
    def discount(self, request, pk=None):
        product = self.get_object()
        discount_percentage = request.data.get('discount_percentage')
        if discount_percentage is not None:
            product.price -= (product.price * (discount_percentage / 100))
            product.save()
            return Response({'message': 'Discount applied successfully.'})
        else:
            return Response({'error': 'Please provide a valid discount percentage.'},
                            status=status.HTTP_400_BAD_REQUEST)


class ProductDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    # filter_backends = [DjangoFilterBackend]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['option__color', 'price']
    permission_classes = [IsAdminOrReadOnly]

    # view
    def retrieve(self, request, *args, **kwargs):
        self.get_queryset()
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = ProductModelSerializer(instance)
        return Response(serializer.data)


# Category
class CategoryCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAdminOrReadOnly]


# WishList
class WishListModelViewSet(ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishListModelSerializer
    permission_classes = [AllowAny]

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


# Order
class OrderCreateView(CreateAPIView):
    serializer_class = OrderModelSerializer
    queryset = Order.objects.all()


# Basket
class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketModelSerializer


# Rating
class RatingCreateView(ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingModelSerializer


# Search
class ProductSearchAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = SearchModelSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
    permission_classes = [AllowAny]


# Comment
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer
    permission_classes = [IsAuthenticated]
