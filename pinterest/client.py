import requests as rq
from urllib.parse import urlencode


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
        if method.lower() == 'get':
            response = self._http.get(
                    url=url,
                    params=params
            )
        elif method.lower() == 'post':
            response = self._http.post(
                url=url + '/?' + urlencode(params),
                data=form_data
            )
        elif method.lower() == 'delete':
            response = self._http.delete(
                url=url + '/?' + urlencode(params)
            )
        else:
            raise Exception('Not Implemented Method')

        if response.ok:
            response = response.json()
        else:
            response = {}

        return response


class BoardsApi(object):
    """
    Class wrap work with board api
    """
    endpoint = 'boards'

    def __init__(self, api: PinterestAPI):
        self.api = api
        self._board_id = None
        self._board_owner = None
        self._board_name = None
        self._board_slug = None
        self._cursor = None

    @property
    def has_next_page(self) -> bool:
        """
        :return: True if response has next page
        """
        return self._cursor is not None

    def get_pins(self, params=None) -> dict:
        """
        Return Pins from Board
        :param params: api params like fields, counters..
        :return: response dict or None
        """
        if params:
            params = params.copy()
        else:
            params = {}

        if self._cursor:
            params.update({'cursor': self._cursor})

        if not self._board_slug:
            return None
        endpoint_full = self.endpoint + '/' + self._board_slug + '/pins'

        response = self.api.method('get', endpoint_full, params)
        if response.get('page'):
            self._cursor = response['page'].get('cursor')
        else:
            self._cursor = None

        return response

    def get(self, params=None):
        if not self._board_slug:
            return None
        endpoint_full = self.endpoint + '/' + self._board_slug
        response = self.api.method('GET', endpoint_full, params)
        return response

    def create(self, name, desc=None):
        form_data = {
            'name': name,
            'description': desc
        }
        endpoint_full = self.endpoint
        response = self.api.method('POST', endpoint_full, form_data=form_data)
        return response

    def board(self,
              owner=None,
              name=None,
              board_id=None,):
        """
        Select board
        example: api.boards.board(owner='dales3d', name='cosplay').get()
        :param board_id:
        :param owner: board
        :param name:
        :return:
        """
        self._board_id = board_id
        self._board_owner = owner
        self._board_name = name

        if board_id:
            self._board_slug = board_id
        elif name and owner:
            self._board_slug = owner + '/' + name

        return self

    def delete(self):
        if not self._board_slug:
            return None
        endpoint_full = self.endpoint + '/' + self._board_slug
        response = self.api.method('DELETE', endpoint_full)
        return response

    def update(self):
        raise NotImplementedError
