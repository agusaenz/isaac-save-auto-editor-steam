import requests
import re
## HOLA MUNDO!
# file location
# C:\Program Files (x86)\Steam\userdata\{user}\250900\remote

filename = r"rep+persistentgamedata2.dat"
_debug = True

# ------------- DATA -------------

def rshift(val, n): 
    return val>>n if val >= 0 else (val+0x100000000)>>n

def getSectionOffsets(data):
    ofs = 0x14
    sectData = [-1, -1, -1]
    entryLens = [1,4,4,1,1,1,1,4,4,1]
    sectionOffsets = [0] * 10
    for i in range(len(entryLens)):
        for j in range(3):
            sectData[j] = int.from_bytes(data[ofs:ofs+2], 'little', signed=False)
            ofs += 4
        if sectionOffsets[i] == 0:
            sectionOffsets[i] = ofs
        for j in range(sectData[2]):
            ofs += entryLens[i]
    return sectionOffsets

def getChecklistUnlocks(data, char_index):
    checklist_data = []
    if char_index == 14:
        clu_ofs = getSectionOffsets(data)[1] + 0x32C
        for i in range(12):
            current_ofs = clu_ofs + i * 4
            checklist_data.append(getInt(data, current_ofs))
            if i == 8:
                clu_ofs += 0x4
            if i == 9:
                clu_ofs += 0x37C
            if i == 10:
                clu_ofs += 0x84
    elif char_index > 14:
        clu_ofs = getSectionOffsets(data)[1] + 0x31C
        for i in range(12):
            current_ofs = clu_ofs + char_index * 4 + i * 19 * 4
            checklist_data.append(getInt(data, current_ofs))
            if i == 8:
                clu_ofs += 0x4C
            if i == 9:
                clu_ofs += 0x3C
            if i == 10:
                clu_ofs += 0x3C
    else:
        clu_ofs = getSectionOffsets(data)[1] + 0x6C
        for i in range(12):
            current_ofs = clu_ofs + char_index * 4 + i * 14 * 4
            checklist_data.append(getInt(data, current_ofs))
            if i == 5:
                clu_ofs += 0x14
            if i == 8:
                clu_ofs += 0x3C
            if i == 9:
                clu_ofs += 0x3B0
            if i == 10:
                clu_ofs += 0x50
    return checklist_data

def getChallenges(data):
    challenge_data = []
    offs = getSectionOffsets(data)[6]
    for i in range(1, 46):
        challenge_data.append(getInt(data, offs+i, num_bytes=1))
    return challenge_data

