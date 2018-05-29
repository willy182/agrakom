from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class EventGalery(models.Model):
    class Meta:
        db_table = 'cover_highlight'
        permissions = (
            ("add_highlight", "Can add highlight"),
            ("change_highlight", "Can change highlight"),
            ("delete_highlight", "Can delete highlight"),

        )

    title = models.CharField(max_length=225)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(blank=True, null=True, upload_to='static/images/galery')
    status = models.BooleanField(blank=True)
    position =  models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,db_column='created_by', related_name='%(class)s_created_by')
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, db_column='modified_by', related_name='%(class)s_modified_by')
    modified_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.title)


class DetailEvent(models.Model):
    class Meta:
        db_table = 'detail_highlight'
        permissions = (
            ("add_detail_highlight", "Can add detail highlight"),
            ("change_detail_highlight", "Can change detail highlight"),
            ("delete_detail_highlight", "Can delete detail highlight"),

        )

    event_galery = models.ForeignKey(EventGalery,on_delete=models.DO_NOTHING)
    image = models.FileField(blank=True, null=True, upload_to='static/images/detail_galery')
    caption =  models.CharField(max_length=225,blank=True, null=True)
    status = models.BooleanField(blank=True)
    position =  models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,db_column='created_by', related_name='%(class)s_created_by')
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, db_column='modified_by', related_name='%(class)s_modified_by')
    modified_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)

