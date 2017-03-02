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



class ArtistCrawlMobile(scrapy.Spider):
    # pdb.set_trace()
    name = "fbm"
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
        global akun,post_id
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
            url = 'https://m.facebook.com/MalinAkermanFanPage/posts/'
            driver.get(url)
            global fb_id
            time.sleep(5)
            try:
                no = 0
                time.sleep(5)
                a = 0
                b = '/div[6]'
                c = '/div[6]'
                d = 0
                for bawah in range(0, 5):
                    if d == a:
                        for i in range(1, 6):
                            a = '/div[' + str(i) + ']'
                            d = a
                            no +=1
                            response = TextResponse(url=url, body=driver.page_source, encoding='utf-8')
                            fb_id = response.xpath('//*[contains(@class, "timelinePublisher async_composer")]/div[1]/@data-store').extract()
                            div = '//*[contains(@class, "_uag")]/'
                            akun = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "m-feed-story-attachments-element")]/header/div[2]/div[1]/div[1]/div[1]/h3/span[1]/strong/a/text()').extract_first()
                            akun2 = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "m-feed-story-attachments-element")]/header/div[2]/div[1]/div[1]/div[1]/h3/strong/a/text()').extract_first()
                            waktu = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "m-feed-story-attachments-element")]/header/div[2]/div[1]/div[1]/div[1]/div[1]/a/abbr/text()').extract_first()
                            post = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "m-feed-story-attachments-element")]/div[1]/span[1]/p/text()').extract_first()
                            like = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "reactions-bling-bar")]/div[1]/div[1]/text()').extract_first()
                            comment = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "reactions-bling-bar")]/div[2]/span[1]/text()').extract_first()
                            share = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "reactions-bling-bar")]/div[2]/span[2]/text()').extract_first()
                            post_id = response.xpath(str(div) + '/div[1]/div[' + str(i) + ']/div[1]/div[1]/article/div[1]/div[1]/div[1]/a/@data-targetid').extract()
                            time.sleep(3)

                            print no

                            fb_id = ''.join(fb_id)
                            fb_id = fb_id.split(":")[1]
                            fb_id = fb_id.split(",")[0]

                            waktu = ''.join(waktu).encode('utf-8')
                            post = ''.join(post).encode('utf-8')
                            like = ''.join(like).encode('utf-8')
                            comment = ''.join(comment).encode('utf-8')
                            share = ''.join(share).encode('utf-8')
                            post_id = ''.join(post_id).encode('utf-8')
                            print "========================================================================================="
                            print fb_id
                            print "========================================================================================="
                            if akun != None:
                                print akun
                            else:
                                akun = akun2
                                print akun
                            print "========================================================================================="
                            print waktu
                            print "========================================================================================="
                            print post_id
                            print "========================================================================================="
                            print post
                            print "========================================================================================="
                            print like
                            print "========================================================================================="
                            print comment
                            print "========================================================================================="
                            print share
                            print "========================================================================================="
                            time.sleep(3)
                            get_react(url,div)

                        a = 1
                    else:
                        for i in range(1, 6):
                            d = c
                            a = '/div[' + str(i) + ']'
                            d = d + a
                            no +=1
                            print d

                            response = TextResponse(url=url, body=driver.page_source, encoding='utf-8')
                            div = '//*[contains(@class, "_uag")]/'
                            fb_id = response.xpath('//*[contains(@id, "timelinePublisher async_composer")]/@data-store').extract()
                            akun = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "m-feed-story-attachments-element")]/header/div[2]/div[1]/div[1]/div[1]/h3/span[1]/strong/a/text()').extract_first()
                            if akun == None:
                                akun1 = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "m-feed-story-attachments-element")]/header/div[2]/div[1]/div[1]/div[1]/h3/strong/a/text()').extract()
                                akun2 = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "m-feed-story-attachments-element")]/header/div[2]/div[1]/div[1]/div[1]/h3/text()').extract()
                                akun3 = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "m-feed-story-attachments-element")]/header/div[2]/div[1]/div[1]/div[1]/h3/a/text()').extract()
                            waktu = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "m-feed-story-attachments-element")]/header/div[2]/div[1]/div[1]/div[1]/div[1]/a/abbr/text()').extract_first()
                            post = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "m-feed-story-attachments-element")]/div[1]/span[1]/p/text()').extract()
                            like = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "reactions-sentence-container")]/div[1]/text()').extract_first()
                            comment = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "reactions-bling-bar")]/div[2]/span[1]/text()').extract_first()
                            share = response.xpath(str(div) + '/div[1]' + d + '//*[contains(@data-sigil, "reactions-bling-bar")]/div[2]/span[2]/text()').extract_first()
                            time.sleep(3)
                            # if no == 9:
                            #     import pdb;pdb.set_trace()
                            print no
                            print "========================================================================================="
                            print fb_id
                            try:
                                ak = str(''.join(akun2[0]))
                                ak1 = str(''.join(akun2[1]))
                                ak2 = ''.join(akun1).encode('utf-8')
                                ak3 = ''.join(akun3).encode('utf-8')
                            except Exception, e:
                                print e
                            print "========================================================================================="
                            if akun != None:
                                print akun
                            else:
                                akun = ak2+ak+ak3+ak1
                                print akun
                            print "========================================================================================="
                            waktu = ''.join(waktu).encode('utf-8')
                            print waktu
                            print "========================================================================================="
                            post = ''.join(post).encode('utf-8')
                            print post
                            print "========================================================================================="
                            like = ''.join(like).encode('utf-8')
                            print like
                            print "========================================================================================="
                            comment = ''.join(comment).encode('utf-8')
                            print comment
                            print "========================================================================================="
                            share = ''.join(share).encode('utf-8')
                            print share
                            print "========================================================================================="
                            get_react(url,div)
                        c = c + b
                    # import pdb;pdb.set_trace()
                    driver.find_element_by_xpath('/html/body').send_keys(Keys.END)
                    time.sleep(5)
                    driver.find_element_by_xpath('/html/body').send_keys(Keys.END)
                    time.sleep(5)
            except Exception, e:
                print e
        except Exception, e:
            print e