def calcAfterbirthChecksum(data, ofs, length):
    CrcTable = [
        0x00000000, 0x09073096, 0x120E612C, 0x1B0951BA, 0xFF6DC419, 0xF66AF48F, 0xED63A535, 0xE46495A3, 
        0xFEDB8832, 0xF7DCB8A4, 0xECD5E91E, 0xE5D2D988, 0x01B64C2B, 0x08B17CBD, 0x13B82D07, 0x1ABF1D91, 
        0xFDB71064, 0xF4B020F2, 0xEFB97148, 0xE6BE41DE, 0x02DAD47D, 0x0BDDE4EB, 0x10D4B551, 0x19D385C7, 
        0x036C9856, 0x0A6BA8C0, 0x1162F97A, 0x1865C9EC, 0xFC015C4F, 0xF5066CD9, 0xEE0F3D63, 0xE7080DF5, 
        0xFB6E20C8, 0xF269105E, 0xE96041E4, 0xE0677172, 0x0403E4D1, 0x0D04D447, 0x160D85FD, 0x1F0AB56B, 
        0x05B5A8FA, 0x0CB2986C, 0x17BBC9D6, 0x1EBCF940, 0xFAD86CE3, 0xF3DF5C75, 0xE8D60DCF, 0xE1D13D59, 
        0x06D930AC, 0x0FDE003A, 0x14D75180, 0x1DD06116, 0xF9B4F4B5, 0xF0B3C423, 0xEBBA9599, 0xE2BDA50F, 
        0xF802B89E, 0xF1058808, 0xEA0CD9B2, 0xE30BE924, 0x076F7C87, 0x0E684C11, 0x15611DAB, 0x1C662D3D, 
        0xF6DC4190, 0xFFDB7106, 0xE4D220BC, 0xEDD5102A, 0x09B18589, 0x00B6B51F, 0x1BBFE4A5, 0x12B8D433, 
        0x0807C9A2, 0x0100F934, 0x1A09A88E, 0x130E9818, 0xF76A0DBB, 0xFE6D3D2D, 0xE5646C97, 0xEC635C01,
        0x0B6B51F4, 0x026C6162, 0x196530D8, 0x1062004E, 0xF40695ED, 0xFD01A57B, 0xE608F4C1, 0xEF0FC457, 
        0xF5B0D9C6, 0xFCB7E950, 0xE7BEB8EA, 0xEEB9887C, 0x0ADD1DDF, 0x03DA2D49, 0x18D37CF3, 0x11D44C65, 
        0x0DB26158, 0x04B551CE, 0x1FBC0074, 0x16BB30E2, 0xF2DFA541, 0xFBD895D7, 0xE0D1C46D, 0xE9D6F4FB, 
        0xF369E96A, 0xFA6ED9FC, 0xE1678846, 0xE860B8D0, 0x0C042D73, 0x05031DE5, 0x1E0A4C5F, 0x170D7CC9, 
        0xF005713C, 0xF90241AA, 0xE20B1010, 0xEB0C2086, 0x0F68B525, 0x066F85B3, 0x1D66D409, 0x1461E49F, 
        0x0EDEF90E, 0x07D9C998, 0x1CD09822, 0x15D7A8B4, 0xF1B33D17, 0xF8B40D81, 0xE3BD5C3B, 0xEABA6CAD, 
        0xEDB88320, 0xE4BFB3B6, 0xFFB6E20C, 0xF6B1D29A, 0x12D54739, 0x1BD277AF, 0x00DB2615, 0x09DC1683, 
        0x13630B12, 0x1A643B84, 0x016D6A3E, 0x086A5AA8, 0xEC0ECF0B, 0xE509FF9D, 0xFE00AE27, 0xF7079EB1, 
        0x100F9344, 0x1908A3D2, 0x0201F268, 0x0B06C2FE, 0xEF62575D, 0xE66567CB, 0xFD6C3671, 0xF46B06E7, 
        0xEED41B76, 0xE7D32BE0, 0xFCDA7A5A, 0xF5DD4ACC, 0x11B9DF6F, 0x18BEEFF9, 0x03B7BE43, 0x0AB08ED5, 
        0x16D6A3E8, 0x1FD1937E, 0x04D8C2C4, 0x0DDFF252, 0xE9BB67F1, 0xE0BC5767, 0xFBB506DD, 0xF2B2364B, 
        0xE80D2BDA, 0xE10A1B4C, 0xFA034AF6, 0xF3047A60, 0x1760EFC3, 0x1E67DF55, 0x056E8EEF, 0x0C69BE79, 
        0xEB61B38C, 0xE266831A, 0xF96FD2A0, 0xF068E236, 0x140C7795, 0x1D0B4703, 0x060216B9, 0x0F05262F, 
        0x15BA3BBE, 0x1CBD0B28, 0x07B45A92, 0x0EB36A04, 0xEAD7FFA7, 0xE3D0CF31, 0xF8D99E8B, 0xF1DEAE1D, 
        0x1B64C2B0, 0x1263F226, 0x096AA39C, 0x006D930A, 0xE40906A9, 0xED0E363F, 0xF6076785, 0xFF005713, 
        0xE5BF4A82, 0xECB87A14, 0xF7B12BAE, 0xFEB61B38, 0x1AD28E9B, 0x13D5BE0D, 0x08DCEFB7, 0x01DBDF21, 
        0xE6D3D2D4, 0xEFD4E242, 0xF4DDB3F8, 0xFDDA836E, 0x19BE16CD, 0x10B9265B, 0x0BB077E1, 0x02B74777, 
        0x18085AE6, 0x110F6A70, 0x0A063BCA, 0x03010B5C, 0xE7659EFF, 0xEE62AE69, 0xF56BFFD3, 0xFC6CCF45, 
        0xE00AE278, 0xE90DD2EE, 0xF2048354, 0xFB03B3C2, 0x1F672661, 0x166016F7, 0x0D69474D, 0x046E77DB, 
        0x1ED16A4A, 0x17D65ADC, 0x0CDF0B66, 0x05D83BF0, 0xE1BCAE53, 0xE8BB9EC5, 0xF3B2CF7F, 0xFAB5FFE9, 
        0x1DBDF21C, 0x14BAC28A, 0x0FB39330, 0x06B4A3A6, 0xE2D03605, 0xEBD70693, 0xF0DE5729, 0xF9D967BF, 
        0xE3667A2E, 0xEA614AB8, 0xF1681B02, 0xF86F2B94, 0x1C0BBE37, 0x150C8EA1, 0x0E05DF1B, 0x0702EF8D
    ]
    checksum = 0xFEDCBA76
    checksum = ~checksum

    for i in range(ofs, ofs+length):
        checksum = CrcTable[((checksum & 0xFF)) ^ data[i]] ^ (rshift(checksum, 8))

    return ~checksum + 2 ** 32

