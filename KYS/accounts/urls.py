from django.urls import path

from . import views

app_name='accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/moredetails', views.signup2, name='signup2'),
]
