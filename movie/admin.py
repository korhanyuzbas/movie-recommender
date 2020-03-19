from django.contrib import admin

# Register your models here.
from movie.models import Movie, Artist, ArtistFollow, MovieFollow, Genre, GenreFollow


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class MovieAdmin(admin.ModelAdmin):
    list_display = ('imdb_id', 'title')
    raw_id_fields = ('cast',)
    search_fields = ('title', 'imdb_id', 'dataset_id')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


class MovieFollowAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'movie')
    list_display = ('user', 'movie')


class ArtistFollowAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'artist')
    list_display = ('user', 'artist')


class GenreFollowAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'genre')
    list_display = ('user', 'genre')


admin.site.register(Movie, MovieAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(ArtistFollow, ArtistFollowAdmin)
admin.site.register(MovieFollow, MovieFollowAdmin)
admin.site.register(GenreFollow, GenreFollowAdmin)
admin.site.register(Genre, GenreAdmin)
