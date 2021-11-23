from django.db import models

class Input(models.Model):
    input=models.CharField(max_length=500)
    translation=models.CharField(max_length=1000, blank=True)
    positivity=models.CharField(max_length=500)

class Satisfaction(models.Model):
    satisfied=models.BooleanField()

class User_Evaluation(models.Model):
    angry=models.BooleanField()
    sad=models.BooleanField()
    joy=models.BooleanField()
    fear=models.BooleanField()
    disgust=models.BooleanField()

