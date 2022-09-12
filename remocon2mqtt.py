import sys
import requests
import json
import paho.mqtt.client as mqtt
from urllib.parse import quote
import configparser

def on_connect(client, userdata, flags, rc):
    print(f'Connected {str(rc)}')

def on_publish(client, userdata, result):
    print("Data published with success")

def on_disconnect(client, userdata, rc):
    print(f'Disconnect, reason {str(rc)}')

def connectMQTT(config):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    client.username_pw_set(username=config.get('MQTT','username'), password=config.get('MQTT','password'))

    try:
        client.connect(config.get('MQTT','host'), config.getint('MQTT','port'), 60)
    except Exception as error: 
        print(f'ERROR: Can not connect to MQTT broker {error}')
        sys.exit(1)
    return client


def sendHVACtoMQTT(config, data):
    client = connectMQTT(config)
    client.publish(config.get('MQTT','topic'), json.dumps(data))  # publish
    client.disconnect()

def main(config):
    base_url = config.get('REMOCON-NET', 'url')    
    url = base_url + "R2/Account/Login?returnUrl=HTTP/2"
    username = quote(config.get('REMOCON-NET','username'), safe='')
    password = quote(config.get('REMOCON-NET','password'), safe='')
    payload = f'Email={username}&Password={password}&RememberMe=false'
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'browserUtcOffset=-120'}
    session = requests.session()
    # login,get session cookie and address for json data
    response = session.post(url=url, headers=headers, data=payload)
    result_json = json.loads(response.text)    
    if(result_json['ok']):
        gateway = config.get('REMOCON-NET','gateway')        
        url = f"{base_url}R2/PlantHomeBsb/GetData/{gateway}"
        # get zone 1 data 
        payload = {
            "useCache": True, 
            "zone": 1, 
            "filter": 
                {
                    "progIds": "null", 
                    "plant": True, 
                    "zone": True
                }
            }
        response = session.post(url=url, json=payload)
        if(response.status_code==200):    
            result_json = json.loads(response.text)
            sendHVACtoMQTT(config=config, data=result_json['data'])
            return
        else:
            print(response.text)
    else:
        print(result_json['message'])
    sys.exit(1)

if __name__ == '__main__':        
    config = configparser.ConfigParser()
    config.read('default.cfg')    
    main(config)
    print("Completed")