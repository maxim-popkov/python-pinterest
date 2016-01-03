# Python Pinterest API
 Requirements:
 > requests

Examples
---
 ```python
from pinterest import PinterestAPI
access_token = 'your_token'
api = PinterestAPI(access_token)

# Board Info
ans = api.boards.board(owner='dales3d', name='cosplay').get()

# Board Pins
data = api.boards.board(owner='dales3d', name='cosplay').get_pins()

# Fetch all Board Pins with query params
params = {
    'fields':['image','note','counts'],
    'limit':'10'
}
board = api.boards.board(owner='dales3d', name='cosplay')
while True:
    data = board.get_pins(params)
    if not board.has_next_page:
        break
```