import boto3
import uuid
import json
import os

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
    """Seed the MusicCatalog table with music metadata."""
    table = dynamodb.Table('MusicCatalog')
    
    # Default sample data
    songs = [
        {'emotion': 'HAPPY', 'songName': 'Walking on Sunshine', 'genre': 'Pop', 's3Url': 's3://emotion-music-storage/happy/sunshine.mp3'},
        {'emotion': 'SAD', 'songName': 'Someone Like You', 'genre': 'Soul', 's3Url': 's3://emotion-music-storage/sad/adele.mp3'},
        {'emotion': 'ANGRY', 'songName': 'In the End', 'genre': 'Nu Metal', 's3Url': 's3://emotion-music-storage/angry/lp.mp3'},
        {'emotion': 'CALM', 'songName': 'Weightless', 'genre': 'Ambient', 's3Url': 's3://emotion-music-storage/calm/marconi.mp3'},
    ]

    # Try to load from our new metadata file if it exists
    metadata_path = os.path.join(os.path.dirname(__file__), '../data/music_metadata.json')
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, 'r') as f:
                songs = json.load(f)
            print(f"Loaded {len(songs)} tracks from {metadata_path}")
        except Exception as e:
            print(f"Error loading metadata JSON: {e}")

    print("Seeding music data...")
    with table.batch_writer() as batch:
        for song in songs:
            # Ensure songId is present
            if 'songId' not in song:
                song['songId'] = str(uuid.uuid4())
            # Clean up keys not needed in DynamoDB (like filename)
            item = {k: v for k, v in song.items() if k != 'filename'}
            batch.put_item(Item=item)
    print("Seeding completed.")

if __name__ == "__main__":
    # In a real scenario, the user would run this after configuring AWS CLI
    print("Warning: Ensure you have AWS credentials set up before running this script.")
    # create_tables()
    # seed_data()
