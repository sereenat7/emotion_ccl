import boto3
import uuid

# Initialize DynamoDB resource
# Note: You must have AWS credentials configured locally to run this script.
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def create_tables():
    """Create the DynamoDB tables if they don't exist."""
    
    # MusicCatalog Table
    try:
        table = dynamodb.create_table(
            TableName='MusicCatalog',
            KeySchema=[
                {'AttributeName': 'emotion', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'songId', 'KeyType': 'RANGE'}  # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'emotion', 'AttributeType': 'S'},
                {'AttributeName': 'songId', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Creating MusicCatalog table...")
        table.wait_until_exists()
        print("MusicCatalog table created.")
    except Exception as e:
        print(f"MusicCatalog table check: {e}")

    # Users Table
    try:
        table = dynamodb.create_table(
            TableName='Users',
            KeySchema=[{'AttributeName': 'userId', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'userId', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Creating Users table...")
        table.wait_until_exists()
        print("Users table created.")
    except Exception as e:
        print(f"Users table check: {e}")

def seed_data():
    """Seed the MusicCatalog table with some sample songs."""
    table = dynamodb.Table('MusicCatalog')
    
    songs = [
        # HAPPY
        {'emotion': 'HAPPY', 'songName': 'Walking on Sunshine', 'genre': 'Pop', 's3Url': 's3://emotion-music-storage/happy/sunshine.mp3'},
        {'emotion': 'HAPPY', 'songName': 'Happy', 'genre': 'Pop', 's3Url': 's3://emotion-music-storage/happy/happy.mp3'},
        {'emotion': 'HAPPY', 'songName': 'Can\'t Stop the Feeling', 'genre': 'Dance', 's3Url': 's3://emotion-music-storage/happy/feeling.mp3'},
        
        # SAD
        {'emotion': 'SAD', 'songName': 'Someone Like You', 'genre': 'Soul', 's3Url': 's3://emotion-music-storage/sad/adele.mp3'},
        {'emotion': 'SAD', 'songName': 'Rainy Night In Georgia', 'genre': 'Soul', 's3Url': 's3://emotion-music-storage/sad/rainy.mp3'},
        {'emotion': 'SAD', 'songName': 'Fix You', 'genre': 'Alt Rock', 's3Url': 's3://emotion-music-storage/sad/fixyou.mp3'},
        
        # ANGRY
        {'emotion': 'ANGRY', 'songName': 'In the End', 'genre': 'Nu Metal', 's3Url': 's3://emotion-music-storage/angry/lp.mp3'},
        {'emotion': 'ANGRY', 'songName': 'Killing In The Name', 'genre': 'Metal', 's3Url': 's3://emotion-music-storage/angry/ratm.mp3'},
        {'emotion': 'ANGRY', 'songName': 'Smells Like Teen Spirit', 'genre': 'Grunge', 's3Url': 's3://emotion-music-storage/angry/nirvana.mp3'},
        
        # CALM
        {'emotion': 'CALM', 'songName': 'Weightless', 'genre': 'Ambient', 's3Url': 's3://emotion-music-storage/calm/marconi.mp3'},
        {'emotion': 'CALM', 'songName': 'Clair de Lune', 'genre': 'Classical', 's3Url': 's3://emotion-music-storage/calm/debussy.mp3'},
        {'emotion': 'CALM', 'songName': 'Ocean Waves', 'genre': 'Nature', 's3Url': 's3://emotion-music-storage/calm/ocean.mp3'},
    ]

    print("Seeding music data...")
    with table.batch_writer() as batch:
        for song in songs:
            song['songId'] = str(uuid.uuid4())
            batch.put_item(Item=song)
    print("Seeding completed.")

if __name__ == "__main__":
    # In a real scenario, the user would run this after configuring AWS CLI
    print("Warning: Ensure you have AWS credentials set up before running this script.")
    # create_tables()
    # seed_data()
