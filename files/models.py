import hashlib
import uuid

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class UserFile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/static_deposit/')
    filename = models.CharField(max_length=120, null=True, blank=True)
    extension = models.CharField(max_length=10, null=True, blank=True)

    uploaded_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_download_date = models.DateTimeField(null=True, blank=True)
    size = models.BigIntegerField(null=True, blank=True)
    commentary = models.CharField(null=True, blank=True, max_length=250)

    link_hash = models.CharField(max_length=250, null=True, blank=True)

    def save(self, *args, **kwargs):

        if not self.filename:
            self.filename = '.'.join(self.file.name.split('.')[:-1])
        if not self.extension:
            self.extension = self.file.name.split('.')[-1]
        if not self.size:
            self.size = self.file.size
        if not self.link_hash:
            self.link_hash = uuid.uuid4().hex

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
