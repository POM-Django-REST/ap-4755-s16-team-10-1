from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'admin'),
)

class CustomUserManager(BaseUserManager):
    """
    Стандартний менеджер користувачів для коректної роботи AbstractBaseUser
    (потрібен для таких речей як createsuperuser в терміналі)
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 1)
        # Додаємо прапорці для адмінки при створенні суперюзера
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    """
        This class represents a basic user. \n
        Attributes:
        -----------
        param first_name: Describes first name of the user
        type first_name: str max length=20
        param last_name: Describes last name of the user
        type last_name: str max length=20
        param middle_name: Describes middle name of the user
        type middle_name: str max length=20
        param email: Describes the email of the user
        type email: str, unique, max length=100
        param password: Describes the password of the user
        type password: str
        param created_at: Describes the date when the user was created. Can't be changed.
        type created_at: int (timestamp)
        param updated_at: Describes the date when the user was modified
        type updated_at: int (timestamp)
        param role: user role, default role (0, 'visitor')
        type updated_at: int (choices)
        param is_active: user role, default value False
        type updated_at: bool
    """
    
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    # Поле password вже наслідується від AbstractBaseUser
    
    # Використовуємо DateTimeField, а в to_dict будемо перетворювати в int(timestamp)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=False)
    
    # Додані поля для роботи Django Admin
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """
        Magic method is redefined to show all information about CustomUser.
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user password, user updated_at, user created_at,
                 user role, user is_active
        """
        return f"{self.id}, {self.first_name}, {self.middle_name}, {self.last_name}, " \
               f"{self.email}, {self.password}, {self.updated_at}, {self.created_at}, " \
               f"{self.role}, {self.is_active}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of CustomUser object.
        :return: class, id
        """
        return f"{self.__class__.__name__}(id={self.id})"

    # --- Обов'язкові методи для адмінки Django ---
    def has_perm(self, perm, obj=None):
        """Чи має користувач певний дозвіл? (Суперюзери мають усі дозволи)"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Чи має користувач дозволи на перегляд додатку в адмінці?"""
        return self.is_superuser
    # ----------------------------------------------

    @staticmethod
    def get_by_id(user_id):
        """
        :param user_id: SERIAL: the id of a user to be found in the DB
        :return: user object or None if a user with such ID does not exist
        """
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_by_email(email):
        """
        Returns user by email
        :param email: email by which we need to find the user
        :type email: str
        :return: user object or None if a user with such ID does not exist
        """
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(user_id):
        """
        :param user_id: an id of a user to be deleted
        :type user_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return True
        except CustomUser.DoesNotExist:
            return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        """
        :param first_name: first name of a user
        :type first_name: str
        :param middle_name: middle name of a user
        :type middle_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param email: email of a user
        :type email: str
        :param password: password of a user
        :type password: str
        :return: a new user object which is also written into the DB
        """
        user = CustomUser(
            email=email,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name
        )
        user.set_password(password)  # Безпечне хешування пароля
        user.save()
        return user

    def to_dict(self):
        """
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user password, user updated_at, user created_at, user is_active
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'updated_at': int(self.updated_at.timestamp()) if self.updated_at else None,
            'role': self.role,
            'is_active': self.is_active
        }

    def update(self,
               first_name=None,
               last_name=None,
               middle_name=None,
               password=None,
               role=None,
               is_active=None):
        """
        Updates user profile in the database with the specified parameters.\n
        :param first_name: first name of a user
        :type first_name: str
        :param middle_name: middle name of a user
        :type middle_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param password: password of a user
        :type password: str
        :param role: role id
        :type role: int
        :param is_active: activation state
        :type is_active: bool
        :return: None
        """
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if middle_name is not None:
            self.middle_name = middle_name
        if password is not None:
            self.set_password(password)  # Оновлюємо безпечно
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active
            
        self.save()

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all users
        """
        return CustomUser.objects.all()

    def get_role_name(self):
        """
        returns str role name
        """
        return dict(ROLE_CHOICES).get(self.role)