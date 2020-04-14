# User işlemleri

## user oluşturma 
1. docker-compose run --rm app sh -c "python manage.py startapp user" : --rm temiz tutar
2. installed apps rest_framework, rest_framework.authtoken, user ekle
3. user test test user_api ekle ve testcase, rest_framework.test import APIClient ekle

> her testte veri tabanı yenilenir

4. sonunda create user api: user/serializers.py
5. 
```py

from django.contrib.auth import get_user_model

from rest_framework import serializers  # direkt model seçimi için kolaylık sağlar


class UserSerializer(serializers.ModelSerializer):
    """ serializer for the user objects"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)
```

6. views.py içinde
```py

from rest_framework import generics  # createapiview listapi view listcreate retriveapiview ...

from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

```
7. daha sonra urls içide create/ kısmına dahil edip ana urls dende user/ a include edilmeli


## Token oluşturma
1. user/test altında daha çnce yapılmış testlere ek 4 tane daha ekledik.
2. serializer kısmında auth dan authenticate ekledik. birde ugettext_lazy as _
3. serializer classında serializer.Serializer kullandık bu fieldları kendimizin oluşturmasını sağlıyor
```py

class AuthTokenSerializer(serializers.Serializer):
    """Serialize for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credintials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs  # her override ettiğimizde return etmemiz gerekiyor

```
4. view altında 
```py
from rest_framework.authtoken.views import ObtainAuthToken  # miras alma için
from rest_framework.settings import api_settings  # for rendered class

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
```