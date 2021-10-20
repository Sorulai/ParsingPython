# Вариант I
# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и
# сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172???

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from datetime import date, timedelta, datetime


class MongoDb:
    client = MongoClient('127.0.0.1', 27017)

    def __init__(self, name, collection):
        db = self.client[name]
        self.mail_db = db[collection]

    def add_to_db(self, dictionary):
        self.mail_db.insert_one(dictionary)


class SeleniumMailRu:
    options = Options()

    def __init__(self, url, mongo_name, mongo_collection, path='chromedriver.exe', ):
        self.url = url
        self.driver = webdriver.Chrome(executable_path=path, options=self.options_window())
        self.wait = WebDriverWait(self.driver, 10)
        self.links_list = []
        self.mail_db = MongoDb(mongo_name, mongo_collection)

    def options_window(self, arg='start-maximized'):
        self.options.add_argument(arg)
        return self.options

    def auth_mail(self, email_key='study.ai_172@mail.ru', pass_key='NextPassword172???'):
        self.driver.get(self.url)
        elem = self.driver.find_element(By.CLASS_NAME, 'email-input')
        elem.send_keys(email_key)
        elem.send_keys(Keys.ENTER)
        elem = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'password-input')))
        elem.send_keys(pass_key)
        elem.send_keys(Keys.ENTER)

    def create_links_arr(self):
        flag = True
        while flag:
            mails = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="dataset__items"]/a')))
            for i in mails:
                link_profile = i.get_attribute('href')
                if link_profile is None:
                    flag = False
                elif link_profile in self.links_list:
                    continue
                else:
                    self.links_list.append(link_profile)

            actions = ActionChains(self.driver)
            actions.move_to_element(mails[-1])
            actions.perform()

        return self.links_list

    def add_to_db(self):
        now = 'Cегодня'
        yesterday = 'Вчера'
        for el in self.create_links_arr():
            data = {}
            self.driver.get(el)
            el_text = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__body'))).text
            el_contact = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact'))).text
            el_title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject'))).text
            el_date = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__date'))).text

            if now in el_date:
                el_date = el_date.replace(now, date.today())
            elif yesterday in el_date:
                yester = datetime.now() - timedelta(1)
                el_date = el_date.replace(yesterday, datetime.strftime(yester, '%Y-%m-%d'))

            data['contact'] = el_contact
            data['date'] = el_date
            data['title'] = el_title
            data['text'] = el_text

            self.mail_db.add_to_db(data)

    def composition(self):
        self.auth_mail()
        self.create_links_arr()
        self.add_to_db()
        self.__del__()

    def __del__(self):
        self.driver.close()
        del self.driver


sel = SeleniumMailRu(url='https://mail.ru/', mongo_name='DbMail', mongo_collection='mails')
sel.composition()
