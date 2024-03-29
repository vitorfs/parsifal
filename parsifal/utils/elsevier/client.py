import requests

from parsifal.utils.elsevier.exceptions import ElsevierException, ElsevierInvalidRequest, ElsevierQuotaExceeded


class ElsevierClient:
    def __init__(self, api_key, host="http://api.elsevier.com/content"):
        self.api_key = api_key
        self.host = host

    def _request(self, endpoint, params, requestType="GET"):
        if self.api_key:
            url = "{0}{1}".format(self.host, endpoint)
            params["apiKey"] = self.api_key
            if requestType == "POST":
                response = requests.post(url, params)
            else:
                response = requests.get(url, params)
            return self._parse_response(response)
        raise ElsevierException("No API Key.")

    def _parse_response(self, response):
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise ElsevierInvalidRequest
        elif response.status_code == 429:
            raise ElsevierQuotaExceeded

    def search_scopus(self, params):
        return self._request("/search/scopus", params)

    def search_science_direct(self, params):
        return self._request("/search/scidir", params)
