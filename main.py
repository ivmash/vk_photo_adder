import vk_api, requests, configparser
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

def get_resp(album_id : int):
    # list of files
    files = {'file1': open(image_path,'rb'),
        'file2': open(image_path,'rb'),
        'file3': open(image_path,'rb'),
        'file4': open(image_path,'rb'),
        'file5': open(image_path,'rb'),
        'file6': open(image_path,'rb'),
        'file7': open(image_path,'rb'),
        'file8': open(image_path,'rb'),
        'file9': open(image_path,'rb')
    }
    # getting server address
    upload_url = vk.photos.getUploadServer(album_id=album_id)['upload_url'] 
    # uploading images to the server
    return requests.post(upload_url, files=files).json()

def album_10000():
    # album creation
    album_id = vk.photos.createAlbum(title="New album")['id']
    # uploading a photo to the server, creating a resp object
    resp = get_resp(album_id)
    # adding to album
    count = 0
    while count < 10000:
        try:
            vk.photos.save(album_id=album_id, 
                server=resp['server'], 
                photos_list=resp['photos_list'], 
                aid=resp['aid'], 
                hash=resp['hash'])
            count += 1
        except:
            print("Flood control; count = ",count)
            # Flood control; waiting for an hour
            sleep(3600)
            # Get a new object
            resp = get_resp(album_id)

album_10000() 
