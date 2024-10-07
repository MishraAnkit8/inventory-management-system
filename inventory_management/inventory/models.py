from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.forms import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Use Django's password hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    mobile_no = models.CharField(max_length=15, unique=True)

    # Required fields for Django's auth system
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Linking UserProfile to custom User
    mobile_no = models.CharField(max_length=15, unique=True)

    def clean(self):
        # Validate if email already exists in User model
        if User.objects.filter(email=self.user.email).exclude(pk=self.user.pk).exists():
            raise ValidationError("A user with this email already exists.")
        
        # Validate if mobile_no already exists in UserProfile model
        if UserProfile.objects.filter(mobile_no=self.mobile_no).exclude(pk=self.pk).exists():
            raise ValidationError("A user with this mobile number already exists.")
        
    def save(self, *args, **kwargs):
        # Call the full clean method before saving
        self.full_clean()  
        super(UserProfile, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.first_name
    


#  for insert data into invetory table 

class InventoryManagement(models.Model):
    id = models.AutoField(primary_key=True)
    inventory_name = models.CharField(max_length=255)  
    inventory_product = models.CharField(max_length=255)
    invetory_platform = models.CharField(max_length=255)  
    invetory_prize = models.BigIntegerField()  
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'inventory_management'  
        managed = False  

    def __str__(self):
        return self.inventory_name 
    
    
    


    
    


class InventoryUpdate(models.Model):
    inventory_name = models.CharField(max_length=255)  
    inventory_product = models.CharField(max_length=255)  
    invetory_platform = models.CharField(max_length=255)  
    invetory_prize = models.BigIntegerField()  
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'inventory_management'  

    def __str__(self):
        return f"{self.inventory_name} - {self.inventory_product}"
        