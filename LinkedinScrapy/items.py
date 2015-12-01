# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkedinScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	
	#
    positionURL = scrapy.Field()
    positionTitle = scrapy.Field()
    positionBackground = scrapy.Field()
    positionDescription = scrapy.Field()
    company = scrapy.Field()
    locality = scrapy.Field()

    jobReccomendorName = scrapy.Field()
    jobReccomendorURL = scrapy.Field()
    jobReccomendorPosition = scrapy.Field()
    jobReccomendationDetail = scrapy.Field()
    
    groupName = scrapy.Field()
    groupURL = scrapy.Field()
    
    school = scrapy.Field()
    degree = scrapy.Field()
    major = scrapy.Field()

    employeeName = scrapy.Field()
    emailAddress = scrapy.Field()
    pass
