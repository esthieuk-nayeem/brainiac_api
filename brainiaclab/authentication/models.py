from django.db import models
from django.contrib.auth.models import Group

# Create your models here.

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _





class UserManager(BaseUserManager):

    def create_user(self,phone,full_name, email, whatsapp_num,password=None): 
        if phone is None:
            raise TypeError("User should have a Phone")


        user = self.model(phone=phone, full_name=full_name, email=email, whatsapp_num=whatsapp_num)
        user.set_password(password)

        user.save()
        token = Token.objects.create(user=user)
        return user

    def create_superuser(self, phone,password=None):
        if password is None:
            raise TypeError("Password shouldn't be None")

        user = self.create_user(phone, password)
        user.is_superuser = True
        user.is_varified = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=225, db_index=True, null=True,blank=True)
    full_name = models.CharField(max_length=225,null=True, blank=True)
    phone = models.CharField(max_length=225,unique=True,  db_index=True)
    whatsapp_num = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(max_length=225, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_varified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    t_assigned_batches = models.ManyToManyField('course.Batch', blank=True, related_name='t_assigned_batches')
    t_salary = models.PositiveIntegerField(null=True,blank=True)
    t_join_date = models.DateField(auto_now_add=True)
    t_status = models.BooleanField(default=True)
    s_enrolled_batches = models.ManyToManyField('course.Batch', blank=True, related_name='s_enrolled_batches')
    s_fees = models.PositiveIntegerField(null=True,blank=True)
    s_status = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone'
    # REQUIRED_FIELDS = ['username']

    objects = UserManager()


    def __str__(self):
        return self.phone


    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh' : str(refresh),
            'access'  : str(refresh.access_token)
        } 