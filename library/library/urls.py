from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('authors/', include('author.urls')),
    path('orders/', include('order.urls')),
    path('api/', include('api_urls')),
    path('', include('book.urls')),
]