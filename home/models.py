from django.contrib.auth.models import AbstractUser, BaseUserManager
from django import forms
from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField

class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class UserManager(BaseUserManager):
    """ 
    Create a usernamager to create new user's data.
    """
    
    def create_user(self, email,username,  password=None, password2=None,Mobile_number=None,gender=None,city=None,first_name=None,last_name=None):
        """ 
        Create a normal user instead of super user with his/ her personal details.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        
        user.username = username
        user.gender  = gender 
        user.Mobile_number = Mobile_number
        user.city = city
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser,TimeStampModel):
    """ 
    This models is create to store and edit the New registered User's Data and edit Django defualt User authentication 
    """
    GENDER = (
        ('MALE','MALE'),
        ('FEMALE','FEMALE'),
        ('CUSTOME','CUSTOME'),
    )
    email = models.EmailField(unique=True)
    Mobile_number = models.CharField(max_length=10)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    gender = models.CharField(max_length=25,choices=GENDER)
    verification_code = models.BigIntegerField(null=True,blank=True)
    is_user_verified = models.BooleanField(default=False)
    credit = models.BigIntegerField(default=100)
    objects = UserManager()
    REQUIRED_FIELDS = ["email","Mobile_number"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
class instagram_accounts(TimeStampModel):
    STATUS = (
        ('ACTIVE','ACTIVE'),
        ('INACTIVE','INACTIVE'),
    )
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    busy = models.BooleanField(default=False)
    status = models.CharField(max_length=25,choices=STATUS,default='ACTIVE')

# class driver_status(models.Model):
#     need_to_restart_driver = models.BooleanField(default=True)
#     user_data = models.TextField(null=True,blank=True)
