import json
import requests
from requests import HTTPError, RequestException


class ProxyHelper:

    proxy_domain = 'http://107.150.102.81:8010'

    @staticmethod
    def get_single_proxy():
        url = ProxyHelper.proxy_domain + '/get'
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            proxy_data = json.loads(resp.text)
            return proxy_data['proxy']
        except (RequestException, TypeError) as e:
            return ''

    @staticmethod
    def delete_proxy(proxy):
        url = ProxyHelper.proxy_domain + '/delete?proxy=%s' % proxy
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            return True
        except HTTPError as e:
            return False
