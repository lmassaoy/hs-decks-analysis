# images_downloader.py

## Who am I 
I am a python job capable to download all render and tile images from [https://hearthstonejson.com/](https://hearthstonejson.com/).

## How do I do my job
I run three threads to have a better performance to download everything I need, by using the python lib concurrent.futures. If you're interested, please read my script :)

## How run me
First: make sure you already have the directories where the images will be downloaded
- /hs-decks-analysis/data/images/cards/renders/256x/
- /hs-decks-analysis/data/images/cards/renders/512x/
- /hs-decks-analysis/data/images/cards/tiles/

Now you just need to run me:
```
$ python3 python/utils/images_downloader.py

Size of the card list: 2674
Starting: Download Render 512x
Starting: Download Render 256
Starting: Download Tiles
--- It took 3907.6407327651978 seconds to complete all downloads ---
```
Yeah, it may take a while to download everything (around 2 GBs)