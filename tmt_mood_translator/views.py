from pickle import NONE
from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from .dynamodb_migrator import get_all, get_all_feedback, push_data, check_data, push_feedback, get_all_feedback, get_this_feedback
from googletrans import Translator
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
import ktrain
from . forms import *
import json
from rest_framework import serializers
from .models import Input, User_Evaluation


predictor=ktrain.load_predictor('bert_model/models/bert_model')


class InitialInputSerializer(serializers.ModelSerializer):
    class Meta:
        model=Input
        fields=('input', )

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model=User_Evaluation
        fields=('input', 'joy', 'sadness', 'fear', 'anger', 'neutral')

def create_evaluation(text):
    output=''
    if len(text)<=5:
        return output
    else:
        translator = Translator()
        language=translator.detect(text).lang
        translated=""
        evaluation=""

        if language!='en':
            translated = translator.translate(text, dest='en').text
            score=predictor.predict_proba(translated)
            joy=float(score[0])
            sadness=float(score[1])
            fear=float(score[2])
            anger=float(score[3])
            neutral=float(score[4])
            score_evaluation = {'joy': joy, 'sadness': sadness, 'fear': fear, 'anger': anger, 'neutral': neutral}
            evaluation=json.dumps(score_evaluation)
            output={
                'input': text, 
                'translation': translated, 
                'joy': joy, 
                'sadness': sadness, 
                'fear': fear, 
                'anger': anger, 
                'neutral': neutral,
                }
            push_data(text, translated.text, evaluation)
        else:
            score=predictor.predict_proba(text)
            joy=float(score[0])
            sadness=float(score[1])
            fear=float(score[2])
            anger=float(score[3])
            neutral=float(score[4])
            score_evaluation = {'joy': joy, 'sadness': sadness, 'fear': fear, 'anger': anger, 'neutral': neutral}
            evaluation=json.dumps(score_evaluation)
            output={
                'input': text, 
                'translation': "",
                'joy': joy, 
                'sadness': sadness, 
                'fear': fear, 
                'anger': anger, 
                'neutral': neutral,
                }
            push_data(text, "", evaluation)
    return output

