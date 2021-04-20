import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import BbcentralItem
from itemloaders.processors import TakeFirst
import json
import requests

url = "https://www.bcentral.cl/web/banco-central/buscador?p_p_id=BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=%2Fbcentral%2Fsearch&p_p_cacheability=cacheLevelPage&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_modoBusqueda=MCS"

payload = "_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_tipoBusqueda=&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_categoriaId=35737%2C35743&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_fechaDesde=&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_fechaHasta=&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_anio=&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_periodo=&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_keyword=&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_busquedaExacta=false&p_auth=13E4Ntf7&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_cur={}&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_maxPages=71&_BancoCentralResultadosBusqueda_INSTANCE_jo7U6rAqbmrq_total=1404&as_sfid=AAAAAAVK5gPYgmvlBakqcnG4Qwzwwc_B6nn9bC5Y3RTmhXonTtH2FvwF0ZVX3gA-vfqqRbbhhLn3EWo8DJkL8jYF6P9cgOUmMjNtnM2JPHHZYpHDujEsjKcU4CSjhJ4BOs0WFqOwFw2e1F-ig5KtuKx_FpGZev7aobLbv0yzuyttKD02pg%3D%3D&as_fid=d8d7570fb862858823a70c5e83afc41863b74c9a"
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
  'Referer': 'https://www.bcentral.cl/web/banco-central/buscador?categoria=Prensa%2FNota%20de%20Prensa',
  'Accept-Language': 'en-US,en;q=0.9',
  'Cookie': 'COOKIE_SUPPORT=true; JSESSIONID=JU8v4n1lp6i9kTyHIMqkKI4fY1zM1Poses5yVy35.srvlifaplic704; _ga=GA1.2.1091277821.1618899162; _gid=GA1.2.1817673190.1618899162; _hjTLDTest=1; _hjid=3446ce58-c0ee-42f3-a1f2-206c1a951163; _hjFirstSeen=1; _hjAbsoluteSessionInProgress=1; _gat=1; _hjIncludedInPageviewSample=1; GUEST_LANGUAGE_ID=es_ES; citrix_ns_id=AAE7lnZ-YDuwlw8AAAAAADugHLKUQnJuBCu9O3n5ndLV-ZCbjeRCOG7mPNA3EMYyOw==eHp-YA==zh_d0IsfVxCbpo4s0KJXndmtwME=; citrix_ns_id_.bcentral.cl_%2F_wlf=AAAAAAXjNUgWgAbD1zYTRu_hTc_tuiBfEg_puxpvG9iFoCJZuRQbWUqsCrWXeV2rG1aK7LJy3KQy-HeIkMQdIIxiz_uzKsPBxmiwBtE_GFPINXYivg==&; citrix_ns_id_.bcentral.cl_%2F_wat=AAAAAAWGfi7b27bccB6O6eAhSi850tT_IgWF_5zGCB3NkJA5L6HN98xWStHlEEHXd8WhObu0YY-7QuCr_A5X6eqZUhET&; LFR_SESSION_STATE_33505=1618900724737; GUEST_LANGUAGE_ID=en_US; citrix_ns_id=AAE7lnZ-YDuwlw8AAAAAADugHLKUQnJuBCu9O3n5ndLV-ZCbjeRCOG7mPNA3EMYyOw==onp-YA==yWjh0zksAa2Yvt3Ik8Rk13s633s=; citrix_ns_id_.bcentral.cl_%2F_wat=AAAAAAXJiGnIP6GcDR-T1mZJxUB9kV8BSMHWai-5k_46Z5Zc44-0xUhWJihNeESGxjZkZWKdBqUnPzMVf2wU-dW9HX_t&; citrix_ns_id_.bcentral.cl_%2F_wlf=AAAAAAWkR-0AHHCqttOaJyy8igbm2RqdwfXl62UKs2vIoXGctWCOjLyzEJ70umjP6retzaTkpUzYaYK55jXb4CSIHCQ8DP2nIzLSbu4k5V7G7D-Kcw==&'
}

pattern = r'(\xa0)?'

class BbcentralSpider(scrapy.Spider):
	name = 'bcentral'
	page = 1
	start_urls = ['https://www.bcentral.cl/en/buscador?categoria=Prensa%2FNota%20de%20Prensa']

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
		content = re.sub(pattern, "",' '.join(content))
		if not content:
			content = "PDF file in the link"

		item = ItemLoader(item=BbcentralItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
