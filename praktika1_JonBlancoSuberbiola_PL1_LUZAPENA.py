import json
import signal
import sys
import psutil
import time

import requests
import urllib

# Praktika 1 : Jon Blanco Suberbiola
def kanala_Sortu():
    metodoa = 'POST'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': 'L72TAKZ9LKNFOIYA',
              'name': 'Nire kanala',
              'field1': "%CPU",
              'field2': "%RAM"}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request(metodoa, uria, data=edukia_encoded,
                                 headers=goiburuak, allow_redirects=False)

    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)

    global apiak_hiztegi
    apiak_hiztegi = json.loads(edukia)
    global idazketa_api
    idazketa_api = apiak_hiztegi['api_keys'][0]['api_key']
    global irakurketa_api
    irakurketa_api = apiak_hiztegi['api_keys'][1]['api_key']
    global channel_id
    channel_id = apiak_hiztegi['id']

def konprobaketak_egin():
    zerr = getKanalak()
    dataZaharrena = zerr[0]['created_at']
    idZahar = ""
    if len(zerr) > 3:
        for kanal in zerr:
            oraingoa = str(kanal['created_at'])
            if (oraingoa <= dataZaharrena):
                idZahar = str(kanal['id'])

        ezabatu_kanala(idZahar)

def handler(sig_num, frame):
    # Gertaera kudeatu
    clear(irakurketa_api)
    print('\nSignal handler called with signal ' + str(sig_num))
    print('Check signal number on '
    'https://en.wikipedia.org/wiki/Signal_%28IPC%29#Default_action')
    print('\nExiting gracefully')
    sys.exit(0)

def cpu_ram():
    while True:
        # KODEA: psutil liburutegia erabiliz, %CPU eta %RAM atera
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))
        metodoa1 = 'POST'
        uria1 = "https://api.thingspeak.com/update.json"
        goiburuak1 = {'Host': 'api.thingspeak.com',
                      'Content-Type': 'application/x-www-form-urlencoded'}
        edukia1 = {'api_key': idazketa_api,
                   'name': 'Nire kanala',
                   'field1': cpu,
                  'field2': ram}

        edukia_encoded1 = urllib.parse.urlencode(edukia1)
        goiburuak1['Content-Length'] = str(len(edukia_encoded1))
        erantzuna = requests.request(metodoa1, uria1, data=edukia_encoded1,
                                     headers=goiburuak1, allow_redirects=False)

        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print(str(kodea) + " " + deskribapena)

        time.sleep(15)

def getKanalak():
    metodoa3 = 'GET'
    uria3 = "https://api.thingspeak.com/channels.json"
    goiburuak3 = {'Host': 'api.thingspeak.com',
                  'Content-Type': 'application/x-www-form-urlencoded'}
    edukia3 = {'api_key': 'L72TAKZ9LKNFOIYA'}
    edukia_encoded3 = urllib.parse.urlencode(edukia3)

    goiburuak3['Content-Length'] = str(len(edukia_encoded3))
    erantzuna3 = requests.request(metodoa3, uria3, data=edukia_encoded3,
                                 headers=goiburuak3, allow_redirects=False)

    kodea3 = erantzuna3.status_code
    deskribapena3 = erantzuna3.reason
    print(str(kodea3) + " " + deskribapena3)

    content = erantzuna3.content
    kanal_Zerrenda = json.loads(content)
    #print("\n"+str(kanal_Zerrenda)+"\n")
    return kanal_Zerrenda


def ezabatu_kanala(kanal):
    metodoa4 = 'DELETE'
    uria4 = "https://api.thingspeak.com/channels/" + str(kanal) + ".json"
    goiburuak4 = {'Host': 'api.thingspeak.com',
                  'Content-Type': 'application/x-www-form-urlencoded'}
    edukia4 = {'api_key': 'L72TAKZ9LKNFOIYA'}

    edukia_encoded4 = urllib.parse.urlencode(edukia4)
    goiburuak4['Content-Length'] = str(len(edukia_encoded4))
    erantzuna4 = requests.request(metodoa4, uria4, data=edukia_encoded4,
                                  headers=goiburuak4, allow_redirects=False)

    kodea = erantzuna4.status_code
    deskribapena = erantzuna4.reason
    print(str(kodea) + " " + deskribapena)


def clear(api_irak):
    print("Datuak ezabatzen...")
    metodoa2 = 'DELETE'
    uria2 = "https://api.thingspeak.com/channels/"+str(channel_id)+"/feeds.json"
    goiburuak2 = {'Host': 'api.thingspeak.com',
                  'Content-Type': 'application/x-www-form-urlencoded'}
    edukia2 = {'api_key': 'L72TAKZ9LKNFOIYA'}

    edukia_encoded2 = urllib.parse.urlencode(edukia2)
    goiburuak2['Content-Length'] = str(len(edukia_encoded2))
    erantzuna2 = requests.request(metodoa2, uria2, data=edukia_encoded2,
                                 headers=goiburuak2, allow_redirects=False)

    kodea = erantzuna2.status_code
    deskribapena = erantzuna2.reason
    print(str(kodea) + " " + deskribapena)




if __name__ == "__main__":
    # SIGINT jasotzen denean, "handler" metodoa exekutatuko da

    signal.signal(signal.SIGINT, handler)
    print('Running. Press CTRL-C to exit.')

    konprobaketak_egin()
    kanala_Sortu()
    cpu_ram()



