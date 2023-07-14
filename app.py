import requests
from selenium import webdriver


def search_for_new_chapter(link):
    browser = webdriver.Chrome()
    browser.get(link)
    with open(f'./staging_html_objects/{link.split("/")[-2]}.html', "w", encoding='utf-8') as f:
        f.writelines(browser.page_source)
    browser.close


def main():
    search_for_new_chapter('https://mangalivre.net/manga/black-clover/1751')
    search_for_new_chapter('https://mangalivre.net/manga/doku-doku-mori-mori/17358')
    search_for_new_chapter('https://mangalivre.net/manga/my-dragon-system/17292')
    search_for_new_chapter('https://mangalivre.net/manga/golden-kamuy/2455')


if __name__ == '__main__':
    main()