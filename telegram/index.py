import asyncio
import boto3
import os
from telethon.sync import TelegramClient
from telethon.tl.types import DocumentAttributeVideo

from regex_test import normalize_subject, get_subject_name

# Set up Telegram API credentials
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
client = TelegramClient('session_name', api_id, api_hash)
BUCKET_NAME = 'omicsreplica'

def upload_to_s3(media, s3_key, temp_file):
    s3_client = boto3.client('s3')
    
    try:
        print(f'will upload {temp_file} to s3 {s3_key}')
        s3_client.upload_file(
            temp_file, 
            BUCKET_NAME, 
            s3_key,
            ExtraArgs={'StorageClass': 'DEEP_ARCHIVE'}
        )
    except Exception as e:
        print(f"Error uploading to S3: {e}")
    finally:
        if os.path.exists(temp_file):
            print(f'removing temp file : {temp_file} after upload')
            os.remove(temp_file)

def check_upload_status(s3_key):
    s3_client = boto3.client('s3')
    bucket_name = 'upsc'
    try:
        s3_client.head_object(Bucket=bucket_name, Key=s3_key)
        return 'UPLOADED'
    except:
        return 'NOT_UPLOADED'

def to_mb(size):
    return round(size / (1024 * 1024), 2)

async def download_media(message):
    try:
        if message.media is not None:
            if hasattr(message.media, 'photo') or hasattr(message.media, 'document') and isinstance(message.media.document.attributes[0], DocumentAttributeVideo) or hasattr(message.media, 'document') and message.media.document.mime_type.split("/")[0] == 'image' and message.media.document.mime_type.split("/")[1] == 'gif':
                temp_file_name = message.media.document.attributes[1].file_name
                subject = get_subject_name(temp_file_name)
                normalized_subject = normalize_subject(subject)
                output_file_path = os.path.join('telegram_media', normalized_subject, temp_file_name)
                s3_key = f'telegram_media/{normalized_subject}/{temp_file_name}'
                
                print(f"Processing: {temp_file_name}")
                
                status = check_upload_status(s3_key)
                if status == 'UPLOADED':
                    print(f"Already uploaded: {temp_file_name}")
                    return
                    
                temp_file = await client.download_media(message.media, file=output_file_path)
                upload_to_s3(message.media, s3_key, temp_file)
                print(f"Completed: {temp_file_name}")
    except Exception as e:
        print(f"Error downloading media: {e}")

async def download_all_media():
    try:
        await client.start()
        entity = await client.get_entity('viskskka')
        print("Starting download process...")
        
        async for message in client.iter_messages(entity):
            await download_media(message)
            
    except Exception as e:
        print(f"Error in download_all_media: {e}")
    finally:
        await client.disconnect()

async def main():
    await download_all_media()

async def run():
    await main()


if __name__ == "__main__":
    print("Starting script...")
    asyncio.run(run())
    # upload_to_s3(None, 'test', 'file_names.tsv')
    print("Script completed")
