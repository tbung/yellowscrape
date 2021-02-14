# -*- coding: utf-8 -*-
import scrapy
import string
import re


class YlpSpider(scrapy.Spider):
    name = "ylp"
    allowed_domains = ["gelbeseiten.de"]
    alphabets = string.ascii_lowercase
    start_urls = [
        "https://www.gelbeseiten.de/Suche/metall/Bundesweit/Seite-" + str(x)
        for x in range(1, 3)
    ]

    def parse(self, response):
        # companies = response.xpath('//*[@class="name m08_name"]')

        for company in response.css("article"):
            name = company.xpath(".//h2//text()").extract_first(default='')
            address = company.xpath(
                './/address//p[@data-wipe-name="Adresse"]//text()'
            ).extract_first(default='')
            postalcode = company.xpath(
                './/address//p[@data-wipe-name="Adresse"]//span//text()'
            ).extract_first(default='\n\t\t\t'*3)
            phone = company.xpath(
                './/address//p[@data-wipe-name="Kontaktdaten"]//text()'
            ).extract_first(default='')
            mail = company.xpath('.//div//div//a[@class="contains-icon-email gs-btn"]/@href').extract_first(default='')
            web = company.xpath('.//div//div//a[@class="contains-icon-homepage gs-btn"]/@href').extract_first(default='')
            branchen = company.xpath(
                './/a/p/text()'
            ).extract_first(default='')

            yield {
                "Name": name,
                "Address": address.replace("\n", "")
                .replace("\t", "")
                .replace(", ", ""),
                "PLZ": postalcode.split("\n\t\t\t")[1].replace('\t', ''),
                "Ort": postalcode.split("\n\t\t\t")[2].replace('\t', ''),
                "Tel": phone,
                "Mail": mail,
                "Web": web,
                "Branche": branchen
                .replace("\t", "")
                .replace(", ", ""),
            }
