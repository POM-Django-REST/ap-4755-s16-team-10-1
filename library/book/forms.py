from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'authors': forms.SelectMultiple(), 
        }