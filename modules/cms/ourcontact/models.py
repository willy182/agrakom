from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class OurContact(models.Model):
    class Meta:
        db_table = 'our_contact'

    name = models.CharField(max_length=225)
    address = models.TextField(blank=True, null=True)
    telphone = models.CharField(max_length=225)
    fax = models.CharField(max_length=225)
    status = models.BooleanField(blank=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, db_column='modified_by', related_name='%(class)s_modified_by')
    modified_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)


class Sosmed(models.Model):
    class Meta:
        db_table = 'sosmed'

    our_contact = models.ForeignKey(OurContact, on_delete=models.DO_NOTHING)
    image = models.FileField(blank=True, null=True, upload_to='images/sosmed')
    caption = models.CharField(max_length=225, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    status = models.BooleanField(blank=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, db_column='modified_by', related_name='%(class)s_modified_by')
    modified_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
