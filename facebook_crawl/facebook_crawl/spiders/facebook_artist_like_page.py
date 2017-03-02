import json
import scrapy
import MySQLdb
import time
import datetime
import re
import config
from selenium.webdriver.common.proxy import *
from array import *
from kafka import KafkaProducer, KafkaConsumer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.http import TextResponse
from pyvirtualdisplay import Display



class LikesCrawl(scrapy.Spider):
    # pdb.set_trace()
    name = "fbl"
    allowed_domains = ["http://www.facebook.com"]
    start_urls = ["http://www.facebook.com"]

    def __init__(self):
        # self.connect = self.conn
        path_to_chromedriver = 'D://chromedriver'
        # path = 'C:\Program Files\Mozilla Firefox\Firefox'
        # path_to_chromedriver='/usr/local/bin/chromedriver'
        # self.driver = webdriver.Chrome(executable_path=path_to_chromedriver)
        # display = Display(visible=False, size=(800, 600))
        # display.start()

        # Setting proxy webdriver

        # chrome_option = webdriver.ChromeOptions()
        # chrome_option.add_argument("--proxy-server=192.168.150.191 :3128")
        # self.driver = webdriver.Chrome(executable_path=path_to_chromedriver,chrome_options=chrome_option)
        self.driver = webdriver.Chrome(executable_path=path_to_chromedriver)
        # self.driver = webdriver.Firefox(executable_path=path)
        # self.driver = webdriver.PhantomJS()

    # Login facebook
    def start_requests(self):
        # Setting MySQL
        db = MySQLdb.connect(host="192.168.20.86", port=3306, user="root", passwd="rahasia2016", db="mm_cloud")
        cursor = db.cursor()
        sql = "select fb_id from fb_subs"
        cursor.execute(sql)
        results = cursor.fetchall()

        time.sleep(10)
        try:
            self.driver.get('http://www.facebook.com')

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
            self.driver.find_element_by_xpath('//*[@id="u_0_l"]').click()
            #//*[@id="u_0_l"]
            time.sleep(3)

            for fb in range(len(results)):
                url = results[fb]
                url = 'https://www.facebook.com/'+str(url).replace('(', '').replace(')', '').replace('\'', '').replace(',', '')
                self.driver.get(url)
                coy = self.driver.current_url
                coy1 = coy.split("?")[0].encode('utf-8')
                url = coy1 + 'likes'
                self.driver.get(url)
                # import pdb;pdb.set_trace()
                try:
                    response = TextResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
                    get_fb_id = response.xpath('//*[@id="facebook"]/head/meta[5]').extract()
                    get_fb_id = ''.join(get_fb_id).encode('utf-8')
                    get_likes_page = response.xpath('//*[contains(@class, "_5cuj")]/div[1]/text()').extract()
                    fb_id = re.findall('\d+', get_fb_id)
                    fb_id = ''.join(fb_id)
                    now = datetime.datetime.now()
                    waktu = now.strftime("%Y-%m-%d %H:%M")
                    fb_likes_page = ''.join(get_likes_page).encode('utf-8').replace(".","")

                    print "============================================================================================="
                    print fb_id
                    print "============================================================================================="
                    print waktu
                    print "============================================================================================="
                    print fb_likes_page
                    print "============================================================================================="
                except Exception, e:
                    pass
        except Exception, e:
            print e

