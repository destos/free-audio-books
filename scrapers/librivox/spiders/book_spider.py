import json
import scrapy

from librivox.items import BookItem, BookCategoryItem, BookChapterItem
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from sizefield.utils import parse_size


class BookSpider(scrapy.Spider):

    name = 'book'
    allowed_domains = ['librivox.org']
    start_urls = [
        'https://librivox.org/search/get_results?primary_key=21&search_category=genre&sub_category=&search_page=1&search_order=alpha&project_type=either'
    ]

    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        if data.get('status', False) == 'SUCCESS':
            results = Selector(text=data.get('results', ''))
            for sel in results.xpath('//li'):
                book = BookItem()
                book['name'] = sel.xpath('div[1]/h3/a/text()').extract()
                book['author'] = sel.xpath('div[1]/p[1]/a/text()').extract()
                book['author_url'] = sel.xpath('div[1]/p[1]/a/@href').extract()
                # book['years'] = sel.xpath('').extract()
                book['book_url'] = sel.xpath('div[1]/h3/a/@href').extract()
                book['book_cover'] = sel.xpath('a/img/@src').extract()
                book['zip_url'] = sel.xpath('div[2]/a/@href').extract()
                for k, v in book.iteritems():
                    try:
                        book[k] = v[0]
                    except Exception, e:
                        pass
                yield book
        else:
            raise Exception('unable to hit book test url')


class CatrgoryBookItemSpider(scrapy.Spider):
    name = 'book_category'
    allowed_domains = ['librivox.org']

    test_run = True

    category_list_url_format = 'https://librivox.org/search/get_results?primary_key={lv_pk}&search_category=genre&sub_category=&search_page={page}&search_order=alpha&project_type=either'

    def start_requests(self):
        # Get all categories
        categories = BookCategoryItem.django_model.objects.filter(will_scrape=True)
        if self.test_run == True:
            # only first category for now
            categories = categories[:1]
        for category in categories:
            yield scrapy.Request(
                self.category_list_url_format.format(lv_pk=category.lv_pk, page=1),
                dont_filter=True,
                meta={'category_lv_pk': category.lv_pk})

    def parse(self, response):
        return self.parse_book_list(response)

    def parse_book_list(self, response):
        category_lv_pk = response.meta['category_lv_pk']
        data = json.loads(response.body_as_unicode())
        if data.get('status', False) == 'SUCCESS':
            results = Selector(text=data.get('results', ''))
            for sel in results.xpath('//li'):
                book = BookItem()
                # make a request for this book's detail page.
                book['name'] = sel.xpath('div[1]/h3/a/text()').extract()[0]
                book['author'] = sel.xpath('div[1]/p[1]/a/text()').extract()[0]
                book['author_url'] = sel.xpath('div[1]/p[1]/a/@href').extract()[0]
                # book['years'] = sel.xpath('').extract()[0]
                book['book_url'] = sel.xpath('div[1]/h3/a/@href').extract()[0]
                # book['zip_url'] = sel.xpath('div[2]/a/@href').extract()[0]

                yield scrapy.Request(
                    book['book_url'],
                    callback=self.parse_book_detail,
                    meta={'book': book})

            # start another request if another page is available
            pagination = data.get('pagination', False)
            if pagination:
                pagination = Selector(text=pagination)
                next_page = pagination.xpath('//a[contains(@class, "active")]/following-sibling::a[1]')
                # Check for next page, if next page is last and don't progress
                if bool(next_page) and not bool(next_page.css('[class*="last"]')):
                    page = next_page.xpath('@data-page_number').extract()[0]
                    yield scrapy.Request(
                        self.category_list_url_format.format(lv_pk=category_lv_pk, page=page),
                        meta={'category_lv_pk': category_lv_pk},
                        callback=self.parse_book_list)


    def parse_book_detail(self, response):
        book = response.meta['book']
        book['total_time'] = response.xpath('//dl[@class="product-details clearfix"]/dd[1]/text()').extract()[0]
        zip_size_str = response.xpath('//dl[@class="product-details clearfix"]/dd[2]/text()').extract()[0]
        book['zip_size'] = parse_size(zip_size_str)
        book['zip_url'] = response.xpath('//dl[@class="listen-download clearfix"]/dd[1]/a/@href').extract()[0]
        book['book_cover'] = response.xpath('//div[@class="book-page-book-cover"]/img/@src').extract()[0]
        try:
            book['description'] = response.xpath('//div[@class="description"]/text()').extract()[0]
        except IndexError:
            pass

        django_book = book.save()
        headers = [header.lower() for header in response.xpath('//table[@class="chapter-download"]/thead/tr/th/text()').extract()]

        def get_h_index(header):
            try:
                headers.index(header)
            except ValueError, e:
                return None

        for chapter in response.xpath('//table[@class="chapter-download"]/tbody/tr'):
            # get table headers
            book_chapter = BookChapterItem()

            # helper func
            def set_property(prop, xpath='td[{col_id}]', col='chapter', default=None):
                col_id = get_h_index(col)
                if col_id:
                    try:
                        value = chapter.xpath(xpath.format(col_id=col_id)).extract[0]
                    except IndexError:
                        value = default
                book_chapter[prop] = value

            import ipdb; ipdb.set_trace()
            # book_chapter['name'] = chapter.xpath('td[{}]/text()'.format(get_h_index('chapter')))[0]
            set_property('name', xpath='td[{col_id}]/text()', col='chapter')
            # book_chapter['reader'] = chapter.xpath('/td[3]/text()')[0]
            import ipdb; ipdb.set_trace()
            book_chapter['number'] = int(chapter.xpath('td[{}]/text()'.format(get_h_index('section')))[0].split('')[1])
            book_chapter['book'] = django_book
            set_property('mp3_url', xpath='td[{col_id}]/a/@url', col='chapter')
            set_property('time', xpath='td[{col_id}]/text()', col='time')
            book_chapter['mp3_size'] = 0
            book_chapter['language'] = 'en'
            book_chapter.save()
        return book


# https://librivox.org/search?primary_key=37&search_category=genre&search_page=1&search_form=get_results

class CategoryItemSpider(scrapy.Spider):

    name = 'category'
    allowed_domains = ['librivox.org']
    start_urls = [
        'https://librivox.org/search/'
    ]

    def parse(self, response):
        for option in response.xpath('//*[@id="genre_id"]/option'):
            category = BookCategoryItem()
            category['lv_pk'] = int(option.xpath('@value').extract()[0])
            try:
                all_names = option.xpath('text()').extract()[0]
            except IndexError:
                continue
            category_tree = [name.strip() for name in all_names.split('>')]
            # Try and find parent object.
            parent = None
            try:
                parent_name = category_tree[-2]
                if parent_name:
                    parent_potentials = BookCategoryItem.django_model.objects.filter(
                        name=parent_name)
                    # filter to only categories with no parents
                    if parent_potentials.count() > 1:
                        parent_potentials = parent_potentials.filter(parent=None)
                    if parent_potentials.count() == 1:
                        parent = parent_potentials[0]
                    # else: add if still >
                    #     raise Exception('more than one parent found?!?!')
            except IndexError, e:
                pass
            # find existing category and update instead of create
            try:
                category = BookCategoryItem.django_model.objects.get(
                    lv_pk=category['lv_pk'])
                category.name = category_tree[-1]
                category.parent = parent
            except BookCategoryItem.django_model.DoesNotExist:
                category['name'] = category_tree[-1]
                category['parent'] = parent
            # import ipdb; ipdb.set_trace()
            category.save()
            yield category
