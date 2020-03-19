from django.urls import path, include
from rest_framework.routers import DefaultRouter

from movie.views import MovieViewSet, GenreViewSet, ArtistViewSet

router = DefaultRouter()
router.register('movie', MovieViewSet)
router.register('genre', GenreViewSet)
router.register('artist', ArtistViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
