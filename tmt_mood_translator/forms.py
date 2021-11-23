from django import forms
from django import forms
from django.forms import ModelForm
from . models import *

class satisfied_form(forms.ModelForm):
    class Meta:
        model = Satisfaction
        fields =['satisfied']
        labels = {'satisfied': 'Check if YES/Uncheck if NO'}

class user_evaluation_form(forms.ModelForm):
    class Meta:
        model = User_Evaluation
        fields = ['angry', 'sad', 'joy', 'fear', 'disgust']
        labels = {'angry': 'Angry', 'sad': 'Sad', 'joy': 'Joy', 'fear': 'Fear', 'disgust':'Disgust'}
