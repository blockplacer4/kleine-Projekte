import requests
import time

laby_url = "https://laby.net/api/user/{uuid}/get-names"
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; discord-blockplacer4/1.0; +blockplacer4)'
}

uuid_file = 'uuid_list.txt'
valid_uuid_file = 'valid_uuids.txt'

def get_last_known_username(data):
    last_username = None
    for entry in data:
        if entry.get('username'):
            last_username = entry['username']
    return last_username

def check_uuids(uuid_list):
    for uuid in uuid_list:
        uuid = uuid.strip()
        response = requests.get(laby_url.format(uuid=uuid), headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            last_username = get_last_known_username(data)
            if last_username:
                print(f"Invalid | {uuid} | {last_username}")
                time.sleep(1.75)
            else:
                print(f"Valid | {uuid}")
                with open(valid_uuid_file, 'a') as valid_fale:
                    valid_fale.write(uuid + '\n')
                    time.sleep(1.75)
        else:
            print(f"Failed UUID: {uuid}")

with open(uuid_file, 'r') as file:
    uuid_list = file.readlines()

check_uuids(uuid_list)

