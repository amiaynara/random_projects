import asyncio
import boto3
import os
from telethon.sync import TelegramClient
from telethon.tl.types import DocumentAttributeVideo

from regex_test import normalize_subject, get_subject_name

# Set up Telegram API credentials
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
print(api_id, api_hash)
client = TelegramClient('session_name', api_id, api_hash)
BUCKET_NAME = 'omicsreplica'

def check_upload_status(s3_key):
    s3_client = boto3.client('s3')
    try:
        s3_client.head_object(Bucket=BUCKET_NAME, Key=s3_key)
        return 'UPLOADED'
    except:
        return 'NOT_UPLOADED'

def to_mb(size):
    return round(size / (1024 * 1024), 2)

async def get_file_info(message):
    try:
        if message.media is not None:
            if hasattr(message.media, 'photo') or hasattr(message.media, 'document') and isinstance(message.media.document.attributes[0], DocumentAttributeVideo) or hasattr(message.media, 'document') and message.media.document.mime_type.split("/")[0] == 'image' and message.media.document.mime_type.split("/")[1] == 'gif':
                temp_file_name = message.media.document.attributes[1].file_name
                subject = get_subject_name(temp_file_name)
                normalized_subject = normalize_subject(subject)
                s3_key = f'telegram_media/{normalized_subject}/{temp_file_name}'
                
                file_size = to_mb(message.media.document.size)
                status = 'NOT_UPLOADED' or check_upload_status(s3_key)
                
                print(f"{file_size}\t{temp_file_name}\t{status}")
    except Exception as e:
        print(f"Error processing file info: {e}")

async def list_all_files():
    try:
        await client.start()
        entity = await client.get_entity('viskskka')
        print("file_size\tfile_name\tdownload_status")
        
        async for message in client.iter_messages(entity):
            print('riding..')
            await get_file_info(message)
            
    except Exception as e:
        print(f"Error in list_all_files: {e}")
    finally:
        await client.disconnect()

async def main():
    await list_all_files()

async def run():
    await main()

if __name__ == "__main__":
    print("Starting script...")
    asyncio.run(run())
    print("Script completed")
