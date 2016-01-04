import requests as rq
from urllib.parse import urlencode
from .board_api import BoardsApi

class PinterestAPI(object):
    host = 'api.pinterest.com'
    base_path = 'v1'
    protocol = 'https'

    def __init__(self, access_token: str = None):
        self._access_token = access_token
        self._http = rq.Session()

    @property
    def boards(self):
        return BoardsApi(self)

    def method(self, method, endpoint, params=None, form_data=None):
        if not all([method, endpoint]):
            return

        method = method.lower()
        url = '{protocol}://{netloc}/{path}'.format(
                protocol=self.protocol,
                netloc=self.host,
                path=self.base_path + '/' + endpoint
        )

        if params:
            params = params.copy()
        else:
            params = {}
        params.update({'access_token': self._access_token})
        for key in params:
            if isinstance(params[key], list):
                params[key] = ','.join(params[key])

        # requests bug, request('post',...) with url query dont work properly
        response = None
        if method == 'get':
            response = self._http.get(
                    url=url,
                    params=params
            )
        elif method == 'post':
            response = self._http.post(
                url=url + '/?' + urlencode(params),
                data=form_data
            )
        elif method == 'delete':
            response = self._http.delete(
                url=url + '/?' + urlencode(params)
            )
        else:
            raise Exception('Not Implemented Method')

        return response.json()


