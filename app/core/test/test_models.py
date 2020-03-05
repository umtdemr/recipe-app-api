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