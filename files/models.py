from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django_cleanup import cleanup


def user_directory_path(instance, filename):
    return 'usr/usr_{0}/{1}'.format(instance.usr.username, filename)
# Create your models here.
@cleanup.ignore
class File(models.Model):
    class Meta:
        db_table='file'
    id = models.BigAutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=250)
    content_type = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=user_directory_path)
    usr = models.ForeignKey(User, verbose_name=("User"), on_delete=models.CASCADE)


