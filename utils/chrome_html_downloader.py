import os
from selenium import webdriver
# from requests_html import HTMLSession


class HtmlDownloader:
    def __init__(self, link, target_dir):
        self.link = link
        self.target_dir = target_dir

    def search_for_new_chapter(self):
        browser = webdriver.Chrome()
        browser.get(self.link)
        with open(f'{self.target_dir}{self.link.split("/")[-2]}.html', "w", encoding='utf-8') as f:
            f.writelines(browser.page_source)
        browser.close

    # TODO
    # def search_for_new_chapter_v2(self):
    #     session = HTMLSession()
    #     request = session.get(self.link)
    #     request.html.render(sleep=3, keep_page=True, scrolldown=3)
    #     with open(f'{self.target_dir}{self.link.split("/")[-2]}.html', "w", encoding='utf-8') as f:
    #         f.writelines(request.html)