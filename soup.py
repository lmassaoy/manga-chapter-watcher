from bs4 import BeautifulSoup
import os
import json
import smtplib, ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


port = 465
smtp_server = 'smtp.gmail.com'
html_dir_path = './staging_html_objects/'

'''
remember to create a config json object inside of the path `./conf/`
model:
{
    "storage": {
        "storeExecutions": true,
        "location": "./storage/cache.json"
    },
    "email": {
        "sender": "my-email@gmail.com",
        "receiver": "my-email@gmail.com",
        "password": "aaaaabbbbccccc"
    }
}

important notes:
- if `storeExecutions` is true, then `location` needs to be informed passing the path of the storage json object
- create an app password for your gmail to attach to this application

'''

def load_configs():
    app_configs = json.load(open('./conf/app_conf.json'))

    storage_usage = app_configs['storage']['storeExecutions']
    if 'location' in app_configs['storage']:
        storage_location = app_configs['storage']['location']
    else:
        storage_location = None
    sender_email = app_configs['email']['sender']
    receiver_email = app_configs['email']['receiver']
    email_password = app_configs['email']['password']

    return storage_usage, storage_location, sender_email, receiver_email, email_password


def load_cache_file(storage_location):
    if storage_location is None:
        storage_location = './storage/cache.json'

    try:
        notification_cache = json.load(open(storage_location))
    except FileNotFoundError as e:
        print(f'Cache object not found. Creating a new one at {storage_location}')
        initial_cache_structure = {
            "mangas": {

            }
        }
        with open(storage_location, 'w') as outfile:  
            json.dump(initial_cache_structure, outfile)
        notification_cache = initial_cache_structure
    
    return notification_cache


def get_chapter_title(chapter):
    try:
        title = chapter.find(class_='cap-name hidden-xs').contents[0]
        return title
    except Exception as e:
        return None


def send_notification(manga_dict, latest_chapter_dict):
    try:
        message = MIMEMultipart()
        message['Subject'] = f'A WILD {manga_dict["title"].upper()} MANGA APPEARED! 👾'
        message['From'] = sender_email
        message['To'] = receiver_email

        body = open('./utils/email_template_html.html', encoding='utf-8').read()
        body = body.replace('{manga_title}', manga_dict['title'])\
                    .replace('{manga_cover}', manga_dict['cover'])\
                    .replace('{manga_chapter}', latest_chapter_dict['title'])\
                    .replace('{manga_chapter_link}', latest_chapter_dict['link'])
        messageText = MIMEText(body,'html')
        message.attach(messageText)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, email_password)
            server.send_message(message, from_addr=sender_email, to_addrs=receiver_email)
    except Exception as e:
        raise(e)
    else:
        return True


# Loading configs and storage
storage_usage, storage_location, sender_email, receiver_email, email_password = load_configs()
if storage_usage:
    notification_cache = load_cache_file(storage_location)
    print('Loaded cache object:')
    print(notification_cache)


for path in os.listdir(html_dir_path):
    try:
        html = open(os.path.join(html_dir_path, path), encoding="utf8")
        soup = BeautifulSoup(html, 'html.parser')
    except Exception as e:
        raise(e)
    else:
        metadata_block = soup.find(id='series-data')
        manga_dict = {
            'title': str(metadata_block.find(class_="series-title").contents[0]).replace('</h1>','<h1>').replace('<h1>',''),
            'author': str(metadata_block.find(class_="series-author").contents[0]).lstrip().rstrip(),
            'cover': metadata_block.find(class_='cover').find('img').get('src')
        }

        latest_chapter = soup.find(class_='full-chapters-list list-of-chapters').find_all('li')[0]
        latest_chapter_dict = {
            'link': 'https://mangalivre.net' + latest_chapter.find('a').get('href'),
            'title': latest_chapter.find('a').get('title').replace('Ler ',''),
            'releaseDate': latest_chapter.find(class_='chapter-date').contents[0],
            'chapterName': get_chapter_title(latest_chapter),
        }
        if latest_chapter_dict['chapterName'] is not None:
            latest_chapter_dict['title'] = latest_chapter_dict['title'] + ' - ' + latest_chapter_dict['chapterName']

        if latest_chapter_dict['releaseDate'].lower() == 'hoje' or \
            latest_chapter_dict['releaseDate'].lower() == 'ontem':

            if storage_usage:
                if manga_dict['title'] not in notification_cache['mangas']:
                    notification_cache['mangas'][manga_dict["title"]] = {}
                
                if latest_chapter_dict['title'] not in notification_cache['mangas'][manga_dict["title"]]:
                    print(f"{manga_dict['title']}: {latest_chapter_dict['title']} was not notified yet. Sending notification.")
                    notification_cache['mangas'][manga_dict["title"]][latest_chapter_dict['title']] = send_notification(manga_dict, latest_chapter_dict)
                else:
                    print(f"{manga_dict['title']}: {latest_chapter_dict['title']} was already notified. Skipping it.")
            else:
                print(f"Sending notification about {manga_dict['title']}: {latest_chapter_dict['title']}")
                send_notification(manga_dict, latest_chapter_dict)


# Updating cache
if storage_usage:
    with open(storage_location, 'w') as outfile:  
        json.dump(notification_cache, outfile)