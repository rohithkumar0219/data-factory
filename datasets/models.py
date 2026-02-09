from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    raw_file = models.FileField(upload_to='raw/')
    processed_file = models.FileField(upload_to='processed/', null=True, blank=True)

    name = models.CharField(max_length=255)
    rows_before = models.IntegerField(default=0)
    rows_after = models.IntegerField(default=0)
    cleaned_rows = models.IntegerField(default=0)

    ai_summary = models.TextField(blank=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
