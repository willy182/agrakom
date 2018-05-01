from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Contactus(models.Model):
    class Meta:
        db_table = 'contact_us'

    name = models.CharField(max_length=225)
    email = models.EmailField(max_length=225)
    subject = models.CharField(max_length=225)
    message = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
    status = models.BooleanField(blank=True)