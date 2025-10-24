from pathlib import Path
from marquise_bot.items import LinkGraphItem
from queue import Queue
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor


class MarquiseSpider(CrawlSpider):
    name = "marquise_bot"
    allowed_domains = ["marquiseambiental.com.br"]
    start_urls = [
        "https://www.marquiseambiental.com.br"
    ]
    
    # 1. Pegar todos os links interno, sob o mesmo dominio "marquiseambiental.com"
    rules = (
        Rule(LinkExtractor(allow=r'marquiseambiental\.com\.br'), 
             callback='parse_item', 
             follow=True),
    )
    
    def parse_item(self, response):
        print("DEBUG: Processando a página: " + response.url)
        links_encontrados = response.css(" a::attr(href)").getall()
        
        conjunto_links = set()
        
        if not links_encontrados:
            print("DEBUG: Nenhum link encontrado!")
            print("DEBUG: conteudo da resposta:\n" + response.text[:500])
        
        # 2. Colocando os link interno dentro de um conjunto
        for link in links_encontrados:
            link_absoluto = response.urljoin(link)
            
            if self.allowed_domains[0] in link_absoluto:
                    conjunto_links.add(link)
        
        item = LinkGraphItem()
        item['pagina_origem'] = response.url
        item['links_destino'] = list(conjunto_links)
        
        yield item