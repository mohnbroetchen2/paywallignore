from django.db import models
from datetime import datetime

class Url(models.Model):
    url = models.CharField(max_length=250)
    ofile = models.CharField(max_length=20, null=True, blank=True)
    pfile = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateField(null=False, auto_now_add=True)