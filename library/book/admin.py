from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Використовуємо кастомний метод display_authors замість прямого виклику 'authors'
    list_display = ('id', 'name', 'count', 'display_authors') 
    
    # Фільтрація збоку
    list_filter = ('authors',)
    
    # Пошук за ID, назвою книги та ім'ям/прізвищем автора
    search_fields = ('id', 'name', 'authors__name', 'authors__surname')

    # Розбиття на секції
    fieldsets = (
        ('Static Data (Do not change)', {
            'fields': ('name', 'description')
        }),
        ('Dynamic Data (Change)', {
            'fields': ('count', 'authors')
        }),
    )

    # Функція для коректного відображення авторів (ManyToManyField) у списку
    def display_authors(self, obj):
        return ", ".join([f"{a.name} {a.surname}" for a in obj.authors.all()])
    
    # Назва колонки в адмінці
    display_authors.short_description = 'Authors'