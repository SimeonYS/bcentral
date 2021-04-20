import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import BbcentralItem
from itemloaders.processors import TakeFirst
import json
import requests

pattern = r'(\xa0)?'

url = "https://www.bcentral.cl/web/banco-central/buscador?p_p_id=BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=%2Fbcentral%2Fsearch&p_p_cacheability=cacheLevelPage&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_modoBusqueda=MCS"

payload = "_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_tipoBusqueda=&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_categoriaId=35737%2C35742&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_fechaDesde=&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_fechaHasta=&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_anio=&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_periodo=&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_keyword=&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_busquedaExacta=false&p_auth=13E4Ntf7&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_cur={}&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_maxPages=14&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_total=263&as_sfid=AAAAAAXoyniCmvDEIFGXpNPc7dnAl_d-Ev6bI25KpODn-3NWhqTG2eoPdSxBSV9fd9MAQTQK7TaJthwyaMHMxakF9mLU40jcZMRXI5QYmaa6tguC7r6jldlG7jaZVRcZPU7rbcXlAiIstKeMNdQAcp1-iYaETPZwcq8rRyHwUXJeL01E9Q%3D%3D&as_fid=6d9225a7a41c8b88a8de06f545dc48d03edaac6d"
headers = {
  'Connection': 'keep-alive',
  'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
  'Accept': '*/*',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': 'https://www.bcentral.cl',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://www.bcentral.cl/web/banco-central/buscador?categoria=Prensa/Comunicados%20de%20RPM',
  'Accept-Language': 'en-US,en;q=0.9',
  'Cookie': 'COOKIE_SUPPORT=true; JSESSIONID=JU8v4n1lp6i9kTyHIMqkKI4fY1zM1Poses5yVy35.srvlifaplic704; _ga=GA1.2.1091277821.1618899162; _gid=GA1.2.1817673190.1618899162; _hjTLDTest=1; _hjid=3446ce58-c0ee-42f3-a1f2-206c1a951163; _hjFirstSeen=1; _hjAbsoluteSessionInProgress=1; GUEST_LANGUAGE_ID=es_ES; citrix_ns_id_.bcentral.cl_%2F_wat=AAAAAAWNeUG5LcACCNm03b2J7lnBqG8FHuK5iOfQaEbAdPHaoc_2ofg4FqqUiXcBcf3yLsNsx5g0cZR9oevK_BLb3ATV&; citrix_ns_id=AAE713p-YDudrA8AAAAAADugHLKUQnJuBCu9O5xiNkkOu7wl9xJwejs4QxZmn1GAOw==XX5-YA==pzMX8uK70-imCL0cCNJfqwRFnc8=; citrix_ns_id_.bcentral.cl_%2F_wlf=AAAAAAW07MsKzaph2RNJtdlgoGckhA4bpcWwuoQuLpZ7Nq9Ue8LJv1vS25E319waxl4v5dB4SGn55c9b5rsIstx8suGd-B1ib-YLIOIfzPIHWkxCEg==&; LFR_SESSION_STATE_33505=1618901721387; GUEST_LANGUAGE_ID=en_US; citrix_ns_id=AAI7-Hp-YDsouQ8AAAAAADugHLKUQnJuBCu9OyMXm0HFf3uw2b7mi8b-849JhP3pOw==fH5-YA==r3LjfIpzCpzFArUsLSbUqBsMD90=; citrix_ns_id_.bcentral.cl_%2F_wat=AAAAAAWIbhZssx-lDy88YW2v30ue3p0XavKm1WEKArkojfYMpgCvysxSVmRjDSsuotwVYR8v1WX-WRNwNt5fBhlHEoJu&; citrix_ns_id_.bcentral.cl_%2F_wlf=AAAAAAWCpUkk-RVkjYHLuKZZdVtJ64awxtp5HT-ETn5nSfTV67f54QuUZELD64bYyg2LH2uyIAJyCDJA1-dZrDJ7vnZkXlmEU7TREIhPeEyZyk1fUw==&'
}

class RpmSpider(scrapy.Spider):
    name = 'rpm'
    page = 1
    start_urls = ['https://www.bcentral.cl/web/banco-central/buscador?categoria=Prensa/Comunicados%20de%20RPM']
    ITEM_PIPELINES = {
        'rpm.pipelines.BbcentralPipeline': 300,
    }

    def parse(self, response):
        data = requests.request("POST", url, headers=headers, data=payload.format(self.page))
        data = json.loads(data.text)

        for index in range(len(data['body']['articulos'])):
            link = data['body']['articulos'][index]['ulrArticulo']
            date = data['body']['articulos'][index]['fechaArticulo']
            title = data['body']['articulos'][index]['tituloArticulo']
            yield response.follow(link, self.parse_post, cb_kwargs=dict(date=date, title=title))

        if self.page < data['body']['maxPages']:
            self.page += 1
            yield response.follow(response.url, self.parse, dont_filter=True)

    def parse_post(self, response, date, title):
        content = response.xpath('//div[@class="mb-6"]//text()').getall()
        content = [p.strip() for p in content if p.strip()]
        content = re.sub(pattern, "", ' '.join(content))
        if not content:
            content = "PDF file in the link"

        item = ItemLoader(item=BbcentralItem(), response=response)
        item.default_output_processor = TakeFirst()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        item.add_value('date', date)

        yield item.load_item()