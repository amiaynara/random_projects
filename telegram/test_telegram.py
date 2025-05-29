from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos, InputMessagesFilterVideo, InputMessagesFilterDocument
import os

# Your Telegram API credentials (get them from https://my.telegram.org)
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
phone_number = os.getenv('TELEGRAM_PHONE_NUMBER')
# app title = 'media-downloader'


# Channel/chat details
limit = 100  # Number of recent messages to check

# Create download directory if it doesn't exist
download_dir = 'telegram_media'
os.makedirs(download_dir, exist_ok=True)

# def main():
#     # Create the client and connect
#     client = TelegramClient('session_name', api_id, api_hash)
#     client.start(phone_number)

#     print("Connected to Telegram. Downloading media...")

#     # Download photos
#     photos = client.get_messages(channel_username, limit=limit, filter=InputMessagesFilterPhotos)
#     for photo in photos:
#         file_path = os.path.join(download_dir, f'photo_{photo.id}.jpg')
#         client.download_media(photo, file=file_path)
#         print(f"Downloaded photo: {file_path}")

#     # Download videos
#     videos = client.get_messages(channel_username, limit=limit, filter=InputMessagesFilterVideo)
#     for video in videos:
#         file_path = os.path.join(download_dir, f'video_{video.id}.mp4')
#         client.download_media(video, file=file_path)
#         print(f"Downloaded video: {file_path}")

#     # Download documents
#     documents = client.get_messages(channel_username, limit=limit, filter=InputMessagesFilterDocument)
#     for doc in documents:
#         file_path = os.path.join(download_dir, doc.document.attributes[0].file_name)
#         client.download_media(doc, file=file_path)
#         print(f"Downloaded document: {file_path}")

#     print("Download completed!")

def main():
    recipient = 'viskskka'
    channel_link = 't.me/viskskka'
    # entity = client.get_entity(channel_link)
    # username = entity.username
    # title = entity.title
    message = 'Hello, this is a test message!'
    download_dir = 'telegram_media'
    with TelegramClient('session_name', api_id, api_hash) as client:
        client.start(phone_number)
        # client.send_message(recipient, message)
        # messages = client.get_messages(recipient, limit=10)

        
        client.download_media(recipient, download_dir)

        # for msg in messages:
        #     print(f"Message: {msg.text}")
        # client.download_profile_photo(recipient)
        # print(f"Message sent to {recipient}!")

if __name__ == '__main__':
    main()
