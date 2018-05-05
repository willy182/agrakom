from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class AboutUs(models.Model):
    class Meta:
        db_table = 'about_us'

    title = models.CharField(max_length=225)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(blank=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, db_column='modified_by', related_name='%(class)s_modified_by')
    modified_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)


class SliderAboutUs(models.Model):
    class Meta:
        db_table = 'slider_about_us'

    about_us = models.ForeignKey(AboutUs,on_delete=models.DO_NOTHING)
    position = models.IntegerField(blank=True, null=True)
    image = models.FileField(blank=True, null=True, upload_to='images/slider')
    caption = models.CharField(max_length=225, blank=True, null=True)
    status = models.BooleanField(blank=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,db_column='created_by', related_name='%(class)s_created_by')
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, db_column='modified_by', related_name='%(class)s_modified_by')
    modified_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