def get_react(url,div):
    # Get React
    url = 'https://m.facebook.com/MalinAkermanFanPage/posts/'
    driver.get(url)

    try:
        driver.find_element_by_xpath(str(div) + '/div[1]/div[1]/div[1]/div[1]/article/div[1]/div[2]/div[1]/a').click()
    except Exception, e:
        print e
    time.sleep(3)

    try:
        driver.find_element_by_xpath('//*[contains(@data-sigil, "m-photo-ufi")]/div[1]/div[1]/a').click()
    except Exception, e:
        print e

    time.sleep(3)
    for lk in range(2, 10):
        response = TextResponse(url=url, body=driver.page_source, encoding='utf-8')
        try:
            driver.find_element_by_xpath('//*[contains(@data-sigil, "context-layer-root content-pane")]//*[contains(@class, "scrollAreaColumn")]/span[' + str(lk) + ']').click()
            type = response.xpath('//*[contains(@data-sigil, "context-layer-root content-pane")]//*[contains(@class, "scrollAreaColumn")]/span[' + str(lk) + ']/span').extract()
            type = ''.join(type)
            reaksi = type.split('dengan ')[1]
            reaksi = reaksi.split('\"')[0].encode('utf-8')
            print reaksi
        except Exception, e:
            print e
        time.sleep(3)

        # Get Like
        try:
            for liked in range(1, 100):
                response = TextResponse(url=url, body=driver.page_source, encoding='utf-8')
                inlike = response.xpath('//*[contains(@data-sigil, "context-layer-root content-pane")]/div[1]/div[1]/div[1]/div[2]/div[' + str(lk) + ']/div[1]/div[' + str(liked) + ']/div[1]/div[1]/div[1]/a/div[1]/span/strong/text()').extract()
                if liked % 48 == 0:
                    try:
                        driver.find_element_by_xpath(
                            '//*[contains(@id, "reaction_profile_pager' + str(liked) + '")]/a').click()
                        time.sleep(5)
                    except Exception, e:
                        print e
                        break
                else:
                    pass
                inlike = ''.join(inlike).encode('utf-8')

                if inlike == "":
                    pass
                else:
                    print "===================================+++++++++====================================="
                    print inlike
                    print "===================================+++++++++====================================="
                    # time.sleep(5)
            time.sleep(3)
        except Exception, e:
            print e

    import pdb;pdb.set_trace()
    driver.find_element_by_xpath('').ke
    driver.find_element_by_xpath('/html/body').send_keys(Keys.ALT + Keys.LEFT)
    time.sleep(3)
    driver.find_element_by_xpath('/html/body').send_keys(Keys.CONTROL + "t")
    time.sleep(3)