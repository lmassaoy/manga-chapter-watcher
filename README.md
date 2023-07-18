# manga-chapter-watcher
A web scraper + news watcher for monitoring and notifying through e-mail about new chapters of your favorite mangas

## About this project
I wanted to create something to help me (and anyone in similar need) in automating a manual (and daily) task of checking multiple times a website to check if there was a new manga chapter at [mangalivre.net](https://mangalivre.net/)

**Whenever** a new chapter shows up (a chapter with date named as **"Hoje"**)
![./media/manga_page.png](./media/manga_page.png)

an e-mail like this one will be sent to my Gmail

![./media/email_example.png](./media/email_example.png)

## Requirements
Not much.
Basically you'll require:
- Python 3 (in my case, Python 3.10)
- some Python libs:
    - [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
    - [Selenium](https://selenium-python.readthedocs.io/)
- A **Gmail** account, with a [app password](https://support.google.com/accounts/answer/185833?hl=en)

## Setup & Run
There are only few steps to setup and run this project

### 1) Conf: App Conf file
Make a copy of `./conf/example_app_conf.json` in the same directory named as `./conf/app_conf.json`

1.1) Update the e-mail information, replacing the sender/receiver with your e-mail, and the app password of your Gmail account 
```
"sender": "my-email@gmail.com",
"receiver": "my-email@gmail.com",
"password": "aaaaabbbbccccc"
```

1.2) Update the mangas lists you want the solution to monitor
```
"mangasList": [
    "https://mangalivre.net/manga/black-clover/1751",
    "https://mangalivre.net/manga/chainsaw-man/7739",
    "https://mangalivre.net/manga/jujutsu-kaisen/7178"
]
```

### 2) Storage: Cache file
Make a copy of `./storage./example_cache.json` in the same directory named as `./storage./cache.json`

The `cache.json` file will store notifications already performed, so the solution won't send duplicated notifications

### 3) Run
Now just run the project as a regular Python application:
```
$ python3 manga_scanner.py
```

Google Chrome will open a couple of times (one time per manga in the list of monitoring) to access the page's data and copy it locally (html file) - *this is required because regular web scraping won't work since the manga's chapters information is rendered only through browser navigation* :(

After that, the application will check if there are new chapters. If there are, they're checked against the already notified chapters and, if they weren't notified yet, the application will produce an e-mail to notify the user

## Next steps

1) Ideally, I'd like to schedule this to run automatically in some cloud provider such as AWS or GCP. Planning to do this in the near future :) For now I scheduled to run everytime I initialize my PC (along Windows), since I do it everyday.

    1.1) Might also create a Docker image to run this in a container

2) Replace Selenium with another web scraping solution capable of handling rendered pages - probably [requests-html](https://pypi.org/project/requests-html/)