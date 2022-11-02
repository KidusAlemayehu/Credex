from django.urls import path
from . import views
urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('open_file/<int:id>', views.open, name='open_file')
]
