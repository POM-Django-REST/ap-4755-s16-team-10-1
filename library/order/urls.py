from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list_view, name='order_list'),
    path('create/<int:book_id>/', views.create_order_view, name='create_order'), # <--- Саме цей рядок шукає Django!
    path('close/<int:order_id>/', views.close_order_view, name='close_order'),
]