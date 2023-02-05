from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.register,name='signup'),
    path('',views.login,name='signin'),
    path('logout/', views.logout, name='signout'),
    path('verify/',views.verification,name='verify'),
    path('dashboard/',views.dashboard,name='dashboard')
]
