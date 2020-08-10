import requests
import os


class ImageRenderDownloader():
    def __init__(self,image_size):
        self.image_size = image_size
        if image_size == 256:
            self.image_directory_path = "data/images/cards/renders/256x/"
            self.image_url_path = "https://art.hearthstonejson.com/v1/render/latest/enUS/256x/"
        else:
            self.image_directory_path = "data/images/cards/renders/512x/"
            self.image_url_path = "https://art.hearthstonejson.com/v1/render/latest/enUS/512x/"
        

    def download(self,image_id):
        target_url = self.image_url_path+image_id+".png"
        target_directory = self.image_directory_path+image_id+".png"

        if os.path.isfile(target_directory):
            return target_directory
        else:
            r = requests.get(target_url, allow_redirects=True)
            if r.status_code == 200:
                open(target_directory, 'wb').write(r.content)
                return target_directory
            else:
                return None
