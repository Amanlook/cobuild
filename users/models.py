from django.db import models

# Create your models here.
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models, transaction
import uuid


# Create your models here.
class Role(models.Model):

    SUPERADMIN = 1
    ADMIN = 2
    USER = 3

    ROLE_CHOICES = (
        (SUPERADMIN, 'SUPERADMIN'),
        (ADMIN, 'ADMIN'),
        (USER, 'USER'),
    )

    id = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, primary_key=True)
    role_name = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.role_name
    
class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role_id', 1)
        return self._create_user(email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    contact = models.BigIntegerField(default=0, unique=True)
    avtar = models.ImageField(upload_to='avtar/', blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    role=models.ForeignKey(Role,null=True, blank=True,on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)
    counter = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    def __str__(self):
        return str(self.email)

    class Meta:
        ordering = ['-date_joined']