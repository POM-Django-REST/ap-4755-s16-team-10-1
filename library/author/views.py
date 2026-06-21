from django.shortcuts import render, redirect
from .models import Author
from .forms import AuthorForm

def author_list_view(request):
    if not request.user.is_authenticated or request.user.role != 1:
        return redirect('/') 

    error_message = None
    form = AuthorForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            form = AuthorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('authors')

        elif action == 'delete':
            author_id = request.POST.get('author_id')
            author = Author.get_by_id(author_id)
            
            if author:
                try:
                    if author.book_set.count() > 0:
                        error_message = f"Не можна видалити автора {author.surname}, бо у нього є книги!"
                    else:
                        Author.delete_by_id(author_id)
                except Exception:
                    Author.delete_by_id(author_id)
            
            if not error_message:
                return redirect('authors')

    authors = Author.get_all()
    return render(request, 'author/author_list.html', {'authors': authors, 'error': error_message, 'form': form})