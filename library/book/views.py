from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from author.models import Author
from .forms import BookForm

def book_list_view(request):
    books = Book.get_all()
    search_query = request.GET.get('search', '')
    if search_query:
        books = books.filter(name__icontains=search_query)

    return render(request, 'book/book_list.html', {'books': books, 'search_query': search_query})

def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book/book_detail.html', {'book': book})

def add_book_view(request):
    if request.user.role != 1: return redirect('/')
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'book/add_book.html', {'form': form})

def delete_book_view(request, book_id):
    if request.user.role == 1:
        if request.method == 'POST':
            Book.delete_by_id(book_id)
    return redirect('book_list')