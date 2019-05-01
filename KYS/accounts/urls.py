from django.urls import path
from django.conf.urls import url
from . import views

app_name='accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/moredetails', views.signup2, name='signup2'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
]