def getInt(data, offset, debug=False, num_bytes=2):
    if debug: print(f"current value: {int.from_bytes(data[offset:offset+num_bytes], 'little', signed=False)}")
    return int.from_bytes(data[offset:offset+num_bytes], 'little')

def alterInt(data, offset, new_val, debug=False, num_bytes=2):
    if debug:
        print(f"current value: {int.from_bytes(data[offset:offset+num_bytes], 'little')}")
        print(f"new value: {new_val}")
    return data[:offset] + new_val.to_bytes(num_bytes, 'little', signed=True) + data[offset + num_bytes:]

def alterChallenge(data, challenge_index, unlock=True):
    if unlock:
        val = 1
    else:
        val = 0
    return alterInt(data, getSectionOffsets(data)[6]+challenge_index, val, num_bytes=1)

def updateChallenges(data, challenge_list):
    for i in range(1, 46):
        data = alterChallenge(data, i, False)
    for i in challenge_list:
        data = alterChallenge(data, int(i), True)
    return data

def updateChecksum(data):
    offset = 0x10
    length = len(data) - offset - 4
    return data[:offset + length] + calcAfterbirthChecksum(data, offset, length).to_bytes(5, 'little', signed=True)[:4]

# ------------- MISC FUNCTIONS -------------

def writeToFile(data, filename):
    with open(filename, 'wb') as file:
        # print(calcAfterbirthChecksum(data, offset, length).to_bytes(5, 'little', signed=True)[:4])
        file.write(updateChecksum(data))
        print(f"File written to {filename} successfully.")

def get_achievements(steam_id, api_key):
    user_achievements = []
    # URL to the Steam Web API
    # url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/"
    url = f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"

    # Parameters for the API call
    params = {
        'steamid': steam_id,
        'appid': '250900',
        'key': api_key
    }

    # Make the GET request to the API
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if 'playerstats' in data:
            player_stats = data['playerstats']
            if 'achievements' in player_stats:
                achievements = player_stats['achievements']
                print(f"Found {len(achievements)} achievements for this game.")

                # Create an array for unlocked achievement apinames
                # user_achievements = [ach['apiname'] for ach in achievements if ach['achieved'] == 1]
                user_achievements = [ach['name'] for ach in achievements]

                if user_achievements:
                    return user_achievements
                else:
                    print("No achievements unlocked.")
                    return user_achievements
            else:
                print("No achievements found for this game.")
                return user_achievements
        else:
            print("Error: Player stats not found.")
            return user_achievements
    else:
        if response.status_code == 403:
            data = response.json()
            if 'playerstats' in data:
                if 'success' in data['playerstats'] and data['playerstats']['success'] == False:
                    print("Error: Steam Profile is private.")
                    return user_achievements
                    
        
        return user_achievements

def isSteamID64(input_value):
    """
    Check if the input is a valid SteamID64.
    A valid SteamID64 is a 17-digit numeric string.
    """
    steam_id64_pattern = re.compile(r'^\d{17}$')
    return bool(steam_id64_pattern.match(input_value))

