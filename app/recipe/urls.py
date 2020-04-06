from django.urls import path, include
from rest_framework.routers import DefaultRouter  # viewset için oto url oluşturur

from recipe import views 


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]