import requests
import pandas as pd
import concurrent.futures
import time


cards = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/datasets/cards/cards.json"
cards_df = pd.read_json(cards)

cards_list = cards_df["id"].drop_duplicates().tolist()

cards_render_path = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/images/cards/renders/"
cards_render_sizes = ["256x/","512x/"]
cards_tile_path = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/images/cards/tiles/"

api_img_render_url = "https://art.hearthstonejson.com/v1/render/latest/enUS/"
api_img_tile_url = "https://art.hearthstonejson.com/v1/tiles/"


print(f'Size of the card list: {len(cards_list)}')


def download_render_512(cards_list):
    print('Starting: Download Render 512x')
    for card_id in cards_list:
        target_url = api_img_render_url+cards_render_sizes[1]+card_id+'.png'
        r = requests.get(target_url, allow_redirects=True)
        if r.status_code == 200:
            open(cards_render_path+cards_render_sizes[1]+card_id+'.png', 'wb').write(r.content)
    print('Finished: Download Render 512x')


def download_render_256(cards_list):
    print('Starting: Download Render 256x')
    for card_id in cards_list:
        target_url = api_img_render_url+cards_render_sizes[0]+card_id+'.png'
        r = requests.get(target_url, allow_redirects=True)
        if r.status_code == 200:
            open(cards_render_path+cards_render_sizes[0]+card_id+'.png', 'wb').write(r.content)
    print('Finished: Download Render 256x')


def download_tile(cards_list):
    print('Starting: Download Tiles')
    for card_id in cards_list:
        target_url = api_img_tile_url+card_id+'.png'
        r = requests.get(api_img_tile_url+card_id+'.png', allow_redirects=True)
        if r.status_code == 200:
            open(cards_tile_path+card_id+'.png', 'wb').write(r.content)
    print('Finished: Download Tiles')

start_time = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(download_render_512,cards_list)
        executor.submit(download_render_256,cards_list)
        executor.submit(download_tile,cards_list)
print("--- It took %s seconds to complete all downloads ---" % (time.time() - start_time))