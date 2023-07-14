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
remember to create a json object inside of the following path, containing the three attributes:
 - sender
 - receiver
 - password
'''
email_confs = json.load(open('./conf/email.json'))
sender_email = email_confs['sender']
receiver_email = email_confs['receiver']
password = email_confs['password']


def get_chapter_title(chapter):
    try:
        title = chapter.find(class_='cap-name hidden-xs').contents[0]
        return title
    except Exception as e:
        return None


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

        if latest_chapter_dict['releaseDate'].lower() == 'hoje':
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
                server.login(sender_email, password)
                server.send_message(message, from_addr=sender_email, to_addrs=receiver_email)