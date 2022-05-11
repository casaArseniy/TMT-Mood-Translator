# TMT-TMT Mood Translator

<br>
<h3>Project for COEN 424</h3>
<br>
<br>
Website that takes as input a text (in any of the languages supported by GoogleTranslate) and gives back a mood translation (neutral, angry, joyful, sad, fearful). Text is translated into English using the googletranslate Python API. Uses a natural language processor model to analyze english text. Website has RESTFUL API supporting GET requests. 
<br>
<br>
Website uses Amazon's DynamoDB to store previous inputs as well as user feedback. Connection between app and database is done using Python's Boto3 library. Website was deployed on an Amazon EC2 instance. Response time of API was tested using POSTMAN. Load Testing was done using K6.

<h3>Requirements</h3>
asgiref==3.4.1
boto3==1.20.10
botocore==1.23.10
certifi==2021.10.8
chardet==3.0.4
charset-normalizer==2.0.7
Django==4.0.2
djangorestframework==3.12.4
googletrans==3.1.0a0
h11==0.9.0
h2==3.2.0
hpack==3.0.0
hstspreload==2021.11.1
httpcore==0.9.1
httpx==0.13.3
hyperframe==5.2.0
idna==2.10
jmespath==0.10.0
python-dateutil==2.8.2
pytz==2021.3
requests==2.26.0
rfc3986==1.5.0
s3transfer==0.5.0
six==1.16.0
sniffio==1.2.0
sqlparse==0.4.2
urllib3==1.26.7
vaderSentiment==3.3.2
