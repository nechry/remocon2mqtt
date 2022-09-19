# ELCO Remocon-net 2 MQTT

This Python script gets the data from the gas boiler system via the Elco Remocon-Net cloud service.

The data will be published via MQTT.

Can be used with [home-assistant](home-assistant/remocon.yaml) to receive boiler data's.

![Thision S Dashboard][img1]

## Setup

Install Python3 requirements

```bash
pip3 install -r requirements.txt
```

Rename or copy [default.example](default.example) to `default.cfg` and adapt it to your configuration

```bash
python3 ./remocon2mqtt.py
```

## Limitation

It not a service but just a script, you have to schedule it via a crontab for instance.

I'ts a readonly integration, we can't modify set-point or any parameters on the boiler.

## node-RED way's

You can also use [node-RED](node-RED/flow.json) to query and push to MQTT

![flow node-RED][img2]





[img1]: images/thision_s.jpg
[img2]: images/remocon2mqtt-node-RED.jpg