class all_API_analysis(APIView):

    serializer_class = InitialInputSerializer

    def get(self, *args, **kwargs):
        data=get_all()
        return Response(data)
       

    def post(self, request, format=NONE):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            text=serializer.data.get('input')
            indicator, data=check_data(text) 
            if indicator == True:
                return Response(data, status=status.HTTP_200_OK)
            else:
                output=create_evaluation(text)
                if output=='':
                    return Response({'Bad Request': 'Too short...'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(output)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class all_API_feedback(APIView):

    serializer_class = FeedbackSerializer

    def get(self, *args, **kwargs):
        data=get_all_feedback()
        return Response(data)
       

    def post(self, request, format=NONE):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            text=serializer.data.get('input')
            indicator, data=check_data(text) 
            if indicator == True:
                push_feedback(text, serializer.data.get('joy'), serializer.data.get('sadness'),
                                serializer.data.get('fear'), serializer.data.get('anger'), serializer.data.get('neutral'))
                data={'input': text,
                    'joy':serializer.data.get('joy'),
                    'sadness':serializer.data.get('sadness'),
                    'fear':serializer.data.get('fear'),
                    'anger': serializer.data.get('anger'),
                    'neutral': serializer.data.get('neutral')}
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'Bad Request': 'No such input was entered'}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class myAPI_analysis(APIView):

    serializer_class = InitialInputSerializer

    def get(self, *args, **kwargs):
        text=self.kwargs['my_input']
        check, data = check_data(text)
        if check == True:
            return Response(data)
        else:
            return Response({'Bad Request': 'No such input was entered'}, status=status.HTTP_400_BAD_REQUEST)
       

    def post(self, request, format=NONE,  *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            text=serializer.data.get('input')
            indicator, data=check_data(text) 
            if indicator == True:
                return Response(data, status=status.HTTP_200_OK)
            else:
                output=create_evaluation(text)
                if output=='':
                    return Response({'Bad Request': 'Too short...'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(output)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class myAPIS_feedback(APIView):
    serializer_class = FeedbackSerializer

    def get(self, *args, **kwargs):
        text=self.kwargs['my_input']
        indicator, data=get_this_feedback(text)
        if indicator == True:
            return Response(data)
        else:
            return Response({"ERROR": "Feedbacks to this text do not exist."}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=NONE, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            text=serializer.data.get('input')
            indicator, data=check_data(text) 
            if indicator == True:
                push_feedback(text, serializer.data.get('joy'), serializer.data.get('sadness'),
                                serializer.data.get('fear'), serializer.data.get('anger'), serializer.data.get('neutral'))
                data={'input': text,
                    'joy':serializer.data.get('joy'),
                    'sadness':serializer.data.get('sadness'),
                    'fear':serializer.data.get('fear'),
                    'anger': serializer.data.get('anger'),
                    'neutral': serializer.data.get('neutral')}
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'Bad Request': 'No such input was entered'}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

        


def eval_post(joy, sadness, fear, anger, neutral):

    if anger>=0.5:
        return "OFFENSIVE POST, POSTER SHOULD BE WARNED!"
    elif anger>0.2 and (sadness>0.2 or fear>0.2):
        return "RISKY POST, NEED MODERATOR FOR JUDGEMENT."
    elif fear>0.5:
        return "RISKY POST, NEED MODERATOR FOR JUDGEMENT."
    else:
        return "NORMAL POST, NO NEED FOR MODERATION."

    

def home(request):

    if request.method == 'POST' and len(request.POST['comment'])>5:
        text=request.POST['comment']

        indicator, data = check_data(text) #check if text is in database

        if indicator == False:
            translator = Translator()
            language=translator.detect(text).lang

            translated=""
            evaluation=""

            if language!='en':
                translated = translator.translate(text, dest='en').text
                score=predictor.predict_proba(translated)
                joy=float(score[0])
                sadness=float(score[1])
                fear=float(score[2])
                anger=float(score[3])
                neutral=float(score[4])
                score_evaluation = {'joy': joy, 'sadness': sadness, 'fear': fear, 'anger': anger, 'neutral': neutral}
                evaluation=json.dumps(score_evaluation)
                output={
                    'input': text, 
                    'translation': translated, 
                    'eval': eval_post(joy, sadness, fear, anger, neutral),
                    'joy': int(joy*100), 
                    'sadness': int(sadness*100), 
                    'fear': int(fear*100), 
                    'anger': int(anger*100), 
                    'neutral': int(neutral*100),
                    'bool': 'True', 
                    'trans':'True'
                    }
                push_data(text, translated, evaluation)
            else:
                score=predictor.predict_proba(text)
                joy=float(score[0])
                sadness=float(score[1])
                fear=float(score[2])
                anger=float(score[3])
                neutral=float(score[4])
                score_evaluation = {'joy': joy, 'sadness': sadness, 'fear': fear, 'anger': anger, 'neutral': neutral}
                evaluation=json.dumps(score_evaluation)
                output={
                    'input': text,
                    'eval': eval_post(joy, sadness, fear, anger, neutral),
                    'joy': int(joy*100), 
                    'sadness': int(sadness*100), 
                    'fear': int(fear*100), 
                    'anger': int(anger*100), 
                    'neutral': int(neutral*100),
                    'bool': 'True', 
                    'trans':'False'
                    }
                push_data(text, "", evaluation)
            
        else:
            eval=json.loads(data['evaluation'])
            joy=eval['joy']
            sadness=eval['sadness']
            fear=eval['fear']
            anger=eval['anger']
            neutral=eval['neutral']

            if data['translation'] == "":
                output={
                    'input': text, 
                    'eval': eval_post(joy, sadness, fear, anger, neutral),
                    'joy': int(joy*100), 
                    'sadness': int(sadness*100), 
                    'fear': int(fear*100), 
                    'anger': int(anger*100), 
                    'neutral': int(neutral*100),
                    'bool': 'True', 
                    'trans':'False'
                    }
            else:
                output={
                    'input': text,
                    'translation': data['translation'], 
                    'eval': eval_post(joy, sadness, fear, anger, neutral),
                    'joy': int(joy*100), 
                    'sadness': int(sadness*100), 
                    'fear': int(fear*100), 
                    'anger': int(anger*100), 
                    'neutral': int(neutral*100),
                    'bool': 'True', 
                    'trans':'True'
                    }

        context = {
        'posts': output
        } 

        my_string=json.dumps(output)
        my_string=my_string.replace('?', '12question_mark21')

        return HttpResponseRedirect('evaluation/%s' % my_string)


    else:
        output={'input': 'Add some more text to your post!', 'bool': 'False' }
    
    context = {
        'posts': output
    }
    return render(request, 'tmt_mood_translator/home.html', context) #can also use a dictionary {'asd': 'asd'}


def evaluation_view(request, output):

    output=output.replace('12question_mark21', '?')

    form_gallery=satisfied_form()

    if 'yes' in request.POST:
        return HttpResponseRedirect('/')
    elif 'no' in request.POST:
        output=output.replace('?','12question_mark21')
        return HttpResponseRedirect('/feedback/%s' % output)

    context = {
            'posts': json.loads(output),
            'form':form_gallery
    }


    return render(request, 'tmt_mood_translator/evaluation.html', context)

def feedback(request, output):
    form_gallery=user_evaluation_form()

    output=output.replace('12question_mark21', '?')

    if request.method == "POST":
        form_gallery = user_evaluation_form(request.POST, request.FILES)

        if form_gallery.is_valid():
            joy=form_gallery.cleaned_data["joy"]
            sadness=form_gallery.cleaned_data["sadness"]
            fear=form_gallery.cleaned_data["fear"]
            anger=form_gallery.cleaned_data["anger"]
            neutral=form_gallery.cleaned_data["neutral"]

            input=json.loads(output)['input']

            push_feedback(input, joy, sadness, fear, anger,  neutral)

            messages.success(request, 'Thank you for your feedback.')
            
            return HttpResponseRedirect('/')


    context = {
            'posts': json.loads(output),
            'form':form_gallery
    }
    return render(request, 'tmt_mood_translator/feedback.html', context)
