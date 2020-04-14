# Custom user model with tdd

```python

# core.models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """ Creates and save new user"""
        if not email:
            raise ValueError('users must have an email adress')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db) # multiple databae
        
        return user
    
    def create_superuser(self, email, password):
        """Creates and saves new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


# core/test/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    
    def test_create_user_with_email_successful(self):
        """Test creating new user with an email is successful"""
        email = 'test@deneme.com'
        password = '12345'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test is the email for new user is normalized"""
        email = 'test@DENEME.COM'
        user = get_user_model().objects.create_user(
            email,
            '12134'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invaild_email(self):
        """test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'qweqe')

    def test_create_new_superuser(self):
        """test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            'deneme@deneme.com',
            'test1234'
        )
        self.assertTrue(user.is_superuser) # permissions mixin
        self.assertTrue(user.is_staff)

# settings.py bottom
AUTH_USER_MODEL = 'core.User'
```