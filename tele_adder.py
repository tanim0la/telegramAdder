from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import (PeerFloodError, UserNotMutualContactError ,
                                          UserPrivacyRestrictedError, UserChannelsTooMuchError,
                                          UserBotError, InputUserDeactivatedError)
from telethon.tl.functions.channels import InviteToChannelRequest
import time, os, sys, json

wt = (
    '''
                                                  
  [[ye]]*   )                              (        
[[re]]` )  /(    )        (      )         )\    )  
 [[ye]]( )(_))( /(   (    )\    (      (  ((_)( /(  
[[re]](_(_()) )(_))  )\ )((_)   )\  '  )\  _  )(_)) 
[[gr]]|_   _|((_)_  _(_/( (_) _((_))  ((_)| |((_)_  
  [[gr]]| |  / _` || ' \))| || '  \()/ _ \| |/ _` | 
  |_|  \__,_||_||_| |_||_|_|_| \___/|_|\__,_| 

            version : 1.0

github.com/Ayscoopy [[re]][DOnt forget to leave a star]
    '''
)
COLORS = {
    "re": "\u001b[31;1m",
    "gr": "\u001b[32m",
    "ye": "\u001b[33;1m",
}
re = "\u001b[31;1m"
gr = "\u001b[32m"
ye = "\u001b[33;1m"
def colorText(text):
    for color in COLORS:
        text = text.replace("[[" + color + "]]", COLORS[color])
    return text
clearType = input('terminal or cmd. (t/c): ').lower()
if clearType == 't':
    clear = lambda:os.system('clear')
elif clearType == 'c':
    clear = lambda:os.system('cls')
else:
    print('Invalid input!!!')
    sys.exit()
    
if sys.version_info[0] < 3:
    telet = lambda :os.system('pip install -U telethon')
elif sys.version_info[0] >= 3:
    telet = lambda :os.system('pip3 install -U telethon')

telet()
time.sleep(1)
clear()

if os.path.isfile('getmem_log.txt'):
    with open('getmem_log.txt', 'r') as r:
        data = r.readlines()
    api_id = data[0]
    api_hash = data[1]

else:
    api_id = input('Enter api_id: ')
    api_hash = input('Enter api_hash: ')
    with open('getmem_log.txt', 'w') as a:
        a.write(api_id + '\n' + api_hash)

client = TelegramClient('anon', api_id, api_hash)

async def main():
    # To Add Members.......
    async def getmem():
        clear()
        print(colorText(wt))
        print('')
        print('')
        
        print(ye+'[+] Choose your channel to Add members.')
        a=0
        for i in channel:
            print(gr+'['+str(a)+']', i.title)
            a += 1
        opt1 = int(input(ye+'Enter a number: '))
        my_participants = await client.get_participants(channel[opt1])
        target_group_entity = InputPeerChannel(channel[opt1].id, channel[opt1].access_hash)
        my_participants_id = []
        for my_participant in my_participants:
            my_participants_id.append(my_participant.id)
        with open('members.txt', 'r') as r:
            users = json.load(r)
        count = 1
        i = 0
        for user in users:
            if count%50 == 0:
                clear()
                print(colorText(wt))
                print('')
                print('')
                print(ye+"please wait for 1 minute...")
                time.sleep(60)
            elif count >= 300:
                await client.disconnect()
                break
            elif i >= 8:
                await client.disconnect()
                break
            count+=1
            time.sleep(1)
            if user['uid'] in my_participants_id:
                print(gr+'User present. Skipping.')
                continue
            else:
                try:
                    user_to_add = InputPeerUser(user['uid'], user['access_hash'])
                    add = await client(InviteToChannelRequest(target_group_entity,[user_to_add]))
                    print(gr+'Added ', str(user['uid']))
                    
                except PeerFloodError:
                    print(re+"Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
                    i += 1
                except UserPrivacyRestrictedError:
                    print(re+"The user's privacy settings do not allow you to do this. Skipping.")
                    i = 0
                except UserBotError:
                    print(re+"Can't add Bot. Skipping.")
                    i = 0
                except InputUserDeactivatedError:
                    print(re+"The specified user was deleted. Skipping.")
                    i = 0
                except UserChannelsTooMuchError:
                    print(re+"User in too much channel. Skipping.")
                except UserNotMutualContactError:
                    print(re+'Mutual No. Skipped.')
                    i = 0
                except Exception as e:
                    print(re+"Error:", e)
                    print("Trying to continue...")
                    i += 1
                    continue
                #end
    
    print(colorText(wt))
    chats = []
    channel = []
    result = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))
    chats.extend(result.chats)
    for a in chats:
        try:
            if True:
                channel.append(a)
        except:
            continue

    a = 0
    print('')
    print('')
    print(ye+'Choose a group to scrape.')
    for i in channel:
        print(gr+'['+str(a)+']', i.title)
        a += 1
    op = input(ye+'Enter a number (or press ENTER to skip): ')
    if op == '':
        print(ye+'Ok. skipping...')
        time.sleep(1)
        await getmem()
        sys.exit()
    else: 
        pass
    opt = int(op)
    print('')
    print(ye+'[+] Fetching Members...')
    time.sleep(1)
    target_group = channel[opt]
    all_participants = []
    mem_details = []
    all_participants = await client.get_participants(target_group)
    for user in all_participants:
        try:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                firstname = user.first_name
            else:
                firstname = ""
            if user.last_name:
                lastname = user.last_name
            else:
                lastname = ""

            new_mem = {
                'uid': user.id,
                'username': username,
                'firstname': firstname,
                'lastname': lastname,
                'access_hash': user.access_hash
            }
            mem_details.append(new_mem)
        except ValueError:
            continue
    
    with open('members.txt', 'w') as w:
        json.dump(mem_details, w)
    time.sleep(1)
    print(ye+'Please wait.....')
    time.sleep(3)
    done = input(gr+'[+] Members scraped successfully. (Press enter to Add members)')
    await getmem()

    await client.disconnect()

with client:
    client.loop.run_until_complete(main())
