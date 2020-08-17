"""best_deals URL Configuration

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
from django.urls import path,include
from app.views import (HomeView, ListView,ContactView,AboutView,
                     DetailView)
from accounts.views import ( RegisterView,LoginView,PassordResetView,EmailConfirmation,
                          LogoutView, UserProfileView, ProfileEditView,UserHistoryView,
                          UserAdressesView,
                          ChangePasswordView, AddressEditView,
                          UserAdressAddView)
from django.conf.urls.static import static
from django.conf import settings                          
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',HomeView.as_view(),name='home'),
    path('product/<subcategory>/',ListView.as_view(),name='subcategory'),
    path('product/<subcategory>/<int:id>',DetailView.as_view(),name='detail'),
    path('cart/',include('cart.urls')),
    path('about/',AboutView.as_view(), name='about'),
    path('contact/',ContactView.as_view(),name='contact'),
    path('accounts/register/',RegisterView.as_view(), name='register'),
    path('accounts/login/',LoginView.as_view(), name='login'),
    path('accounts/reset-password/',PassordResetView.as_view(), name='reset-password'),
    path('accounts/register/email-confirmation',EmailConfirmation.as_view(), name='email_confirmation'),
    path('accounts/logout/',LogoutView.as_view(), name='logout'),
    path('accounts/<username>/',UserProfileView.as_view(), name='profile'),
    path('accounts/<username>/edit',ProfileEditView.as_view(), name='profile-edit'),
    path('accounts/<username>/history',UserHistoryView.as_view(), name='history'),
    path('accounts/<username>/addresses',UserAdressesView.as_view(), name='addresses'),
    path('accounts/<username>/change-password',ChangePasswordView.as_view(), name='change-password'),
    path('accounts/<username>/address-edit/<id>/',AddressEditView.as_view(), name='address-edit'),
    path('accounts/<username>/address-add/',UserAdressAddView.as_view(), name='address-add'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
