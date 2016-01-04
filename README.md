# Python Pinterest API

### Requirements:
 - requests 
 - Python 3.x
 
 
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
pins = []
while True:
    response = board.get_pins(params)
    pins.extend(response.get('data',[]))
    if not board.has_next_page:
        break
        
# Create Board
ans = api.boards.create('skiflab2', 'description some')

# Delete Board
ans = api.boards.board(owner='dales3d', name='skiflab2').delete()
```

## Install
```sh
git clone https://github.com/maxim-popkov/python-pinterest.git
cd python-pinterest
python setup.py install
```