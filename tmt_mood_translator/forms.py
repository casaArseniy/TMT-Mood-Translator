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
        fields = ['joy', 'sadness', 'fear', 'anger', 'neutral']
        labels = {'joy': 'Joy', 'sadness': 'Sadness', 'fear': 'Fear', 'anger': 'Anger', 'neutral':'Neutral'}
