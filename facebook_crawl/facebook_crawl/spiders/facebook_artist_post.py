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



class ArtistCrawl(scrapy.Spider):
    # pdb.set_trace()
    name = "test"
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
                url = str(url).replace('(', '').replace(')', '').replace('\'', '').replace(',', '') + 'posts?'
                self.driver.get(url)
                try:
                    # kiriman = '//*[contains(@class,"_1xnd")]/div['+ str(fb) +']/div[1]/span[2]/a'
                    # # kiriman = '//*[contains(@class, "_5ss8")]/div[1]/div[4]/a[2]'
                    # self.driver.find_element_by_xpath(kiriman).click()
                    time.sleep(5)
                    a = 0
                    b = '/div[9]'
                    c = '/div[9]'
                    d = 0
                    for bawah in range (0,1000):
                        no = 0
                        if d == a:
                            for i in range(1,9):
                                a = '/div[' + str(i) + ']'
                                d = a
                                response = TextResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
                                no+=1
                                first = '//*[contains(@class, "_1qkq _1qkx")]/'
                                print no
                                akun1 = response.xpath(str(first) + '/div[2]/div[1]' + str(d) + '//*[contains(@class, "userContentWrapper")]//*[contains(@class, "fwn fcg")]/span[1]/a/text()').extract()
                                akun2 = response.xpath(str(first) + '/div[2]/div[1]' + str(d) + '//*[contains(@class, "userContentWrapper")]//*[contains(@class, "fwn fcg")]/span[1]/span[1]/a/text()').extract()
                                waktu = response.xpath(str(first) + '/div[2]/div[1]' + str(d) + '//*[contains(@class, "userContentWrapper")]//*[contains(@class, "fsm fwn fcg")]/a/abbr/@title').extract()
                                post = response.xpath(str(first) + '/div[2]/div[1]' + str(d) + '//*[contains(@class, "userContentWrapper")]//*[contains(@class, "_5pbx userContent")]/div[1]/p/text()').extract()
                                post2 = response.xpath(str(first) + '/div[2]/div[1]' + str(d) + '//*[contains(@class, "userContentWrapper")]//*[contains(@class, "fwn fcg")]/span[1]/text()').extract()
                                article = response.xpath(str(first) + '/div[2]/div[1]' + str(d) + '//*[contains(@class, "userContentWrapper")]//*[contains(@class, "mtm")]/div[1]/div[1]/div[1]/span[1]/div[2]/a/@href').extract()
                                like = response.xpath(str(first) + '/div[2]/div[1]' + str(d) + '//*[contains(@class, "userContentWrapper")]/div[2]/form//*[contains(@class, "uiUfi UFIContainer")]//*[contains(@class, "UFIRow UFILikeSentence")]/div[1]/div[2]/div[1]/div[1]/div[1]/a/span[2]/span[1]/text()').extract_first()
                                comment = response.xpath(str(first) + '/div[2]/div[1]' + str(d) + '//*[contains(@class, "userContentWrapper")]/div[2]/form//*[contains(@class, "uiUfi UFIContainer")]//*[contains(@class, "fcg UFIPagerCount")]/em/text()').extract_first()
                                shared = response.xpath(str(first) + '/div[2]/div[1]' + str(d) + '//*[contains(@class, "userContentWrapper")]/div[2]/form//*[contains(@class, "uiUfi UFIContainer")]//*[contains(@class, "UFIRow UFIShareRow")]/a/em/text()').extract_first()
                                try:
                                    akun1 = akun1
                                    akun1 = ''.join(akun1).encode('utf-8')
                                    akun2 = akun2
                                    akun2 = ''.join(akun2).encode('utf-8')
                                except Exception, e:
                                    print e

                                if akun1 != "":
                                    print "============================================================"
                                    print akun1
                                else:
                                    print "============================================================"
                                    akun1 = akun2
                                    print akun1
                                try:
                                    waktu = waktu
                                    waktu = ''.join(waktu).encode('utf-8')
                                except Exception, e:
                                    print e
                                try:
                                    post = post[0]
                                    post = ''.join(post).encode('utf-8')
                                except:
                                    post = post

                                try:
                                    post2 = ''.join(post2).encode('utf-8')
                                except:
                                    post2 = post2

                                try:
                                    article = ''.join(article).encode('utf-8')
                                except:
                                    article = article

                                if "," in like:
                                    like = ''.join(like).replace(",", "").replace(" rb", "00")
                                else:
                                    like = ''.join(like).replace(" rb", "000")

                                print "============================================================"
                                print waktu
                                print "============================================================"
                                if post != []:
                                    print post
                                    print "============================================================"
                                else:
                                    pass
                                print post2
                                print "============================================================"
                                if article != "":
                                    print article
                                    print "============================================================"
                                else:
                                    pass
                                print like
                                print "============================================================"
                                try:
                                    comment = ''.join(comment).split(" ")
                                    print comment[2]
                                except Exception, e:
                                    print e
                                print "============================================================"
                                try:
                                    shared = ''.join(shared).split(" ")
                                    print shared[0]
                                except Exception, e:
                                    print e
                                print "============================================================"
                                time.sleep(3)
                            a = 1
                        else:
                            for i in range(1,9):
                                d = c
                                a = '/div[' + str(i) + ']'
                                d = d+a

                                no +=1
                                print no
                                response = TextResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
                                # first = '//*[contains(@class, "_1qkq _1qkx")]/'
                                akun1 = response.xpath(str(first) + '/div[2]/div[1]' + d + '//*[contains(@class, "userContentWrapper")]//*[contains(@class, "fwn fcg")]/span[1]/a/text()').extract()
                                akun2 = response.xpath(str(first) + '/div[2]/div[1]' + d + '//*[contains(@class, "userContentWrapper")]//*[contains(@class, "fwn fcg")]/span[1]/span[1]/a/text()').extract()
                                waktu = response.xpath(str(first) + '/div[2]/div[1]' + d + '//*[contains(@class, "userContentWrapper")]//*[contains(@class, "fsm fwn fcg")]/a/abbr/@title').extract()
                                post = response.xpath(str(first) + '/div[2]/div[1]' + d + '//*[contains(@class, "userContentWrapper")]//*[contains(@class, "_5pbx userContent")]/div[1]/p/text()').extract()
                                post2 = response.xpath(str(first) + '/div[2]/div[1]' + d + '//*[contains(@class, "userContentWrapper")]//*[contains(@class, "fwn fcg")]/span[1]/text()').extract()
                                article = response.xpath(str(first) + '/div[2]/div[1]' + d + '//*[contains(@class, "userContentWrapper")]//*[contains(@class, "mtm")]/div[1]/div[1]/div[1]/span[1]/div[2]/a/@href').extract()
                                like = response.xpath(str(first) + '/div[2]/div[1]' + d + '//*[contains(@class, "userContentWrapper")]/div[2]/form//*[contains(@class, "uiUfi UFIContainer")]//*[contains(@class, "UFIRow UFILikeSentence")]/div[1]/div[2]/div[1]/div[1]/div[1]/a/span[2]/span[1]/text()').extract_first()
                                comment = response.xpath(str(first) + '/div[2]/div[1]' + d + '//*[contains(@class, "userContentWrapper")]/div[2]/form//*[contains(@class, "uiUfi UFIContainer")]//*[contains(@class, "fcg UFIPagerCount")]/em/text()').extract_first()
                                shared = response.xpath(str(first) + '/div[2]/div[1]' + d + '//*[contains(@class, "userContentWrapper")]/div[2]/form//*[contains(@class, "uiUfi UFIContainer")]//*[contains(@class, "UFIRow UFIShareRow")]/a/em/text()').extract_first()
                                # import pdb;pdb.set_trace()
                                try:
                                    akun1 = akun1
                                    akun1 = ''.join(akun1).encode('utf-8')
                                    akun2 = akun2
                                    akun2 = ''.join(akun2).encode('utf-8')
                                except Exception, e:
                                    print e

                                if akun1 != "":
                                    print "============================================================"
                                    print akun1
                                else:
                                    print "============================================================"
                                    akun1 = akun2
                                    print akun1
                                try:
                                    waktu = waktu
                                    waktu = ''.join(waktu).encode('utf-8')
                                except Exception, e:
                                    print e
                                try:
                                    post = post[0]
                                    post = ''.join(post).encode('utf-8')
                                except:
                                    post = post

                                try:
                                    post2 = ''.join(post2).encode('utf-8')
                                except:
                                    post2 = post2

                                try:
                                    article = ''.join(article).encode('utf-8')
                                except:
                                    article = article

                                if "," in like:
                                    like = ''.join(like).replace(",", "").replace(" rb", "00")
                                else:
                                    like = ''.join(like).replace(" rb", "000")

                                print "============================================================"
                                print waktu
                                print "============================================================"
                                if post != []:
                                    print post
                                    print "============================================================"
                                else:
                                    pass
                                print post2
                                print "============================================================"
                                if article != "":
                                    print article
                                    print "============================================================"
                                else:
                                    pass
                                print like
                                print "============================================================"
                                try:
                                    comment = ''.join(comment).split(" ")
                                    print comment[2]
                                except Exception, e:
                                    print e
                                print "============================================================"
                                try:
                                    shared = ''.join(shared).split(" ")
                                    print shared[0]
                                except Exception, e:
                                    print e
                                print "============================================================"
                                time.sleep(3)
                            c = c+b
                        time.sleep(3)
                        self.driver.find_element_by_xpath('/html/body').send_keys(Keys.END)
                        time.sleep(5)
                        total = json.dumps({'type': 'post', 'from': akun1, 'created_at': waktu, 'message': posting, 'caption': article,
                             'is_like': like, 'is_comment': comment})
                        try:
                            for kafka in range(0, 20):
                                try:
                                    # import pdb; pdb.set_trace()
                                    prod = KafkaProducer(
                                        bootstrap_servers=['master01.cluster1.ph:6667', 'namenode01.cluster1.ph:6667',
                                                           'namenode02.cluster1.ph:6667'])
                                    prod.send('crawl_facebook', b"{}".format(total))
                                    print "=================================================="
                                    print "SUKSES SEND TO KAFKA"
                                    print "=================================================="
                                    print total
                                    kafka = 1
                                except:
                                    pass
                                if kafka == 1:
                                    break
                        except Exception, e:
                            print e
                except Exception, e:
                    pass
        except Exception, e:
            print e

