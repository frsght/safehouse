from django.db import models
from django.contrib.auth.models import User

class Locker(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255)
    size = models.CharField(max_length=50)
    isopen = models.BooleanField(default=True)
    rented_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="lockers")

    class Meta:
        db_table = "lockerslist"
        managed = False



