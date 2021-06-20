import scrapy

class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['trustpilot.com']
    start_urls = ['https://www.trustpilot.com/categories/utilities']

    def parse(self, response):
        urls_1 = response.css('div.styles_businessUnitCardsContainer__1ggaO > a::attr(href)').extract()
        if urls_1 != []:
            for url_1 in urls_1:
                url_1 = response.urljoin(url_1)
                yield scrapy.Request(url=url_1, callback=self.parse_details)

        next_page_url = response.css('a[name="pagination-button-next"]::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        for review in response.css('div.review-content'):
            yield {
                'Company': response.xpath('//h1/span[1]/text()').extract_first().strip(),
                'Category': response.css('p.company-breadcrumbs-mobile > a::text').extract_first().strip(),
                'total_reviews': response.css('span.headline__review-count::text').extract_first(),
                'general_rating': response.css('p.header_trustscore::text').extract_first(),
                'review_rating': review.xpath('div//@alt').re(r'(\d+)'),
                'review_text': " ".join(review.xpath('string(div/p[descendant-or-self::text()])').extract_first().split())
            }
        #next_page = response.css('body > main > div > div.company-profile-body > section > div.review-list > nav > a::attr(href)').get()
        next_page = response.css('a.button.button--primary.next-page').attrib['href'] 
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_details)


