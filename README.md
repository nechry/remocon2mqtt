# ELCO Remocon-net 2 MQTT

This Python script gets the data from the gas boiler system via the Elco Remocon-Net cloud service.

The data will be published via MQTT.

Can be used with Home Assistant to receive boiler data's.

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

## Home Assistant integration

No auto-discovery in home-assistant for the moment. You have to create manually your MQTT entities.

In your `configuration.yaml` add a packages merge dir named `packages`

```yaml
homeassistant:
  packages: !include_dir_named packages 
```

Create in your config folder a sub-folder named  `packages`

add the [remocon.yaml](home-assistant/remocon.yaml) file inside.

At the end you will have this structure:

```bash

packages/remocon.yaml
configuration.yaml

```

For more details about package usage check the [Packages folder documentation](https://www.home-assistant.io/docs/configuration/packages/#create-a-packages-folder) in Home Assistant.

## node-RED way's

You can also use [node-RED](node-RED/flow.json) to query and push to MQTT

![flow node-RED][img2]

The flow use the node [credentials](https://flows.nodered.org/node/node-red-contrib-credentials).

Install it before import

## License

[MIT](LICENSE)

[img1]: images/home-assistant-card.png
[img2]: images/node-RED-flow.jpg
