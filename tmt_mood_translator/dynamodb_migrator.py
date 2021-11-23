import boto3
import random
import string
# from boto3.session import Session
# from botocore.client import Config
# from botocore.handlers import set_list_objects_encoding_type_url


def get_all():
    session = boto3.Session(
    aws_access_key_id='AKIA5M7CQUGVVIJIJWVF',
    aws_secret_access_key='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',
    region_name='ca-central-1'
    )

    DB=session.resource('dynamodb')
    table=DB.Table("My_TMT_Table")

    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    
    return data


def check_data(input):
    session = boto3.Session(
    aws_access_key_id='AKIA5M7CQUGVVIJIJWVF',
    aws_secret_access_key='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',
    region_name='ca-central-1'
    )

    DB=session.resource('dynamodb')
    table=DB.Table("My_TMT_Table")

    response = table.get_item(
            Key={
                'input': input
            }
        )
    
    if 'Item' in response:
        return True, response["Item"]
    
    return False, "NULL"


def push_data(input, translation, evaluation):

    session = boto3.Session(
    aws_access_key_id='AKIA5M7CQUGVVIJIJWVF',
    aws_secret_access_key='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',
    region_name='ca-central-1'
    )

    DB=session.resource('dynamodb')
    table=DB.Table("My_TMT_Table")

    
    response = table.put_item(
        Item={
            'input': input,
            'evaluation': evaluation,
            'translation' : translation,
                }
            )

def randStr(chars=string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))

def push_feedback(input, angry, sad, joy, fear, disgust):

    session = boto3.Session(
        aws_access_key_id='AKIA5M7CQUGVVIJIJWVF',
        aws_secret_access_key='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',
        region_name='ca-central-1'
    )

    DB=session.resource('dynamodb')
    table=DB.Table("My_FeedBack_Table")

    id=randStr()

    response = table.put_item(
        Item={
            'input': input,
            'id': id,
            'angry': angry,
            'sad' : sad,
            'joy': joy,
            'fear': fear,
            'disgust': disgust,
                }
            )

    pass