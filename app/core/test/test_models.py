from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@london.com', password='testpass'):
    """Crate sample user"""
    return get_user_model().objects.create_user(email, password)


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
    
    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Cucumber"
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='streak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
