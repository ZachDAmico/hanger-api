from django.db import models

class Cuisine(models.Model):
    type = models.CharField(max_length=255)