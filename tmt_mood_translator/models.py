from django.db import models

class Input(models.Model):
    input=models.CharField(max_length=500)
    translation=models.CharField(max_length=1000, blank=True)
    positivity=models.DecimalField(max_digits=2, decimal_places=1)

