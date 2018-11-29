from django.urls import path
from django.conf.urls import url
from . import views
from .forms import LoginForm
from django.contrib.auth import views as authv

urlpatterns = [
    # index
    path(r'', views.index, name='index'),
    # profile
    path(r'user_profile/', views.profile, name='profile'),
    # register
    path(r'user_register/', views.register, name='register'),
    path(r'user_register_save/', views.register_save, name='register_save'),
    # login
    path(r'user_login/', authv.LoginView.as_view(template_name='main_app/login.html',
                                                 authentication_form=LoginForm), name='login'),
    # logout
    path(r'user_logout/', authv.LogoutView.as_view(template_name='main_app/logout.html'), name='logout'),
    # password reset
    path(r'user_login/password_reset/', views.password_reset, name='password_reset'),
    path(r'user_login/password_reset_done/', views.password_reset_done, name='password_reset_done'),
    # password reset confirm using url method (I can't build using path method.. why?)
    url(
        r'^user_login/password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    path(r'user_login/password_reset_complete', views.password_reset_complete, name='password_reset_complete'),
    # end password

    # project
    url(r'^user_profile/project/(?P<project_name>[0-9A-Za-z_\-]+)/action', views.handle_select_button, name='handle_button'),
    url(r'^user_profile/project/(?P<project_name>[0-9A-Za-z_\-]+)/upload_complete', views.form, name='uploading'),
    url(r'^user_profile/project/(?P<project_name>[0-9A-Za-z_\-]+)/', views.certain_project, name='your_project'),
]

app_name = 'main_app'
