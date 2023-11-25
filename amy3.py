import aiohttp
import asyncio

async def username_to_uuid(session, username):
    async with session.get(f'https://mojang.pro/name/production/{username}') as response:
        if response.status == 200:
            print(f'Successfully retrieved UUID for {username}')
            return (await response.json())['id']
        else:
            print(f'Failed to retrieve UUID for {username}')
            return None

async def convert_usernames_to_uuids(usernames):
    async with aiohttp.ClientSession() as session:
        tasks = [username_to_uuid(session, username) for username in usernames]
        uuids = await asyncio.gather(*tasks)
    return uuids

with open('usernames.txt', 'r') as f:
    usernames = [line.strip() for line in f]

with open('suffixes.txt', 'r') as f:
    suffixes = [line.strip() for line in f]

combined_usernames = [username + suffix for username in usernames for suffix in suffixes]

print('Starting conversion of usernames to UUIDs...')
loop = asyncio.get_event_loop()
uuids = loop.run_until_complete(convert_usernames_to_uuids(combined_usernames))
print('Conversion completed.')

with open('uuids.txt', 'w') as f:
    print('Writing UUIDs to uuids.txt...')
    for uuid in uuids:
        f.write(f'{uuid}\n')
    print('UUIDs written to uuids.txt.')

with open('response.txt', 'w') as f:
    print('Writing UUIDs and corresponding usernames to response.txt...')
    for username, uuid in zip(combined_usernames, uuids):
        f.write(f'{username}: {uuid}\n')
    print('UUIDs and corresponding usernames written to response.txt.')