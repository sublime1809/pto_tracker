from django.db import models


class TimeTypes(models.Model):
    type = models.CharField(max_length=300)
    default_count = models.IntegerField()
