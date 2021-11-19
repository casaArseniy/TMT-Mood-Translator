from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from .models import Input
from .dynamodb_migrator import get_all, push_data, check_data
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json

# Create your views here.

class myAPI(APIView):

    def get(self, *args, **kwargs):
        data=get_all()
        return Response(data)
       

    def post(self):
        pass

class myAPISingle(APIView):
    def get(self, *args, **kwargs):
        text=self.kwargs['input']
        indicator, data=check_data(text)
        if indicator == True:
            return Response(data)
        else:
            if len(self.kwargs['input'])<=5:
                return HttpResponseNotFound('<h1>Input too short</h1>')
            else:
                translator = Translator()
                language=translator.detect(text).lang

                analyzer=SentimentIntensityAnalyzer()
                translated=""
                evaluation=""

                if language!='en':
                    translated = translator.translate(text, dest='en')
                    evaluation=json.dumps(analyzer.polarity_scores(translated.text))
                    output={'input': text, 'translation': translated.text, 'positivity': evaluation}
                    push_data(text, translated.text, evaluation)
                else:
                    evaluation=json.dumps(analyzer.polarity_scores(text))
                    output={'input': text, 'translation': "", 'positivity': evaluation}
                    push_data(text, "", evaluation)
                
                return Response(output)

       

    def post(self):
        pass


def eval_post(neg, neu, pos):
    
    if neg>=0.6:
        return "OFFENSIVE POST, POSTER SHOULD BE WARNED!"
    
    elif neg>=0.3 and (neu<0.4 or pos<0.4):
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

            analyzer=SentimentIntensityAnalyzer()
            translated=""
            evaluation=""

            if language!='en':
                translated = translator.translate(text, dest='en')
                evaluation=json.dumps(analyzer.polarity_scores(translated.text))
                ################################################################
                eval=json.loads(evaluation)
                neg=float(eval['neg'])
                neu=float(eval['neu'])
                pos=float(eval['pos'])
                #output={'input': text, 'translation': translated.text, 'positivity': evaluation, 'bool': 'True', 'trans':'True'}
                output={'input': text, 'translation': translated.text, 'eval': eval_post(neg, neu, pos), 'neg':int(neg*100), 'neu':int(neu*100), 'pos':int(pos*100), 'bool': 'True', 'trans':'True'}
                push_data(text, translated.text, evaluation)
            else:
                evaluation=json.dumps(analyzer.polarity_scores(text))
                eval=json.loads(evaluation)
                neg=float(eval['neg'])
                neu=float(eval['neu'])
                pos=float(eval['pos'])
                #output={'input': text, 'positivity': evaluation, 'bool': 'True', 'trans':'False'}
                output={'input': text, 'eval': eval_post(neg, neu, pos), 'neg':int(neg*100), 'neu':int(neu*100), 'pos':int(pos*100), 'bool': 'True', 'trans':'False'}
                push_data(text, "", evaluation)
            
        else:
            eval=json.loads(data['evaluation'])
            neg=float(eval['neg'])
            neu=float(eval['neu'])
            pos=float(eval['pos'])

            if data['translation'] == "":
                output={'input': text, 'eval': eval_post(neg, neu, pos), 'neg':int(neg*100), 'neu':int(neu*100), 'pos':int(pos*100), 'translation': data['translation'], 'bool': 'True', 'trans':'False'}
            #output={'input': text, 'positivity': data['evaluation'], 'translation': data['translation'], 'bool': 'True', 'trans':'True'}
            else:
                output={'input': text, 'eval': eval_post(neg, neu, pos), 'neg':int(neg*100), 'neu':int(neu*100), 'pos':int(pos*100), 'translation': data['translation'], 'bool': 'True', 'trans':'True'}
         
    else:
        output={'input': 'Add some more text to your post!', 'bool': 'False' }
    
    context = {
        'posts': output
    }
    return render(request, 'tmt_mood_translator/home.html', context) #can also use a dictionary {'asd': 'asd'}