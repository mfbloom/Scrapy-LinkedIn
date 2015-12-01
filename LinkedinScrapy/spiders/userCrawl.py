import scrapy
from scrapy.spiders import BaseSpider
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import FormRequest
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from LinkedinScrapy.items import LinkedinScrapyItem

#from spider.settings import JsonWriterPipeline
    
class userCrawl (CrawlSpider):
    name = 'userCrawl'
    allowed_domains = ['linkedin.com']
    login_page = 'https://linkedin.com/uas/login'
    start_urls = ['https://linkedin.com/uas/login']
    
    def start_requests(self):
        return self.init_request()

    def init_request(self):
        #"""This function is called before crawling starts."""
        return [Request(url=self.login_page, callback=self.login)]
    
    def login(self, response):
        print "****LOGIN function*****"
        return [FormRequest.from_response(response, formname='login_form',
                    formdata={'session_key':'L_USERNAME',
                              'session_password':'L_PASSWORD'},
                    callback=self.after_login)]
        
        #check to see if the user was able to login
        #if they can login, open the url list and start making requests to parse
    def after_login(self, response):
        print "***********Checking login*********"
        #myURL = "https://www.linkedin.com/vsearch/p?keywords=security&company=PSEG%20OR%20%22Con%20Edison%22&openAdvancedForm=true&companyScope=CP&locationType=Y"

        # check login succeed before going on
        if "the password you entered is incorrect" in response.body:
            self.log("\n\n\n\nLogin failed\n\n\n\n", level=self.log())
            return
        else:
            self.log("\n\n\n Login was successful!!!\n\n\n")
            #self.log(response.body)
            f = open("urls.txt")
            myList = [url.strip() for url in f.readlines()]
            f.close()
        
            for link in myList:
                #tempURL = self.make_requests_from_url(link)
                #yield Request(url=link,callback=self.parse_data(response))
                yield self.make_requests_from_url(link)
    
    #after the yield ^, this will automatically make a request to the parse function below
    #the parse function will select the xpath to create the object that will be sent to mongodb
    def parse(self,response):
        
        print "***MADE IT TO PARSE_DATA***"
        name = scrapy.Selector(response).xpath('//*[@id="name"]/h1/span/span')
        positions = scrapy.Selector(response).xpath('//header')
        schools = scrapy.Selector(response).xpath('//*[contains(@class,"education")]/header')
        descriptions = scrapy.Selector(response).xpath('//*[contains(@class,"editable-item") and contains(@class, "section-item")and contains(@class, "past-position")]/div')
        reccomendations = scrapy.Selector(response).xpath('//*[contains(@class,"endorsement-info")]')
        groups = scrapy.Selector(response).xpath('//*[@id="groups"]/ul/li')
        contactInfo = scrapy.Selector(response).xpath('//*[@id="contact-comments"]')
        #descriptions = scrapy.Selector(response).xpath('//div')
        item = LinkedinScrapyItem()
        
        for user in name:
            item['employeeName'] = user.xpath('text()').extract()
            #yield item
        
        #education
        for school in schools:
            item['school'] = school.xpath('h4/a/text()').extract()
            item['degree'] = school.xpath('h5/span/text()').extract()
            item['major'] = school.xpath('h5/span/a/text()').extract()
            yield item
            
        #job information
        for position in descriptions:
            #item['positionURL'] = position.xpath('a/@href').extract()
            item['positionTitle'] = position.xpath('header/h4/a/text()').extract()
            item['company'] = position.xpath('header/h5/span/strong/a/text()').extract()
            item['locality'] = position.xpath('span/span/text()').extract()

            #item['positionBackground'] = response.xpath('//p[@description summary-field-show-more"]').extract()
            #item['positionTitle'] = position.xpath('div/ul/li/text()').extract()
            yield item
            
        for reccomendation in reccomendations:
            #item['positionURL'] = position.xpath('a/@href').extract()
            item['jobReccomendorName'] = reccomendation.xpath('hgroup/h5/span/strong/a/strong/text()').extract()
            item['jobReccomendorURL'] = reccomendation.xpath('hgroup/h5/span/strong/a/@href').extract()
            item['jobReccomendorPosition'] = reccomendation.xpath('hgroup/h6/text()').extract()
            #item['jobReccomendationDetail'] = reccomendation.xpath('//*[contains(@class,"endorsement-quote")]/p/text()').extract()
            item['jobReccomendationDetail'] = reccomendation.xpath('blockquote/p/text()').extract()
            yield item
            
        for group in groups:
            item['groupName'] = group.xpath('p/a/text()').extract()
            item['groupName'] = group.xpath('p/a/@href()').extract()
            yield item
        #job descriptions
        for description in descriptions:
            #item['positionURL'] = position.xpath('a/@href').extract()
            item['positionDescription'] = description.xpath('p/text()').extract()
            yield item
        
        for contact in contactInfo:
            item['emailAddress'] = contact.xpath('div/p/text()').extract()
            yield item
        #yield item
        #pass

            
        
            
            
            
            
            
            
            
            
            
            
            