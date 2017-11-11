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
 		url(r'^ajaxdashboard/$',views.ajax_dashboard,name='ajaxdashboard'),
 		url(r'^ajaxtoggle/$',views.toggle,name='toggle'),
 		url(r'^about/$',views.about,name='about'),
 		url(r'^bibtexloads/$',views.bibtex,name='bibtex'),
 		url(r'^checker/$',views.checker,name='checker'),
 		url(r'^editpost$',views.editpost,name='editpost'),
 		url(r'^savepost/$',views.savepost,name='savepost'),
 		
         
]
