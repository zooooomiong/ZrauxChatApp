# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
# from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import random 


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('confirm_email', True)

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    confirm_email = models.BooleanField(default=False)
    confirm_code = models.CharField(max_length=6, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Use custom related_name to avoid clash with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = "user"

    @property
    def make_random_code(self):
        return str(random.randint(100000, 999999)) 

    def create_code(self):
        self.confirm_code = self.make_random_code
        self.save()



# class UserCustomManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name, password, **extra_fields):
#         if email:
#             email = self.normalize_email(email)
#             try:
#                 validate_email(email)
#             except ValidationError:
#                 raise ValueError(_("Please enter a valid email address"))
#         else:
#             raise ValueError(_("Please enter an email address"))
        
#         if not first_name:
#             raise ValueError(_("First name is required"))
#         if not last_name:
#             raise ValueError(_("Last name is required"))

#         user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, first_name, last_name, password, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("email_verified", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError(_("Superuser must have is_superuser=True."))
#         if extra_fields.get("is_staff") is not True:
#             raise ValueError(_("Superuser must have is_staff=True."))
#         if extra_fields.get("email_verified") is not True:
#             raise ValueError(_("Superuser must have email_verified=True."))

#         return self.create_user(email=email, first_name=first_name, last_name=last_name, password=password, **extra_fields)


# def make_username():
#     import uuid
#     import hashlib
#     import random
#     h = hashlib.sha256()
#     h.update(str(uuid.uuid4()).encode())
#     h.update(str(random.random()).encode())
#     return h.hexdigest()


# class User(AbstractUser):
#     username = models.CharField(max_length=64, default=make_username, unique=True)
#     email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
#     first_name = models.CharField(_("First Name"), default="", max_length=128)
#     last_name = models.CharField(_("Last Name"), default="", max_length=128)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     email_verified = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now=True)

    
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["first_name", "last_name"]
#     objects = UserCustomManager()

#     class Meta:
#         db_table = "user"
#         verbose_name = _("User")
#         verbose_name_plural = _("Users")

#     def __str__(self):
#         return self.email

#     @property
#     def full_name(self):
#         return f"{self.first_name} {self.last_name}"
