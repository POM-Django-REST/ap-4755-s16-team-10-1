from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class UserOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    # Повертаємо замовлення тільки конкретного юзера
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(user_id=user_id)