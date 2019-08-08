from django.conf.urls import url
from django.contrib.auth import views as auth_views
from urbanizze.accounts.views import register


urlpatterns = [
    url(r'^login/$', auth_views.login,
       {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', auth_views.logout,
        {'next_page': 'home:home'},
        name='logout'),
    url(r'^register/$', register, name='register'),
]
