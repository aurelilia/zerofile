from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class File(models.Model):
    """ File class, contains file and metadata. User is null if anonymous """
    _id = models.CharField('File ID', max_length=15)
    name = models.CharField('File name', max_length=64)
    mime = models.CharField('Mimetype', max_length=64)
    upload_date = models.DateTimeField('Upload date')
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    expiry = models.DateTimeField('Expires at', default=timezone.datetime(year=2021,month=1,day=7))
    deleted = models.BooleanField('Deleted or expired', default=False)

    def __str__(self):
        return self.name
