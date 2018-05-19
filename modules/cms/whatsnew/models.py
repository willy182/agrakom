from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Whatsnew(models.Model):
    class Meta:
        db_table = 'whatsnew'

    title = models.CharField(max_length=225)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(blank=True, null=True, upload_to='static/images/galery')
    status = models.BooleanField(blank=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,db_column='created_by', related_name='%(class)s_created_by')
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, db_column='modified_by', related_name='%(class)s_modified_by')
    modified_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.title)


class DetailWhatsnew(models.Model):
    class Meta:
        db_table = 'detail_whatsnew'

    whatsnew = models.ForeignKey(Whatsnew,on_delete=models.DO_NOTHING)
    image = models.FileField(blank=True, null=True, upload_to='static/images/detail_galery')
    caption =  models.CharField(max_length=225,blank=True, null=True)
    status = models.BooleanField(blank=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,db_column='created_by', related_name='%(class)s_created_by')
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, db_column='modified_by', related_name='%(class)s_modified_by')
    modified_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)

