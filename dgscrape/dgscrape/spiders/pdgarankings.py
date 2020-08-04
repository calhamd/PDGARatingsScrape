import scrapy
import pandas as pd
from functools import partial


class PdgaRatingsSpider(scrapy.Spider):
    name = 'pdgaratings'
    allowed_domains = ['pdga.com']
    start_urls = ['http://pdga.com/']

    def start_requests(self):
        players_url = 'https://www.pdga.com/players?FirstName=&LastName=&PDGANum=&Status=All&Gender=M&Class=P&MemberType=All&City=&StateProv=All&Country=All&Country_1=All&UpdateDate='
        
        yield scrapy.Request(url=players_url, callback=self.parse_players)        

    def parse_players(self, response):
        rows = response.xpath('//*[@class="table-container"]//table//tr')
        if rows:            
            headers = rows[0].xpath('th//text()').extract()
            for row in rows[1:]:
                player_id = int(row.xpath('td[2]//text()').extract()[0].strip())
                player_name = row.xpath('td[1]//text()').extract()[1]
                #print(f'Pulling: {player_id}, {player_name}')
                url = f'https://www.pdga.com/player/{player_id}/history'
                yield response.follow(url, callback=partial(self.parse_history, player_id=player_id, player_name=player_name))
            next_page = response.css('li.pager-next a::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_players)
            pass

    def parse_history(self, response, player_id=0, player_name=''):
        print(f'    Pulling History: {player_id}, {player_name}')
        rows = response.xpath('//*[@id="player-results-history"]//tr')  
        if rows:
            items = []
            headers = rows[0].xpath('th//text()').extract()
            for row in rows[1:]:
                item = { headers[idx]: res for idx, res in enumerate(row.xpath('td//text()').extract())}
                item['player_id'] = player_id
                item['player_name'] = player_name
                items.append(item)
                yield item
        pass        
