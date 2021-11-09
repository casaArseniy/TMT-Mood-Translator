from django.shortcuts import render
from .models import Input
from .dynamodb_migrator import push_data, check_data
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

# Create your views here.



def home(request):

    if request.method == 'POST' and len(request.POST['comment'])>5:
        text=request.POST['comment']

        indicator, data = check_data(text)

        if indicator == False:
            translator = Translator()
            language=translator.detect(text).lang

            analyzer=SentimentIntensityAnalyzer()
            translated=""
            evaluation=""

            if language!='en':
                translated = translator.translate(text, dest='en')
                evaluation=json.dumps(analyzer.polarity_scores(translated.text))
                output={'input': text, 'translation': translated.text, 'positivity': evaluation, 'bool': 'True', 'trans':'True'}
                push_data(text, translated.text, evaluation)
            else:
                evaluation=json.dumps(analyzer.polarity_scores(text))
                output={'input': text, 'positivity': evaluation, 'bool': 'True', 'trans':'False'}
                push_data(text, "", evaluation)
            
        else:
            output={'input': text, 'positivity': data['evaluation'], 'translation': data['translation'], 'bool': 'True', 'trans':'True'}
        
        


        # indicator, my_dict = 
        # # check if text is in database
        # if Input.objects.filter(input=text).exists()==False:
        #     translator = Translator()
        #     language=translator.detect(text).lang
        #     if language!='en':
        #         translated = translator.translate(text, dest='en')
        #         #db=Input(input=text, translation=translated.text, positivity=1)
        #         #db.save()
        #         #output={'input': text, 'translation': translated.text, 'positivity': '0.5', 'bool': 'True', 'trans':'True'}
        #     else:
        #         db=Input(input=text, positivity=1)
        #         db.save()
        #         output={'input': text, 'positivity': '0.5', 'bool': 'True', 'trans':'False'}

        #  # if text is already in database
        # else:
        #     positivity=Input.objects.filter(input=text).values('positivity')[0]['positivity']
        #     output={'input': text, 'positivity': positivity, 'bool': 'True'}
         
    else:
        output={'input': 'Add some more text to your post!', 'bool': 'False' }
    
    
    # context = {
    #     'posts': Input.objects.all()
    # }
    context = {
        'posts': output
    }
    return render(request, 'tmt_mood_translator/home.html', context) #can also use a dictionary {'asd': 'asd'}