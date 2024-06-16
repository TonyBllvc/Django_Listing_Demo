from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserAccountManager

# Create your models here.
class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True) #False when you need to verify user
    is_staff = models.BooleanField(default=False)

    # used to distinguish, a realtor, user and admin user
    is_realtor = models.BooleanField(default=False)
    
    USERNAME_FIELD="email" # username field

    REQUIRED_FIELDS=["name"] #required on signup

    objects = UserAccountManager()
    
    # Provided by ai
    # class Meta:
    #     app_label = 'user'
    #     db_table = 'user_useraccount'  # Optional: Specify custom table name
    #     verbose_name = 'User Account'
    #     verbose_name_plural = 'User Accounts'

    def __str__(self):
        return self.email