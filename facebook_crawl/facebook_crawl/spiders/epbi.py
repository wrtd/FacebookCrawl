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



class CrawlFBFB(scrapy.Spider):
    # pdb.set_trace()
    name = "asd"
    allowed_domains = ["https://m.facebook.com"]
    start_urls = ["https://m.facebook.com"]

    def __init__(self):
        global driver
        # self.connect = self.conn
        # path_to_chromedriver = 'D://chromedriver'
        path = 'C://Program Files//Mozilla Firefox//firefox'
        # path_to_chromedriver='/usr/local/bin/chromedriver'
        # driver = webdriver.Chrome(executable_path=path_to_chromedriver)
        # display = Display(visible=False, size=(800, 600))
        # display.start()

        # driver = webdriver.Chrome(executable_path=path_to_chromedriver)
        driver = webdriver.Firefox(executable_path=path)
        # driver = webdriver.PhantomJS()

    # Login facebook
    def start_requests(self):
        db = MySQLdb.connect(host="192.168.20.37", port=3360, user="root", passwd="rahasia2016", db="facebook")
        cursor = db.cursor()
        sql = "select URL from malaysia"
        cursor.execute(sql)
        results = cursor.fetchall()

        time.sleep(10)
        try:
            driver.get('https://m.facebook.com')

            # Username
            email = driver.find_element_by_name('email')
            email.click()
            email.send_keys("blcklst.mthrfckrs@yahoo.com")
            time.sleep(5)

            # Password
            password = driver.find_element_by_name('pass')
            password.click()
            password.send_keys("mthrfckrs")
            time.sleep(3)

            # Login Button
            driver.find_element_by_name('login').click()
            time.sleep(3)
            try:
                driver.find_element_by_xpath('//*[contains(@id, "page")]//*[contains(@method, "post")]/div[1]/button').click()
                time.sleep(3)
            except:
                pass

            for fb in range(len(results)):
                url = results[fb]
                url = str(url).replace('(', '').replace(')', '').replace('\'', '').replace(',', '')
                driver.get(url)
                # import pdb;pdb.set_trace()
                response = TextResponse(driver.current_url, body=driver.page_source, encoding='utf-8')

                name = response.xpath('//*[contains(@id, "pages_navigation")]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/a/text()').extract()
                name = ''.join(name).encode('utf-8')
                if name != "":
                    print "============================================================================================"
                    print "Success"
                    status = "Success"
                    cursor = db.cursor()
                    sql = "UPDATE malaysia SET status = '{}' WHERE URL = '{}'".format(status, url)
                    cursor.execute(sql)
                    db.commit()
                    print "============================================================================================"
                else:
                    print "============================================================================================"
                    print "Fail"
                    status = "Fail"
                    sql = "UPDATE malaysia SET status = '{}' WHERE URL = '{}'".format(status, url)
                    cursor.execute(sql)
                    db.commit()
                    print "============================================================================================"
        except Exception, e:
            print e