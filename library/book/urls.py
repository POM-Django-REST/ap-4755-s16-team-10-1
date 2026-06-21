from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list_view, name='book_list'),
    path('<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('add/', views.add_book_view, name='add_book'),
    path('delete/<int:book_id>/', views.delete_book_view, name='delete_book'),
]