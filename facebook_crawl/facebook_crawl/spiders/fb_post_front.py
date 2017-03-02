import json
import scrapy
import MySQLdb
import time
import datetime

from array import *
from kafka import KafkaProducer, KafkaConsumer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.http import TextResponse
from pyvirtualdisplay import Display


class InputFB(scrapy.Spider):
    # pdb.set_trace()
    name = "fbtest"
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
        sql = "select URL from artist"
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

            # for fb in range(len(results)):
            #     url = results[fb]
            #     url = str(url).replace('(', '').replace(')', '').replace('\'', '').replace(',', '').replace('https://www', 'https://mobile') + 'posts?'
            #     driver.get(url)
            # import pdb;pdb.set_trace()
            url = 'https://m.facebook.com/MalinAkermanFanPage/'
            driver.get(url)
            count = 0
            response = TextResponse(url=url, body=driver.page_source, encoding='utf-8')
            fb_image = response.xpath('//*[contains(@class, "bm bn bo")]/a/img/@src').extract()
            fb_image = ''.join(fb_image).encode('utf-8')

            for year in range(3, 10):
                driver.find_element_by_xpath('//*[contains(@id, "structured_composer_async_container")]/div[' + str(year) + ']/a').click()
                firstpost = driver.current_url
                for nextpage in range(1,10000):
                    for i in range(1,6):
                        count +=1
                        print count
                        # import pdb;pdb.set_trace()
                        # Get facebook content
                        response = TextResponse(url=url, body=driver.page_source, encoding='utf-8')
                        fb_id = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[1]/div[1]/h3/span/strong/a/@href').extract()
                        fb_id = ''.join(fb_id).encode('utf-8')
                        if fb_id == "":
                            fb_id = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[1]/div[1]/h3/strong/a/@href').extract()
                            fb_id = ''.join(fb_id).encode('utf-8')
                        fb_account = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[1]/div[1]/h3/span/strong/a/text()').extract()
                        fb_account = ''.join(fb_account).encode('utf-8')
                        if fb_account == "":
                            fb_account1 = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[1]/div[1]/h3/strong/a/text()').extract()
                            fb_account2 = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[1]/div[1]/h3/text()').extract()
                            fb_account3 = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[1]/div[1]/h3/a/text()').extract()
                        fb_post_id = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[1]/div[1]/h3/span/strong/a/@href').extract()
                        fb_post_id = ''.join(fb_post_id).encode('utf-8')
                        if fb_post_id == "":
                            fb_post_id = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[1]/div[1]/h3/strong/a/@href').extract()
                            fb_post_id = ''.join(fb_post_id).encode('utf-8')
                        fb_post = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[1]/div[2]/span/p/text()').extract()
                        fb_post_date = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[2]/div[1]/abbr/text()').extract()
                        like = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[2]/div[2]/span/a/text()').extract()
                        comment = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[2]/div[2]/a/text()').extract()
                        linkv = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[1]/div[3]/div[1]/div[1]/a/@href').extract()
                        link = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[1]/div[3]/a/@href').extract()

                        # Parsing from list to string
                        fb_id = fb_id.split('%')[2]
                        fb_id = fb_id.split('.')[1]

                        try:
                            fb_acc = ''.join(fb_account1).encode('utf-8')
                            fb_acc1 = ''.join(fb_account3).encode('utf-8')
                            fb_acc2 = str(''.join(fb_account2[0]))
                            fb_acc3 = str(''.join(fb_account2[1]))
                            story = fb_acc+fb_acc2+fb_acc1+fb_acc3
                        except:
                            pass

                        fb_post_id = fb_post_id.split('%')[0]
                        fb_post_id = fb_post_id.split('.')[1]

                        fb_post = ''.join(fb_post).encode('utf-8')

                        # import pdb;pdb.set_trace()
                        fb_post_date = ''.join(fb_post_date).encode('utf-8').split(' ')
                        now = datetime.datetime.now()
                        waktu = now.strftime("%Y-%m-%d").split('-')
                        year = fb_post_date[2]
                        month = fb_post_date[1]
                        day = fb_post_date[0]
                        if ":" in year:
                            year = waktu[0]
                        if day == "Kemarin":
                            day = str(int(waktu[2])-1)
                        like = ''.join(like).encode('utf-8')
                        like = like.split('Suka')[0]

                        comment = ''.join(comment).encode('utf-8')
                        comment = comment.split(' ')[0]
                        linkv = ''.join(linkv).encode('utf-8')
                        if linkv != "":
                            try:
                                linkv = "m.facebook.com"+linkv
                            except:
                                pass

                        try:
                            link = ''.join(link).encode('utf-8')
                            link = link
                        except:
                            pass

                        if fb_post != "":
                            type = "status"
                        elif linkv != "":
                            type = "video"
                        else:
                            type = "link"

                        id = fb_id+"_"+fb_post_id

                        print "================================================================================================="
                        print id
                        print "================================================================================================="
                        print fb_id
                        print "================================================================================================="
                        if fb_account != "":
                            print fb_account
                        else:
                            fb_account = fb_acc
                            print fb_account
                        print "================================================================================================="
                        print story
                        print "================================================================================================="
                        print fb_post_id
                        print "================================================================================================="
                        print fb_post
                        print "================================================================================================="
                        print fb_post_date
                        print "================================================================================================="
                        if linkv != "":
                            print linkv
                            print "================================================================================================="
                        else:
                            pass
                        if link != "":
                            print link
                            print "================================================================================================="
                        else:
                            pass
                        print type
                        print "================================================================================================="
                        print like
                        print "================================================================================================="
                        print comment
                        print "================================================================================================="
                        print year
                        print month
                        print day

                        time.sleep(3)

                        total = json.dumps(
                            {'type': 'post_front', 'fb_id': fb_id, 'id': id, 'from': fb_account,
                             'fb_status_id': fb_post_id, 'comment_from_id': "", 'like_from_id': "",
                             'caption': link, 'desc': story, 'created_at': fb_post_date,
                             'fb_type': type, 'crawler_id': "Indonesia001", 'fb_image': fb_image,
                             'd_year': year, 'd_month': month, 'd_day': day, 'is_comment': 0,
                             'message': fb_post})
                        print total
                        # try:
                        #     for kafka in range(0, 20):
                        #         try:
                        #             # import pdb; pdb.set_trace()
                        #             prod = KafkaProducer(
                        #                 bootstrap_servers=['master01.cluster1.ph:6667', 'namenode01.cluster1.ph:6667',
                        #                                    'namenode02.cluster1.ph:6667'])
                        #             prod.send('crawl_facebook', b"{}".format(total))
                        #             print "=================================================="
                        #             print "SUKSES SEND TO KAFKA"
                        #             print "=================================================="
                        #             print total
                        #             kafka = 1
                        #         except:
                        #             pass
                        #         if kafka == 1:
                        #             break
                        # except Exception, e:
                        #     print e
                    # this year
                    nextyear = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[2]/a/text()').extract()
                    nextyear = ''.join(nextyear).encode('utf-8')
                    if nextyear == "Tampilkan lainnya":
                        driver.find_element_by_xpath('//*[contains(@id, "structured_composer_async_container")]/div[2]/a').click()
                    else:
                        break
                    time.sleep(1)

                # driver.get(url)
                time.sleep(1)
        except Exception, e:
            print e