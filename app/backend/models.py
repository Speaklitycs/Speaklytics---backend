from django.db import models

class ErrorModel(models.Model):
    name = models.CharField(max_length=50, null=True)
    timestamp_start = models.FloatField(null=True)
    timestamp_end = models.FloatField(null=True)