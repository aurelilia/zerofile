from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    """ File class, contains file and metadata. User is null if anonymous """
    _id = models.CharField('File ID', max_length=15)
    name = models.CharField('File name', max_length=64)
    mime = models.CharField('Mimetype', max_length=64)
    upload_date = models.DateTimeField('upload date')
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
