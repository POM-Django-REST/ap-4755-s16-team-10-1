from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    # Явно вказуємо, що пароль має бути прихованим інпутом
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'middle_name', 'role']

    # Перевизначаємо метод save, щоб пароль безпечно хешувався
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user