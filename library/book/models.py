from django.db import models
from author.models import Author  # Підключаємо модель Автора

class Book(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    count = models.IntegerField(default=10)
    # Зв'язок багато-до-багатьох з моделлю Author
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        authors_list = ", ".join([f"{a.name} {a.surname}" for a in self.authors.all()])
        return f"{self.id}, {self.name}, {self.description}, {self.count}, [{authors_list}]"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    @staticmethod
    def get_by_id(book_id):
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(book_id):
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            return True
        except Book.DoesNotExist:
            return False

    @staticmethod
    def create(name, description, count=10, authors=None):
        book = Book(name=name, description=description, count=count)
        book.save()
        if authors:
            book.authors.set(authors)  # Додаємо авторів після збереження книги
        return book

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'authors': [author.id for author in self.authors.all()]
        }

    def update(self, name=None, description=None, count=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if count is not None:
            self.count = count
        self.save()

    def add_authors(self, authors):
        if authors:
            self.authors.add(*authors)

    def remove_authors(self, authors):
        if authors:
            self.authors.remove(*authors)

    @staticmethod
    def get_all():
        return Book.objects.all()