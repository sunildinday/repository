from django.conf.urls import url

from . import views

app_name = 'user'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register_user/$', views.register_user, name='register_user'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
     url(r'^search/$', views.search, name='search'),
 		url(r'^query/$', views.query, name='query'),
 		url(r'^home/$', views.dashboard, name='dashboard'),
         
]
