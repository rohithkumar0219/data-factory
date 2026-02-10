from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face_image = models.ImageField(upload_to='faces/', null=True, blank=True)
    face_id = models.CharField(max_length=255, null=True, blank=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
