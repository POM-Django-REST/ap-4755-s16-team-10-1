from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Order
from book.models import Book
from .forms import OrderForm

def order_list_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.role == 1:
        orders = Order.get_all()
    else:
        orders = Order.objects.filter(user=request.user)
    
    return render(request, 'order/order_list.html', {'orders': orders})

def close_order_view(request, order_id):
    if request.user.role == 1:
        order = Order.get_by_id(order_id)
        if order and not order.end_at:
            order.update(end_at=timezone.now())
            
            book = order.book
            book.count += 1
            book.save()
            
    return redirect('order_list')

def create_order_view(request, book_id=None):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            
            book = order.book
            book.count -= 1
            book.save()
            
            return redirect('order_list')
    else:
        initial_data = {
            'user': request.user,
            'plated_end_at': timezone.now() + timedelta(days=14)
        }
        if book_id:
            initial_data['book'] = get_object_or_404(Book, id=book_id)
            
        form = OrderForm(initial=initial_data)

    return render(request, 'order/create_order.html', {'form': form})