from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.register,name='signup'),
    path('signin',views.login,name='signin'),
    path('signout', views.logout, name='signout'),
    path('verify',views.verification,name='verify'),
    path('account/dashboard',views.dashboard,name='dashboard')
]