def getSteamID64(steam_id, api_key):
    url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"

    params = {
        'key': api_key,
        'vanityurl': steam_id
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if 'response' in data:
            response_data = data['response']

            if 'success' in response_data:
                success = response_data['success']

                if success == 1:
                    return response_data['steamid']
                else:
                    print("Error: Steam ID not found.")
                    return None
            else:
                print("Error: 'success' key not found in response data.")
                return None
        else:
            print("Error: 'response' key not found in data.")
            return None

# ------------- POST-IT FUNCTIONS -------------

""" checklist_order = [
    "Mom's Heart", 
    "Isaac", 
    "Satan", 
    "Boss Rush", 
    "???", 
    "The Lamb", 
    "Mega Satan", 
    "Ultra Greed", 
    "Ultra Greedier", 
    "Hush", 
    "Delirium", 
    "Mother", 
    "The Beast"
] """

CharactersAchievements = {
    'Isaac':['167','106','43','70','49','149','205','192','296','179','282','440','441'],
    'Magdalene': ['168','20','45','109','50','71','206','193','297','180','283','442','443'],
    'Cain':['171','21','46','110','75','51','207','194','298','181','284','444','445'],
    'Judas':['170','107','72','108','77','52','208','195','299','182','285','446','447'],
    "???": ['174','29','48','114','113','73','209','196','300','183','286','448','449'],
    "Eve": ['169','76','44','112','53','111','210','197','302','184','288','450','451'],
    "Samson": ['177','54','56','115','55','74','211','198','301','185','287','452','453'],
    "Azazel": ['173','126','127','9','128','47','212','199','304','186','290','454','455'],
    "Lazarus": ['172','116','117','105','118','119','213','200','305','187','291','456','457'],
    "Eden": ['176','121','122','125','123','124','214','201','303','188','289','458','459'],
    "The Lost": ['175','129','130','133','131','132','215','202','307','189','293','460','461'],
    "Lilith": ['223','218','220','222','219','221','216','203','306','190','292','462','463'],
    "Keeper": ['241','236','237','240','238','239','217','204','308','191','294','464','465'],
    "Apollyon": ['318','310','311','314','312','313','317','316','309','315','295','466','467'],
    "Forgotten": ['392','393','394','397','395','396','403','399','400','398','401','468','469'],
    "Bethany": ['416','417','418','421','419','420','427','422','424','423','425','470','471'],
    "Jacob & Esau": ['428','429','430','433','431','432','439','434','436','435','437','472','473'],

    "T Isaac":  ['548','548','548','618','548','548','601','541','541','618','584','549','491'],
    "T Magdalene":  ['550','550','550','619','550','550','602','530','530','619','585','551','492'],
    "T Cain":  ['552','552','552','620','552','552','603','534','534','620','586','553','493'],
    "T Judas":  ['554','554','554','621','554','554','604','525','525','621','587','555','494'],
    "T ???":  ['556','556','556','622','556','556','605','528','528','622','588','557','495'],
    "T Eve":  ['558','558','558','623','558','558','606','527','527','623','589','559','496'],
    "T Samson":  ['560','560','560','624','560','560','607','535','535','624','590','561','497'],
    "T Azazel":  ['562','562','562','625','562','562','608','539','539','625','591','563','498'],
    "T Lazarus":  ['564','564','564','626','564','564','609','543','543','626','592','565','499'],
    "T Eden":  ['566','566','566','627','566','566','610','544','544','627','593','567','500'],
    "T Lost":  ['568','568','568','628','568','568','611','524','524','628','594','569','501'],
    "T Lilith":  ['570','570','570','629','570','570','612','526','526','629','595','571','502'],
    "T Keeper":  ['572','572','572','630','572','572','613','536','536','630','596','573','503'],
    "T Apollyon":  ['574','574','574','631','574','574','614','540','540','631','597','575','504'],
    "T Forgotten":  ['576','576','576','632','576','576','615','537','537','632','598','577','505'],
    "T Bethany":  ['578','578','578','633','578','578','616','529','529','633','599','579','506'],
    "T Jacob":  ['580','580','580','634','580','580','617','542','542','634','600','581','507']
}

UserPostIt = {
    'Isaac': [],
    'Magdalene': [],
    'Cain':[],
    'Judas':[],
    "???":[],
    "Eve":[],
    "Samson":[],
    "Azazel":[],
    "Lazarus":[],
    "Eden":[],
    "The Lost":[],
    "Lilith":[],
    "Keeper":[],
    "Apollyon":[],
    "Forgotten":[],
    "Bethany":[],
    "Jacob & Esau":[],
    "T Isaac":[],
    "T Magdalene":[],
    "T Cain":[],
    "T Judas":[],
    "T ???":[],
    "T Eve":[],
    "T Samson":[],
    "T Azazel":[],
    "T Lazarus":[],
    "T Eden":[],
    "T Lost":[],
    "T Lilith":[],
    "T Keeper":[],
    "T Apollyon":[],
    "T Forgotten":[],
    "T Bethany":[],
    "T Jacob":[]
}

def updateChecklistArray(data,char_name):
    if list(UserPostIt).index(char_name) == 14:
        clu_ofs = getSectionOffsets(data)[1] + 0x32C
        for i in range(12):
            current_ofs = clu_ofs + i * 4
            data = alterInt(data, current_ofs, UserPostIt[char_name][i])
            if i == 8:
                clu_ofs += 0x4
            if i == 9:
                clu_ofs += 0x37C
            if i == 10:
                clu_ofs += 0x84
    elif list(UserPostIt).index(char_name) > 14:
        clu_ofs = getSectionOffsets(data)[1] + 0x31C
        for i in range(12):
            current_ofs = clu_ofs + list(UserPostIt).index(char_name) * 4 + i * 19 * 4
            data = alterInt(data, current_ofs, UserPostIt[char_name][i])
            if i == 8:
                clu_ofs += 0x4C
            if i == 9:
                clu_ofs += 0x3C
            if i == 10:
                clu_ofs += 0x3C
    else:
        clu_ofs = getSectionOffsets(data)[1] + 0x6C
        for i in range(12):
            current_ofs = clu_ofs + list(UserPostIt).index(char_name) * 4 + i * 14 * 4
            data = alterInt(data, current_ofs, UserPostIt[char_name][i])
            if i == 5:
                clu_ofs += 0x14
            if i == 8:
                clu_ofs += 0x3C
            if i == 9:
                clu_ofs += 0x3B0
            if i == 10:
                clu_ofs += 0x50
    return data

def ChecklistAllCharacter(user_achievements):
    for i in CharactersAchievements.keys():
        for j in CharactersAchievements.get(i):
            if j in user_achievements:
                UserPostIt[i].append(2)
            else:
                UserPostIt[i].append(0)
        if UserPostIt[i][8]==2:
            del UserPostIt[i][7]
        elif UserPostIt[i][7]==2:
            UserPostIt[i][8]=1
            del UserPostIt[i][7]
        else:
            UserPostIt[i][8]=0
            del UserPostIt[i][7]
    return

def updatePostIt(data, user_achievements):
    ChecklistAllCharacter(user_achievements)

    if _debug:
        for char, post_it_array in UserPostIt.items():
            if char:
                print(f"Updating {char}'s post-it note")
                print(post_it_array) 
                data = updateChecklistArray(data, char)
            else:
                return
    else:
        for char in UserPostIt.keys():
            if char:
                print(f"Updating {char}'s post-it note")
                data = updateChecklistArray(data, char)
            else:
                return
    return data
        
# ------------- CHALLENGES FUNCTIONS -------------

all_challenges_achievements = ['89','90','91','92','93','94','120','96','97','98','99','100','60','63','101','102','103','104','62','95','224','225','226','227','228','229','230','231','232','233','331','332','333','334','335','517','518','519','520','521','522','531','532','533','538']

def updateChallengesArray(data, user_achievements):
    user_achievements_set = set(user_achievements)
    completed_challenges = [index + 1 for index, achievement in enumerate(all_challenges_achievements) if achievement in user_achievements_set]

    # [index + 1] is used to get the challenge number from the index

    if _debug:
        print("Updating challenges")
        print(completed_challenges)

    return updateChallenges(data, completed_challenges)

# ------------- MAIN -------------
        
if __name__ == "__main__":
    
    offset = 0x10
    with open(filename, "rb") as file:
        data = file.read()
        length = len(data) - offset - 4
        checksum = calcAfterbirthChecksum(data, offset, length).to_bytes(5, 'little', signed=True)[:4]
        # print(checksum)
        old_checksum = data[offset + length:]    

    steam_id = "76561198070040216"  # Your Steam ID64
    steam_id = "cacatuas26"  # or custom id
    # these are found in the url of your steam profile. examples:
    # https://steamcommunity.com/profiles/76561198070040216/
    # https://steamcommunity.com/id/cacatuas26/

    api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Your Steam Web API key
    
    if not isSteamID64(steam_id):
        steam_id_64 = getSteamID64(steam_id, api_key)

        if steam_id_64:
            user_achievements = get_achievements(steam_id_64, api_key)
        else:
            print("Error: Invalid Steam ID.")
    else:
        user_achievements = get_achievements(steam_id, api_key)
    
    

    if user_achievements:
        # post-it
        data = updatePostIt(data, user_achievements)
        # challenges
        data = updateChallengesArray(data, user_achievements)
        writeToFile(data,filename)
    else:
        print("Error handler.")
