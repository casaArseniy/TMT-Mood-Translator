from django.db import models

class Input(models.Model):
    input=models.CharField(max_length=500)
    translation=models.CharField(max_length=1000, blank=True)
    evaluation=models.CharField(max_length=500)

class Satisfaction(models.Model):
    satisfied=models.BooleanField()

class User_Evaluation(models.Model):
    input=models.CharField(max_length=500)
    joy=models.BooleanField()
    sadness=models.BooleanField()
    fear=models.BooleanField()
    anger=models.BooleanField()
    neutral=models.BooleanField()


