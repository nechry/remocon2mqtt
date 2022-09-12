import requests
import json
import paho.mqtt.client as mqtt
from urllib.parse import quote
import configparser


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    pass

def on_publish(client, userdata, result):
    print("Data published")
    pass

def on_disconnect(client, userdata, rc):
    print("disconnecting reason  " + str(rc))
    pass

def connectMQTT(config):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.username_pw_set(username=config.get('MQTT','username'), password=config.get('MQTT','password'))
    try:
        client.connect(config.get('MQTT','host'), config.getint('MQTT','port'), 60)
    except Exception as e: 
        print(e)
        print("ERROR: Can not connect to MQTT broker")
        return -1
    return client


def sendHVACtoMQTT(config, data):
    client = connectMQTT(config)
    if client == -1:
        return -1

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
    result_json = json.loads(response.text)        
    sendHVACtoMQTT(config=config, data=result_json['data'])


if __name__ == '__main__':        
    config = configparser.ConfigParser()
    config.read('default.cfg')    
    main(config)
    print("finishing")