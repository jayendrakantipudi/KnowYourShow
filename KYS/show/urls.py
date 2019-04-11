
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'show'
urlpatterns = [
    path("language",views.language_form),
    path("genre",views.genre_form),
    path("movie/<int:id>/",views.movie,name='movieID'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
