from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductModelViewSet, CategoryCreateAPIView, ProductDetailRetrieveAPIView, WishListModelViewSet, \
    OrderCreateView, CommentViewSet, ProductSearchAPIView, RatingCreateView, BasketModelViewSet

routers = DefaultRouter()
routers.register('product', ProductModelViewSet, '')
routers.register('wishlist', WishListModelViewSet, '')
routers.register('comment', CommentViewSet, 'comments')
routers.register('baskets', BasketModelViewSet, 'baskets')
urlpatterns = [
    path('', include(routers.urls)),
    path('category/<int:pk>', CategoryCreateAPIView.as_view()),
    path('product_detail/<int:pk>', ProductDetailRetrieveAPIView.as_view()),
    path('order', OrderCreateView.as_view()),
    path('search', ProductSearchAPIView.as_view()),
    path('ratings', RatingCreateView.as_view()),
]
