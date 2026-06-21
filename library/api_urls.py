from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authentication.api_views import UserViewSet
from author.api_views import AuthorViewSet
from book.api_views import BookViewSet
from order.api_views import OrderViewSet, UserOrderViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'author', AuthorViewSet, basename='author')
router.register(r'book', BookViewSet, basename='book')
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path('v1/', include(router.urls)),
    
    # Кастомний шлях для замовлень конкретного юзера: api/v1/user/{id}/order/{id}
    path('v1/user/<int:user_id>/order/', UserOrderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('v1/user/<int:user_id>/order/<int:pk>/', UserOrderViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    })),
]