"""webscrapping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from myapp import views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup_user', views.signup_user, name='signup_user'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('scrapping', views.scrapping, name='scrapping'),
    path('showallword', views.showallword, name='showallword'),
    path('upload_more_word', views.upload_more_words, name='upload_more_word'),
    path('allhistory', views.showhistory, name='allhistory'),
    path('change_password', views.change_password, name='change_password'),
    path('showhistoryuser', views.showhistoryuser, name='showhistoryuser'),
    path('deletehistory/<int:pid>/', views.deletehistory, name='deletehistory'),
    path('editword', views.editword, name='editword'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
