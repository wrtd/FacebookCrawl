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



class ArtistCrawlMobileFirefox(scrapy.Spider):
    # pdb.set_trace()
    name = "fbmf"
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

                        # Parsing from list to string
                        fb_id = fb_id.split('%')[2]
                        fb_id = fb_id.split('.')[1]

                        try:
                            fb_acc = ''.join(fb_account1).encode('utf-8')
                            fb_acc1 = ''.join(fb_account3).encode('utf-8')
                            fb_acc2 = str(''.join(fb_account2[0]))
                            fb_acc3 = str(''.join(fb_account2[1]))
                        except:
                            pass

                        fb_post_id = fb_post_id.split('%')[0]
                        fb_post_id = fb_post_id.split('.')[1]

                        fb_post = ''.join(fb_post).encode('utf-8')

                        fb_post_date = ''.join(fb_post_date).encode('utf-8')

                        like = ''.join(like).encode('utf-8')
                        like = like.split('Suka')[0]

                        comment = ''.join(comment).encode('utf-8')
                        comment = comment.split(' ')[0]

                        print "================================================================================================="
                        print fb_id
                        print "================================================================================================="
                        if fb_account != "":
                            print fb_account
                        else:
                            fb_account = fb_acc+fb_acc2+fb_acc1+fb_acc3
                            print fb_account
                        print "================================================================================================="
                        print fb_post_id
                        print "================================================================================================="
                        print fb_post
                        print "================================================================================================="
                        print fb_post_date
                        print "================================================================================================="
                        print like
                        print "================================================================================================="
                        print comment
                        print "================================================================================================="
                        time.sleep(3)

                        # Klik Like
                        import pdb;pdb.set_trace()
                        driver.find_element_by_xpath('//*[contains(@id, "structured_composer_async_container")]/div[1]/div[2]/div[1]/div[' + str(i) + ']/div[2]/div[2]/span/a').click()
                        try:
                            driver.find_element_by_xpath('//*[contains(@id, "ufi")]/div[1]/div[1]/a').click()
                        except:
                            driver.find_element_by_xpath('//*[contains(@id, "ufi")]/div[1]/div[2]/a').click()

                        no = 0
                        for nextreact in range(1, 1000):
                            counter = 0
                            for lk in range(1, 11):
                                counter +=1
                                no +=1
                                response = TextResponse(driver.current_url, body=driver.page_source, encoding='utf-8')
                                try:
                                    id_suka = response.xpath('//ul[@class="be"]/li[' + str(lk) + ']/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td[3]/div/h3/a/@href').extract()
                                    id_suka = ''.join(id_suka).encode('utf-8')
                                    id_suka = id_suka.split('=')[1]
                                except:
                                    pass
                                reaction = response.xpath('//ul[@class="be"]/li[' + str(lk) + ']/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td[2]/img/@alt').extract()
                                reaction = ''.join(reaction).encode('utf-8')
                                suka = response.xpath('//ul[@class="be"]/li[' + str(lk) + ']/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td[3]/div/h3/a/text()').extract()
                                suka = ''.join(suka).encode('utf-8')
                                if reaction != "":
                                    print no
                                    print "================================================================================================="
                                    print id_suka
                                    print "================================================================================================="
                                    print reaction
                                    print "================================================================================================="
                                    print suka
                                    print "================================================================================================="
                                else:
                                    break

                            if counter > 8:
                                try:
                                    driver.find_element_by_xpath('//ul[@class="be"]/li[9]/table/tbody/tr/td/div/a').click()
                                except:
                                    try:
                                        driver.find_element_by_xpath('//ul[@class="be"]/li[10]/table/tbody/tr/td/div/a').click()
                                    except:
                                        try:
                                            driver.find_element_by_xpath('//ul[@class="be"]/li[11]/table/tbody/tr/td/div/a').click()
                                        except:
                                            break
                            else:
                                break
                            time.sleep(1)
                        driver.get(firstpost)

                    # this year
                    nextyear = response.xpath('//*[contains(@id, "structured_composer_async_container")]/div[2]/a/text()').extract()
                    nextyear = ''.join(nextyear).encode('utf-8')
                    if nextyear != "":
                        driver.find_element_by_xpath('//*[contains(@id, "structured_composer_async_container")]/div[2]/a').click()
                    else:
                        break
                time.sleep(1)

                driver.get(url)
                time.sleep(1)
        except Exception, e:
            print e