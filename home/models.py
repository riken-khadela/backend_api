from email.policy import default
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django import forms
from django.db import models
import random, string
# from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
def generate_random_string(length=15):
    letters = string.ascii_letters  # includes uppercase and lowercase letters
    return ''.join(random.choice(letters) for _ in range(length))


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True




# --------------------------------------------UserManager Code By Riken-------------------------------------------------------------


# class UserManager(BaseUserManager):
#     """ 
#     Create a usernamager to create new user's data.
#     """
    
#     def create_user(self, email,username,  password=None, password2=None,Mobile_number=None,gender=None,city=None,first_name=None,last_name=None):
#         """ 
#         Create a normal user instead of super user with his/ her personal details.
#         """
#         if not email:
#             raise ValueError('User must have an email address')

#         user = self.model(
#             email=self.normalize_email(email),
#         )
        
#         user.username = username
#         user.first_name = first_name
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, name, password=None):
#         """
#         Creates and saves a superuser with the given email, name and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             name=name,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


# --------------------------------------------UserManager Code By Riken-------------------------------------------------------------



# --------------------------------------------UserManager Code By Adil-------------------------------------------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """ 
        Create a normal user instead of super user with his/ her personal details.
        """
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Superuser must have an email address')

        email = self.normalize_email(email)
        #user = self.model(email=email, username=email, is_staff=True, is_superuser=True, **extra_fields)
        user = self.model(email=email, is_staff=True, is_superuser=True, **extra_fields)
        #user = self.model(email=email, is_admin = True, is_staff=True, is_superuser=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

# --------------------------------------------UserManager Code By Adil-------------------------------------------------------------





#-----------------------------------------------------CustomUser Code BY Riken-------------------------------------------------------------
# class CustomUser(AbstractUser,TimeStampModel):
#     """ 
#     This models is create to store and edit the New registered User's Data and edit Django defualt User authentication 
#     """
#     GENDER = (
#         ('MALE','MALE'),
#         ('FEMALE','FEMALE'),
#         ('CUSTOME','CUSTOME'),
#     )
#     id = models.BigAutoField(primary_key=True)
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=25)
#     verification_code = models.BigIntegerField(null=True,blank=True)
#     is_user_verified = models.BooleanField(default=False)
#     credit = models.BigIntegerField(default=100)
#     objects = UserManager()
#     Mobile_number = models.IntegerField(default=0)
#     REQUIRED_FIELDS = ["email","Mobile_number"]

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return self.is_admin

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True

#-----------------------------------------------------Code BY Riken-------------------------------------------------------------
    

#-----------------------------------------------------Code BY Adil-------------------------------------------------------------
class CustomUser(AbstractUser,TimeStampModel):
    """ 
    This models is create to store and edit the New registered User's Data and edit Django defualt User authentication 
    """
    GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        ('CUSTOM', 'CUSTOM'),
    )

    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=25)
    verification_code = models.BigIntegerField(null=True, blank=True)
    is_user_verified = models.BooleanField(default=False)
    credit = models.BigIntegerField(default=100)
    Mobile_number = models.IntegerField(default=0)
    #gender = models.CharField(max_length=25, choices=GENDER, null=True, blank=True)
    REQUIRED_FIELDS = ["email","is_user_verified"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_staff

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True 
#-----------------------------------------------------Code BY Adil-------------------------------------------------------------






class DepositeMoney(TimeStampModel):
    METHOD = (
        ('CREDIT_CARD','CREDIT_CARD'),
        ('DEBIT_CARD','DEBIT_CARD'),
    )
    STATUS = (
        ('COMPLETE','COMPLETE'),
        ('INPROCESS','INPROCESS'),
        ('DECLINED','DECLINED'),
    )
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Amount = models.BigIntegerField()
    TransactionId = models.CharField(max_length=255)
    method = models.CharField(max_length=255,choices=METHOD)
    status =  models.CharField(max_length=25,choices=STATUS)

class SearchedHistory(TimeStampModel):
    CHOICES = (
        ('Instagram','Instagram'),
        ('Youtube','Youtube'),
    )
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    hashtag = models.CharField(max_length=25)
    platform = models.CharField(max_length=25,choices=CHOICES)
    result = models.TextField()
        
class instagram_accounts(TimeStampModel):
    STATUS = (
        ('ACTIVE','ACTIVE'),
        ('INACTIVE','INACTIVE'),
    )
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    busy = models.BooleanField(default=False)
    status = models.CharField(max_length=25,choices=STATUS,default='ACTIVE')

# class driver_status(models.Model):
#     need_to_restart_driver = models.BooleanField(default=True)
#     user_data = models.TextField(null=True,blank=True)
