import csv
import os
import json
import random
from random import randint
import re
import time
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import amazon_creds


class AmazonScrape:

    created_movie_links = []
    movies_poster_links = []
    # USERNAME = "osama_jamil"
    # PASSWORD = "NTFr3NRmrjuT4sC"
    # ENDPOINT = "pr.oxylabs.io:7777"
    # COUNTRY = 'IN'

    # def chrome_proxy(self, user: str, country:str, password: str, endpoint: str) -> dict:
    #     wire_options = {
    #         "proxy": {
    #             "http": f"http://{user}-cc{country}:{password}@{endpoint}",
    #             "https": f"http://{user}-cc{country}:{password}@{endpoint}",
    #         }
    #     }
    #     return wire_options
    
    # def driver_initialize(self):
    #     chrome_options = webdriver.ChromeOptions()
    #     chrome_options.headless = False
    #     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #     chrome_options.add_experimental_option('useAutomationExtension', False)
    #     chrome_options.add_argument("--start-maximized")
    #     chrome_options.add_argument("--no-sandbox")
    #     chrome_options.add_argument("--disable-dev-shm-usage")
    #     chrome_options.add_argument("--disable-notifications")
    #     chrome_options.add_argument('--disable-gpu')
    #     chrome_options.add_argument("--dns-prefetch-disable")
    #     chrome_options.add_argument("--disable-javascript")
    #     chrome_options.add_argument('--ignore-certificate-errors')
    #     chrome_options.add_argument('--ignore-ssh-errors')
    #     proxies = self.chrome_proxy(self.USERNAME, self.PASSWORD, self.COUNTRY, self.ENDPOINT)
    #     driver = webdriver.Chrome(
    #         ChromeDriverManager().install(), options=chrome_options, seleniumwire_options=proxies
    #     )
    #     return driver

    def driver_initialize(self):
        chrome_options = Options()
        ua = UserAgent()
        userAgent = ua.random
        print(userAgent)
        chrome_options.add_argument(f'user-agent={userAgent}')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--dns-prefetch-disable")
        chrome_options.add_argument("--disable-javascript")
        driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
        driver.set_page_load_timeout(300)
        return driver

    def login_site(self):
        driver.get("https://www.primevideo.com/")
        time.sleep(20)
        try:
            driver.find_element(By.XPATH,'//span/a[text()="Sign In"]').click()
        except:
            driver.find_element(By.ID, "pv-nav-accounts").click()
            time.sleep(0.3)
            driver.find_element(By.ID, "pv-nav-sign-in").click()
        time.sleep(5)
        email_id = amazon_creds.email
        email = driver.find_element(By.ID,"ap_email")
        email.clear()
        for word in email_id:
            time.sleep(0.1)
            email.send_keys(word)
        time.sleep(3)
        user_password = amazon_creds.password
        password = driver.find_element(By.ID,"ap_password")
        password.click()
        password.clear()
        time.sleep(2)
        for word in user_password:
            time.sleep(0.1)
            password.send_keys(word)
        time.sleep(5)
        button = driver.find_element(By.XPATH,'//input[@id="signInSubmit"]')
        button.click()

    def scroll_to_bottom(self):
        SCROLL_PAUSE_TIME = 5
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def search_movies(self):
        time.sleep(10)
        categories = driver.find_element(By.XPATH, '//li//span[text()="Categories"]')
        categories.click()
        movies_genere = driver.find_element(By.XPATH, '//ul[@class="cat_columns--2"]/li[@class="categories-li"]/a[text()="Indian TV and movies"]')
        movies_genere.click()
        time.sleep(5)
        amazon.scroll_to_bottom()
        movie_links = driver.find_elements(By.XPATH, '//a[@class="av-beard-title-link"]')
        for link in movie_links:
            full_link= link.get_attribute('href')
            self.created_movie_links.append(full_link)
        movie_posters = driver.find_elements(By.CSS_SELECTOR, 'div[class*="av-grid-packshot"] img')
        for poster in movie_posters:
            full_link= poster.get_attribute('src')
            self.movies_poster_links.append(full_link)

    def scrape_details(self):

        def get_episodes():
            episodes = []
            episodes_list = soup.select('div[id="tab-content-episodes"] ol li')
            for episode in episodes_list:
                episode_name = episode.select_one('span[dir="auto"]').text
                episodes.append(episode_name)
            episodes = ','.join(episodes)
            return episodes

        with open('amazon_movies_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            headers = ['id', 'name', 'year', 'rating', 'imdb_rating', 'popularity', 'summary', 'length', 'genres', 
                'directors', 'actors', 'supporting_actors', 'producers', 'writers', 'studio',  'pg_rating',
                'content_advisory', 'seasons' , 'episodes', 'web_link', 'ios_link', 'android_link', 
                'trailer_url', 'poster_url', 'backdrop_url']
            writer.writerow(headers)
            for idx, link in enumerate(self.created_movie_links):
                poster_URL = self.movies_poster_links[idx]
                director_name = None
                actors = None
                genres = None
                content_advisory = None
                supporting_actors = None
                producers = None
                popularity = None
                rating = None
                writers = None
                studio = None
                seasons = ''
                episodes = ''
                ios_android_deep_link = ''

                url = requests.get(link)
                soup = BeautifulSoup(url.content, 'html.parser')
                web_deep_link = link.split('ref')[0]
                print(web_deep_link)

                synopsis_tag = soup.select_one('div[data-automation-id="atf-synopsis"]')
                if synopsis_tag:
                    synopsis = synopsis_tag.text

                    half_link = link.split('/ref')[0]
                    trailer_link = f"{half_link}/ref=atv_dp_watch_trailer?autoplay=trailer"

                    title_element = soup.select_one('h1[data-automation-id="title"]')
                    if title_element:
                        title = title_element.text
                    else:
                        title_tag = soup.select_one('head title')
                        if title_tag:
                            title = title_tag.text.replace('Prime Video:','')

                    scripts = soup.select('script[type="text/template"]')
                    for script_tag in scripts:
                        text_in_script = script_tag.text
                        if 'pageTitleId' in text_in_script:
                            json_file = json.loads(text_in_script)
                            deep_link_code = json_file['props']['state']['pageTitleId']
                            ios_android_deep_link = f"https://app.primevideo.com/detail?gti={deep_link_code}"
                        
                        json_file = json.loads(text_in_script)
                        title_list = []
                        def get_all_keys(d):
                            for key, value in d.items():
                                if key == 'title':
                                    if 'Season' in value:
                                        if title in value:
                                            print(title,value)
                                            title_list.append(value)
                                if isinstance(value, dict):
                                    yield from get_all_keys(value)
                        for x in get_all_keys(json_file):
                            x = x
                        if len(title_list)>0:
                            seasons_text = str(title_list[-1])
                            if '-' in seasons_text:
                                seasons = seasons_text.split('-')[-1]
                            elif '–' in seasons_text:
                                seasons = seasons_text.split('–')[-1]
                            elif ':' in seasons_text:
                                seasons = seasons_text.split(':')[1]
                            else:
                                seasons_no = seasons_text.split('Season')[1]
                                seasons_no = re.sub(r"\b[a-zA-Z]\b", "", seasons_no)
                                seasons = f"Season {seasons_no}"
                            print(f"Season : {seasons}")
                            episodes = get_episodes()
                        
                        elif soup.select_one('title'):
                            seasons_text = soup.select_one('title').text
                            if 'Season' in seasons_text:
                                if '-' in seasons_text:
                                    seasons = seasons_text.split('-')[-1]
                                    seasons = seasons.split('(')[0]
                                elif '–' in seasons_text:
                                    seasons = seasons_text.split('–')[-1]
                                    seasons = seasons.split('(')[0]
                                elif ':' in seasons_text:
                                    seasons = seasons_text.split(':')[-1]
                                    seasons = seasons.split('(')[0]
                                    seasons_no = seasons_text.split('Season')[1]
                                    seasons_no = re.sub(r"\b[a-zA-Z]\b", "", seasons_no)
                                    seasons = f"Season {seasons_no}"
                                else:
                                    seasons_no = seasons_text.split('Season')[1]
                                    seasons_no = re.sub(r"\b[a-zA-Z]\b", "", seasons_no)
                                    seasons = f"Season {seasons_no}"
                                episodes = get_episodes()
                        
                        elif soup.select_one('meta[name="title]'):
                            print(soup.select_one('meta[name="title]').get("content"))
                            seasons_text = soup.select_one('meta[name="title]').get("content")
                            print(seasons_text)
                            if 'Season' in seasons_text:
                                if '-' in seasons_text:
                                    seasons = seasons_text.split('-')[-1]
                                    seasons = seasons.split('(')[0]
                                elif '–' in seasons_text:
                                    seasons = seasons_text.split('–')[-1]
                                    seasons = seasons.split('(')[0]
                                else:
                                    seasons_no = seasons_text.split('Season')[1]
                                    seasons_no = re.sub(r"\b[a-zA-Z]\b", "", seasons_no)
                                    seasons = f"Season {seasons_no}"
                                print(seasons)
                                episodes = get_episodes()
                                print(f"Episodes C1 {episodes}")
                        elif soup.select_one('h1[data-automation-id="title"]'):
                            season_tag_1 = soup.select_one('h1[data-automation-id="title"]').find_next_sibling('span')
                            if season_tag_1:
                                seasons = season_tag_1.text
                                episodes = get_episodes()
                                print(f"Episodes C2 {episodes}")
                        
                        elif soup.select_one('.av-detail-section span'):
                            seasons_text = soup.select_one('.av-detail-section span span').text
                            if 'Season' in seasons_text:
                                seasons = seasons_text
                                episodes = get_episodes()

                        elif soup.select_one('div.dv-dp-node-playback'):
                            seasons_text = soup.select_one('div.dv-dp-node-playback a').text
                            if 'Season' in seasons_text:
                                seasons = seasons_text.split(',')[0].replace('Play','')
                                episodes = get_episodes()
                        else:
                            seasons = ''
                            episodes = ''

                    pg_rating_tag = soup.select_one('div.av-detail-section span[data-automation-id="rating-badge"] span')
                    if pg_rating_tag:
                        output = pg_rating_tag.text
                        PG_rating = re.sub(r"\b[a-zA-Z]\b", "", output)
                        PG_rating = PG_rating.replace("/",'')
                    else:
                        PG_rating = ''
                    
                    year_tag = soup.select_one('span[data-automation-id="release-year-badge"]')
                    if year_tag:
                        year = year_tag.text
                    else:
                        year = ''

                    imdb_rating_tag = soup.select_one('span[data-automation-id="imdb-rating-badge"]')
                    if imdb_rating_tag:
                        IMDB_rating= imdb_rating_tag.text
                    else:
                        IMDB_rating = ''

                    length_tag = soup.select_one('span[data-automation-id="runtime-badge"]')
                    if length_tag:
                        time = length_tag.text
                        if 'h' in time:
                            hours = time.split('h')[0]
                            if hours:
                                mins = length_tag.text.split('h')[1].replace(" ",'')
                                numeric_filter = filter(str.isdigit, mins)
                                min_string = "".join(numeric_filter)
                                hours_to_mins = int(hours) * 60
                                if min_string != '':
                                    total_minutes = hours_to_mins + int(min_string)
                                else:
                                    total_minutes = hours_to_mins
                                length = f"{total_minutes} Min"
                        else:
                            length = time
                    else:
                        length = ''

                    backdrop_url_tag = soup.select_one('img[id="atf-full"]')
                    if backdrop_url_tag:
                        Backdrop_URL = backdrop_url_tag.attrs['src']
                    else:
                        Backdrop_URL = ''

                    movie_id = link.split('/')[-2]
                    
                    meta_info = soup.select('div[id="meta-info"] div dl')
                    for data in meta_info:
                        heading = data.dt.text
                        if 'Directors' in heading:
                            director_name = data.dd.a.text
                        if 'Starring' in heading:
                            actors = data.dd.text
                        if 'Genres' in heading:
                            genres = data.dd.text

                    info_details = soup.select('div[id="btf-product-details"] div dl')
                    for data in info_details:
                        heading = data.dt.text
                        if 'Directors' in heading:
                            director_name = data.dd.a.text
                        if 'Producers' in heading:
                            producers = data.dd.text
                        if 'Studio' in heading or 'Network' in heading:
                            studio = data.dd.text
                        if 'Content advisory' in heading:
                            content_advisory = data.dd.text
                        if 'Supporting actors' in heading:
                            supporting_actors = data.dd.text

                    # print(
                    #     f"""
                    #         Movie ID : {movie_id}
                    #         Title : {title}, 
                    #         Year : {year},
                    #         IMDB_rating : {IMDB_rating},
                    #         Synopsis : {synopsis},
                    #         length : {length},
                    #         genres : {genres},
                    #         director Name : {director_name},
                    #         actors : {actors},
                    #         supporting_actors : {supporting_actors}
                    #         Producers : {producers},
                    #         Studio : {studio},
                    #         PG_rating : {PG_rating}
                    #         content_advisory : {content_advisory}
                    #         seasons : {seasons}
                    #         episodes : {episodes}
                    #         web deep link : {link},
                    #         ios android deep link : {ios_android_deep_link}
                    #         trailer_link : {trailer_link},
                    #         poster url : {poster_URL}
                    #         Backdrop URL : {Backdrop_URL}
                    #     """
                    # )

                    data = ([movie_id , title, year, rating, IMDB_rating, popularity, synopsis, length, genres, director_name, 
                        actors, supporting_actors, producers, writers, studio, PG_rating, content_advisory, seasons, episodes, 
                        web_deep_link, ios_android_deep_link, ios_android_deep_link, trailer_link, poster_URL, Backdrop_URL])
                    
                    writer.writerow(data)
        file.close()

def main():
    amazon.login_site()
    amazon.search_movies()
    amazon.scrape_details()
    
if __name__ == "__main__":
    driver = webdriver.Chrome()
    amazon = AmazonScrape()
    driver = amazon.driver_initialize()
    main()