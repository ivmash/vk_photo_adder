import vk_api
import requests
import configparser

from time import sleep


# Login, password and an image
config = configparser.ConfigParser()
config.read('settings.ini')
image_path = config['Vk_Photo_Adder']['image_path']
phone_number = config['Vk_Photo_Adder']['phone_number']
password = config['Vk_Photo_Adder']['password']

vk_session = vk_api.VkApi(phone_number, password)
vk_session.auth()
vk = vk_session.get_api()

def get_resp(album_id : int, files_count : int):

    # list of files
    files = {}
    for n in range(1, files_count+1):
         files['file'+str(n)] = open(image_path,'rb')

    # getting server address
    upload_url = vk.photos.getUploadServer(album_id=album_id)['upload_url'] 
    # uploading images to the server

    return requests.post(upload_url, files=files).json()

def album(images_count : int):

    # album creation
    album_id = vk.photos.createAlbum(title="New album")['id']
 
    # uploading a photo to the server, creating a resp object
    resp = get_resp(album_id, 9)

    # adding to album
    count = 0
    while count < (images_count // 9):
        try:
            # Print count of images after every hundered
            if ((count*9+9) // 100) > (count*9 // 100):
                print(f"Image {count*9+9}")
            vk.photos.save(album_id=album_id, 
                server=resp['server'], 
                photos_list=resp['photos_list'], 
                aid=resp['aid'], 
                hash=resp['hash'])
            count += 1
        except:
            print("Flood control; Images count = ", count*9)
            # Flood control; waiting for an hour
            sleep(3600)
            # Get a new object
            resp = get_resp(album_id, 9)
    
    if count*9 != images_count:
        resp = get_resp(album_id, images_count % 9)
        vk.photos.save(album_id=album_id, 
                    server=resp['server'], 
                    photos_list=resp['photos_list'], 
                    aid=resp['aid'], 
                    hash=resp['hash'])


if __name__ == "__main__":
    album(10000) 
