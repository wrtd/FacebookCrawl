import json
import scrapy
import MySQLdb
import time

from array import *
from kafka import KafkaProducer, KafkaConsumer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.http import TextResponse
from pyvirtualdisplay import Display



class ScrapyDoo(scrapy.Spider):
    # pdb.set_trace()
    name = "fbmm"
    allowed_domains = ["https://m.facebook.com"]
    start_urls = ["https://m.facebook.com"]

    def __init__(self):
        # self.connect = self.conn
        path_to_chromedriver = 'D://chromedriver'
        # path = 'C:\Program Files\Mozilla Firefox\Firefox'
        # path_to_chromedriver='/usr/local/bin/chromedriver'
        # self.driver = webdriver.Chrome(executable_path=path_to_chromedriver)
        # display = Display(visible=False, size=(800, 600))
        # display.start()
        self.driver = webdriver.Chrome(executable_path=path_to_chromedriver)
        # self.driver = webdriver.Firefox(executable_path=path)
        # self.driver = webdriver.PhantomJS()

    # Login facebook
    def start_requests(self):
        db = MySQLdb.connect(host="192.168.20.37", port=3360, user="root", passwd="rahasia2016", db="facebook")
        cursor = db.cursor()
        sql = "select URL from artist"
        cursor.execute(sql)
        results = cursor.fetchall()

        time.sleep(10)
        try:
            self.driver.get('https://m.facebook.com')

            # Username
            email = self.driver.find_element_by_name('email')
            email.click()
            email.send_keys("blcklst.mthrfckrs@yahoo.com")
            time.sleep(5)

            # Password
            password = self.driver.find_element_by_name('pass')
            password.click()
            password.send_keys("mthrfckrs")
            time.sleep(3)

            # Login Button
            self.driver.find_element_by_name('login').click()
            time.sleep(3)
            try:
                self.driver.find_element_by_xpath('//*[contains(@id, "page")]//*[contains(@method, "post")]/div[1]/button').click()
                time.sleep(3)
            except:
                pass

            # for fb in range(len(results)):
            #     url = results[fb]
            #     url = str(url).replace('(', '').replace(')', '').replace('\'', '').replace(',', '').replace('https://www', 'https://mobile') + 'posts?'
            #     self.driver.get(url)
            # import pdb;pdb.set_trace()
            url = 'https://m.facebook.com/MalinAkermanFanPage/posts/'
            self.driver.get(url)
            time.sleep(5)
            self.driver.find_element_by_xpath('/html/body').send_keys(Keys.END)
            time.sleep(5)
            self.driver.find_element_by_xpath('/html/body').send_keys(Keys.END)
            time.sleep(5)
            self.driver.find_element_by_xpath('/html/body').send_keys(Keys.END)
            time.sleep(5)
            self.driver.find_element_by_xpath('/html/body').send_keys(Keys.END)
            time.sleep(5)
            self.driver.find_element_by_xpath('/html/body').send_keys(Keys.END)
            time.sleep(5)
            response = TextResponse(url=url, body=self.driver.page_source, encoding='utf-8')
            try:
                div = '//*[contains(@class, "_uag")]/'
                akun2 = response.xpath(str(div) + '/div[1]/div[6]/div[4]//*[contains(@data-sigil, "m-feed-story-attachments-element")]/header/div[2]/div[1]/div[1]/div[1]/h3/strong/a/text()').extract_first()
            except Exception, e:
                pass
            print akun2
        except Exception, e:
            print e