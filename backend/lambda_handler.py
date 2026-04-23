import json
import boto3
import base64
import os
import uuid
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# Initialize AWS clients
comprehend = boto3.client('comprehend')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# Environment variables (to be set in Lambda console)
MUSIC_TABLE = os.environ.get('MUSIC_TABLE', 'MusicCatalog')
USERS_TABLE = os.environ.get('USERS_TABLE', 'Users')
BUCKET_NAME = os.environ.get('S3_BUCKET', 'emotion-music-storage')

def get_presigned_url(s3_url):
    """Generate a pre-signed URL for the S3 object."""
    try:
        # Expected format: s3://bucket-name/key
        if s3_url.startswith('s3://'):
            parts = s3_url.replace('s3://', '').split('/', 1)
            bucket = parts[0]
            key = parts[1]
        else:
            # Fallback if only key is provided
            bucket = BUCKET_NAME
            key = s3_url

        response = s3.generate_presigned_url('get_object',
                                            Params={'Bucket': bucket,
                                                    'Key': key},
                                            ExpiresIn=3600)
        return response
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")
        return None

def detect_emotion_from_text(text):
    """Use Amazon Comprehend to detect sentiment/emotion."""
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment'] # POSITIVE, NEGATIVE, NEUTRAL, MIXED
    
    # Map Comprehend sentiment to our emotions
    mapping = {
        'POSITIVE': 'HAPPY',
        'NEGATIVE': 'ANGRY', # Simplified mapping
        'NEUTRAL': 'CALM',
        'MIXED': 'SAD'
    }
    return mapping.get(sentiment, 'CALM')

def detect_emotion_from_image(image_base64):
    """Use Amazon Rekognition to detect facial emotion."""
    try:
        image_bytes = base64.b64decode(image_base64)
        response = rekognition.detect_faces(
            Image={'Bytes': image_bytes},
            Attributes=['EMOTIONS']
        )
        
        if not response['FaceDetails']:
            return 'CALM'
            
        # Get the highest confidence emotion
        emotions = response['FaceDetails'][0]['Emotions']
        top_emotion = max(emotions, key=lambda x: x['Confidence'])
        
        # Rekognition emotions: HAPPY, SAD, ANGRY, CONFUSED, DISGUSTED, SURPRISED, CALM, UNKNOWN
        return top_emotion['Type']
    except Exception as e:
        print(f"Error detecting emotion from image: {e}")
        return 'CALM'

def get_recommendations(emotion):
    """Query DynamoDB for songs matching the emotion."""
    table = dynamodb.Table(MUSIC_TABLE)
    try:
        response = table.query(
            KeyConditionExpression=Key('emotion').eq(emotion),
            Limit=5
        )
        songs = response.get('Items', [])
        
        # Add pre-signed URLs
        for song in songs:
            if 's3Url' in song:
                song['streamUrl'] = get_presigned_url(song['s3Url'])
        
        return songs
    except Exception as e:
        print(f"Error querying DynamoDB: {e}")
        return []

def lambda_handler(event, context):
    """Main Lambda entry point."""
    print(f"Received event: {json.dumps(event)}")
    
    # CORS headers
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    try:
        body = json.loads(event.get('body', '{}'))
        user_id = body.get('userId', 'anonymous')
        input_type = body.get('type') # 'text' or 'image'
        input_data = body.get('data')

        detected_emotion = 'CALM'

        if input_type == 'text':
            detected_emotion = detect_emotion_from_text(input_data)
        elif input_type == 'image':
            detected_emotion = detect_emotion_from_image(input_data)
        else:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Invalid input type. Must be text or image.'})}

        # Get songs
        songs = get_recommendations(detected_emotion)

        # Save to history
        try:
            user_table = dynamodb.Table(USERS_TABLE)
            # We use a combined key or just update the user's current session
            user_table.put_item(Item={
                'userId': user_id,
                'lastDetected': detected_emotion,
                'lastUpdate': str(uuid.uuid4()), # simplified for demo
                'history': [s['songName'] for s in songs]
            })
        except Exception as e:
            print(f"History logging failed: {e}")

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'emotion': detected_emotion,
                'songs': songs
            })
        }

    except Exception as e:
        print(f"Unhandled error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
