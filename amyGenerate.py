import requests
import json
import time

def remove_dashes(uuid):
    return uuid.replace("-", "")

def get_last_known_username(data):
    last_username = None
    for entry in data:
        if entry.get('username'):
            last_username = entry['username']
    return last_username

laby_url = "https://laby.net/api/user/{uuid}/get-names"
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; discord-blockplacer4/1.0; +blockplacer4)'
}

valid_uuid_file = 'valid_uuids.txt'
uuid_api_url = "https://www.uuidtools.com/api/generate/v4/count/100"

while True:
    response = requests.get(uuid_api_url)

    if response.status_code == 200:
        generated_uuids = response.json()
        
        for uuid in generated_uuids:
            uuid = remove_dashes(uuid)
            
            mojang_url = f"https://mojang.pro/uuid/production/{uuid}"
            mojang_response = requests.get(mojang_url)
            mojang_data = mojang_response.json()

            if mojang_data.get("id"):
                # UUID Mojang
                if response.status_code == 200:
                    # Labymod Request hier
                    response = requests.get(laby_url.format(uuid=uuid), headers=headers)
                    data = response.json()
                    last_username = get_last_known_username(data)
                    if last_username:
                        # Labymod ja
                        print(f"Invalid | {uuid} | {last_username}")
                    else:
                        # Labymod Nein
                        print(f"Valid | {uuid}")
                        with open(valid_uuid_file, 'a') as valid_fale:
                            valid_fale.write(uuid + '\n')
                else:
                    # UUID nicht Mojang
                    result = f"Wrong | {uuid}"
                    print(f"Wrong | {uuid}")
            else:
                # UUID nicht Mojang
                result = f"Wrong | {uuid}"
                print(f"Wrong | {uuid}")
    else:
        print("Fehler beim Abrufen der generierten UUIDs")
