import requests
import os
from selenium import webdriver


html_dir_path = './staging_html_objects/'


def search_for_new_chapter(link):
    browser = webdriver.Chrome()
    browser.get(link)
    with open(f'{html_dir_path}{link.split("/")[-2]}.html', "w", encoding='utf-8') as f:
        f.writelines(browser.page_source)
    browser.close


def main():
    if os.path.exists(html_dir_path) is False:
        os.mkdir(html_dir_path)

    search_for_new_chapter('https://mangalivre.net/manga/black-clover/1751')
    search_for_new_chapter('https://mangalivre.net/manga/chainsaw-man/7739')
    search_for_new_chapter('https://mangalivre.net/manga/jujutsu-kaisen/7178')


if __name__ == '__main__':
    main()