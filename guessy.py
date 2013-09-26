import re
import os
import sys
import json
import requests
import random
from bs4 import SoupStrainer, BeautifulSoup

LOGO = '''
          _____                    _____                    _____                    _____                    _____                _____          
         /\    \                  /\    \                  /\    \                  /\    \                  /\    \              |\    \         
        /::\    \                /::\____\                /::\    \                /::\    \                /::\    \             |:\____\        
       /::::\    \              /:::/    /               /::::\    \              /::::\    \              /::::\    \            |::|   |        
      /::::::\    \            /:::/    /               /::::::\    \            /::::::\    \            /::::::\    \           |::|   |        
     /:::/\:::\    \          /:::/    /               /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          |::|   |        
    /:::/  \:::\    \        /:::/    /               /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \         |::|   |        
   /:::/    \:::\    \      /:::/    /               /::::\   \:::\    \       \:::\   \:::\    \       \:::\   \:::\    \        |::|   |        
  /:::/    / \:::\    \    /:::/    /      _____    /::::::\   \:::\    \    ___\:::\   \:::\    \    ___\:::\   \:::\    \       |::|___|______  
 /:::/    /   \:::\ ___\  /:::/____/      /\    \  /:::/\:::\   \:::\    \  /\   \:::\   \:::\    \  /\   \:::\   \:::\    \      /::::::::\    \ 
/:::/____/  ___\:::|    ||:::|    /      /::\____\/:::/__\:::\   \:::\____\/::\   \:::\   \:::\____\/::\   \:::\   \:::\____\    /::::::::::\____\ 
\:::\    \ /\  /:::|____||:::|____\     /:::/    /\:::\   \:::\   \::/    /\:::\   \:::\   \::/    /\:::\   \:::\   \::/    /   /:::/~~~~/~~      
 \:::\    /::\ \::/    /  \:::\    \   /:::/    /  \:::\   \:::\   \/____/  \:::\   \:::\   \/____/  \:::\   \:::\   \/____/   /:::/    /         
  \:::\   \:::\ \/____/    \:::\    \ /:::/    /    \:::\   \:::\    \       \:::\   \:::\    \       \:::\   \:::\    \      /:::/    /          
   \:::\   \:::\____\       \:::\    /:::/    /      \:::\   \:::\____\       \:::\   \:::\____\       \:::\   \:::\____\    /:::/    /           
    \:::\  /:::/    /        \:::\__/:::/    /        \:::\   \::/    /        \:::\  /:::/    /        \:::\  /:::/    /    \::/    /            
     \:::\/:::/    /          \::::::::/    /          \:::\   \/____/          \:::\/:::/    /          \:::\/:::/    /      \/____/             
      \::::::/    /            \::::::/    /            \:::\    \               \::::::/    /            \::::::/    /                           
       \::::/    /              \::::/    /              \:::\____\               \::::/    /              \::::/    /                            
        \::/____/                \::/____/                \::/    /                \::/    /                \::/    /                             
                                                           \/____/                  \/____/                  \/____/                              
'''

try:
  ETSY_API_KEY = os.environ['ETSY_API_KEY']
except:
  print 'Please set the environment variables ETSY_API_KEY and ETSY_API_SECRET'
  sys.exit(1)

ETSY_API_URL_BASE = 'https://openapi.etsy.com/v2/{action}/?api_key=' + ETSY_API_KEY
IMAGE_TO_ASCII_URL = 'http://picascii.com/upload.php'

def http(url):
  return re.sub(r'^https://|^', r'http://', url) if not url.startswith('http://') else url

def image_to_ascii(image_url):
  response = requests.post(IMAGE_TO_ASCII_URL, data={
    'url' : http(image_url)
  }).text

  return BeautifulSoup(response, parse_only=SoupStrainer('pre')).find('pre').get_text()

def etsy_api_call(action, params={}):
  return requests.get(ETSY_API_URL_BASE.format(action=action), params=params).json()['results']

def get_listing():
  return random.choice(etsy_api_call('listings/active', {
    'page' : random.randint(0, 1000)
  }))

def get_listing_image_url(listing):
  try:
    return etsy_api_call(
        'listings/{listing_id}/images'.format(listing_id=listing['listing_id'])
    )[0]['url_170x135']
  except:
    print 'Oops, no image'

def get_listing_title(listing):
  return listing['title']

def capture_input():
    while True:
      choice = raw_input('> ').strip()
      if len(choice) > 0:
        return choice

def display_menu():
  while True:
    print 'Making magic happen (please be patient)'

    chosen_listing, dummy_listing_1, dummy_listing_2 = [get_listing() for _ in range(3)]
    print image_to_ascii(get_listing_image_url(chosen_listing))
    print 'Can you guess the item?'

    titles = map(get_listing_title, [chosen_listing, dummy_listing_1, dummy_listing_2])
    random.shuffle(titles)
    correct_answer = titles.index(chosen_listing['title'])
    print '\n'.join(['%d. %s' % (i+1, title) for i, title in enumerate(titles)])

    choice = capture_input()
    if choice in ('q', 'quit'):
      return
    elif int(choice)-1 == correct_answer:
      print 'YOU GOT IT!'
    else:
      print 'WRONG! YOU SUCK! The correct answer was %d' % (correct_answer+1)

if __name__ == '__main__':
  print LOGO
  display_menu()
