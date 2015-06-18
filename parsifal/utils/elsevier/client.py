import requests

from exceptions import ElsevierException


class ElsevierClient(object):
    def __init__(self,
                 api_key,
                 host='http://api.elsevier.com/content'):
        self.api_key = api_key
        self.host = host

    def _request(self, endpoint, params, requestType='GET'):
        response= None
        if self.api_key is not None:
            url = u'{0}{1}'.format(self.host, endpoint)
            params['apiKey'] = self.api_key
            if requestType == 'POST':
                response = requests.post(url, params)
            else:
                response = requests.get(url, params)
        else:
            raise ElsevierException('No API Key.')
        return self._parse_response(response)

    def _parse_response(self, response):
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            raise ElsevierException('Quota Exceeded.')


    def search_scopus(self, query):
        return self._request('/search/scopus', { 'query': query })

    def search_science_direct(self, query):
        return self._request('/search/scidir', { 'query': query })
