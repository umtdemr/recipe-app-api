# Udemy course note

## Docker

Dockerfile

docker build .

docker-compose

travis ci

## Unit tests

https://docs.python.org/3/library/unittest.html#assert-methods


```py
# calc.py
def add(x, y):
    """ Add to numbers together """
    return x + y

# tests.py 

from django.test import TestCase

from app.calc import add

class CalcTests(TestCase):
    def test_add_numbers(self):
        """Test that two numbers are added together"""
        self.assertEqual(add(3, 8), 11)

# in terminal
docker-compose run app sh -c "python manage.py test" 

```

## Custom user model

diğer docs da.

user manager create_user içinde self.normalize_email(email) demek kayıt esnasında işimize yarar.

### assertEqual
### assertTrue
### assertRaises
bunu with ile kullanırsak: 

```py
# app/core/test/test_models.py
def test_new_user_invaild_email(self):
    """test creating user with no email raises error"""
    with self.assertRaises(ValueError):
        get_user_model().objects.create_user(None, 'qweqe')

# app/core/models.py
def create_user(self, email, password=None, **extra_fields):
    """ Creates and save new user"""
    if not email:
        raise ValueError('users must have an email adress')
    # bu şekilde bu testi geçeriz
```
