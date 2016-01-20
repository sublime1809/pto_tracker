from django.db import models

from pto import models as pto_models


class Company(models.Model):
    name = models.CharField(max_length=500)
    time_types = models.ManyToManyField(pto_models.TimeTypes)
