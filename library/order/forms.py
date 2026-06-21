from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # Поле end_at зазвичай ставиться автоматично при здачі книги, тому його не додаємо при створенні
        fields = ['user', 'book', 'plated_end_at']
        widgets = {
            # Використовуємо HTML5 інпут для вибору дати та часу
            'plated_end_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }