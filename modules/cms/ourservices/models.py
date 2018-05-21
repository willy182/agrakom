from django.contrib.auth.models import User
from django.db import models

class OurServices(models.Model):
    class Meta:
        db_table = 'our_services'

    title = models.CharField(max_length=225)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(blank=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,db_column='created_by', related_name='%(class)s_created_by')
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, db_column='modified_by', related_name='%(class)s_modified_by')
    modified_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.title)

class OurServiceDetail(models.Model):
    class Meta:
        db_table = 'our_service_detail'

    # our_services = models.ForeignKey(OurServices, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=225)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(blank=True, null=True, upload_to='static/images/services')
    # caption = models.CharField(max_length=225, blank=True, null=True)
    status = models.BooleanField(blank=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,db_column='created_by', related_name='%(class)s_created_by')
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, db_column='modified_by', related_name='%(class)s_modified_by')
    modified_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
