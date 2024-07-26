import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

MAIN_URL = "https://www.wowhead.com/wow/retail"
WOW_URL = "https://www.wowhead.com"


class Scrape:

    page = requests.get(MAIN_URL, headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
    soup = BeautifulSoup(page.content, "html.parser")

    def get_item_links(self, link):
        pattern = re.compile(r'/item=')
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        main_content = soup.find(class_="news-post-content")
        a_tag = main_content.find_all('a')
        item_links = []
        for tag in a_tag:
            href = tag.get("href")
            if pattern.match(href):
                if WOW_URL + href not in item_links:
                    item_links.append(WOW_URL + href)

        return item_links

    def get_item_names(self, item_links):
        item_names = []

        for item_link in item_links:
            page = requests.get(item_link)
            soup = BeautifulSoup(page.content, "html.parser")
            h1_tag = soup.find(class_="heading-size-1")
            item_names.append(h1_tag.string)

        return item_names

    def get_post_titles(self):
        print("getting post titles")
        post_titles = []
        class_news_list = self.soup.find_all(id="main-news-heading")
        news_posts = class_news_list[0].find_all_next(class_="news-list-card-content")

        for post in news_posts:
            #find tags with h3, then tags with a nested under h3, then the string value of the a tag
            post_titles.append(post.find("h3").find("a").string)

        return post_titles

    def get_post_dates(self):
        print("getting post dates")
        post_dates = []

        class_news_list = self.soup.find_all(id="main-news-heading")
        news_posts = class_news_list[0].find_all_next(class_="news-list-card-content-byline-date")

        for post in news_posts:
            date = post.get("title")
            date = date.replace("at ", "").replace("/", "-")
            date = datetime.strptime(date, "%Y-%m-%d %I:%M %p")
            date = date.strftime("%Y-%m-%d %H:%M")
            date += ":00"
            post_dates.append(date)

        return post_dates

    def get_post_links(self):
        print("getting post links")
        post_links = []

        class_news_list = self.soup.find_all(id="main-news-heading")
        news_posts = class_news_list[0].find_all_next(class_="news-list-card-teaser-image")

        for post in news_posts:
            post_links.append((MAIN_URL + post.get("href")).replace("/wow/retail", ""))

        return post_links
