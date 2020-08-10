# images_downloader.py

## Who am I 
I am a python job capable to download all render and tile images from [https://hearthstonejson.com/](https://hearthstonejson.com/).

[![OG-317.png](https://i.postimg.cc/K8k1P35f/OG-317.png)](https://postimg.cc/87GkD59f) [![WE1-036.png](https://i.postimg.cc/xqr1gt5P/WE1-036.png)](https://postimg.cc/7JV4Z1pC) [![AT-072.png](https://i.postimg.cc/RhtHM3bX/AT-072.png)](https://postimg.cc/jns5cjT7)

## How do I do my job
I run three threads to have a better performance to download everything I need, by using the python lib concurrent.futures. If you're interested, please read my script :)

## How to run me
First: make sure you already have the directories where the images will be downloaded
- /hs-decks-analysis/data/images/cards/renders/256x/
- /hs-decks-analysis/data/images/cards/renders/512x/
- /hs-decks-analysis/data/images/cards/tiles/

Now you just need to run me:
```
$ python3 python/utils/images_downloader.py

Size of the card list: 2674
Starting: Download Render 512x
Starting: Download Render 256x
Starting: Download Tiles
--- It took 3907.6407327651978 seconds to complete all downloads ---
```
Yeah, it may take a while to download everything (around 2 GBs)