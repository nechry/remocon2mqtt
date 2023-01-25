# ELCO Remocon-net 2 MQTT

Two way's to get data from your Elco Remocon-Net boiler system, published on MQTT broker and display on a Home Assistant dashboard.

![Thision S Dashboard][img1]

## Description

I initially wrote a python script to get data from my boiler system and forward then to a MQTT broker.
Than I found a easy way to install, debug and share with Home-Assistant community via a node-RED flow.

## Setup

I recommend to use the Node-RED way.

### node-RED way's

![flow node-RED][node-RED-flow]

First you have to install [Node-RED Community Add-on](https://nodered.org/docs/getting-started/local) for Home Assistant.

You can also install [node-RED](https://nodered.org/) on a standalone server, if you prefer.

#### Node-RED requirements

The flow use the node [credentials](https://flows.nodered.org/node/node-red-contrib-credentials).

Install node-red-contrib-credentials before import the flow.

![node-RED-manage-palette][node-RED-manage-palette]

On Install tab, search for `node-red-contrib-credentials` module and install it.

![node-red-contrib-credentials][node-red-contrib-credentials]

#### Node-RED flow

Then import the [flow.json](node-RED/flow.json) file.

![import][node-RED-import]

#### Node-RED configuration

You have to configure the Elco Remocon-Net credentials.

You also need to know your gatewayId.

The easy way to get the gatewayId is to login to the [Elco Remocon-Net webapp](https://www.remocon-net.remotethermo.com/).

After login, you will see the gatewayId in the URL. For example `FFEEBBAA0011`:
https://www.remocon-net.remotethermo.com/R2/Plant/Index/FFEEBBAA0011?navMenuItem=0&breadcrumbPath=0

With the gatewayId, you can now configure the `Remocon Auth` node.

![configure][node-RED-configure]

Set the your gatewayId, your username and password, click Ok and deploy the flow.

If everything correctly configured, you will see the boiler data in the debug tab.

Ensure that the MQTT broker is running and the MQTT node is configured for Home-Assistant.

### Python way's

This Python script gets the data from the gas boiler system via the Elco Remocon-Net cloud service.

The data will be published via MQTT.

You can use this script on a standalone server, I never try it directly Home Assistant server.

#### Requirements

Install Python3 requirements

```bash
pip3 install -r requirements.txt
```

#### Configuration

Rename or copy [default.example](default.example) to `default.cfg` and adapt it to your configuration

```bash
python3 ./remocon2mqtt.py
```

It not a service but just a script, you have to schedule it via a crontab for instance.


## Home Assistant side

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

### Home Assistant dashboard

I build a simple dashboard with the following 3 cards definition:

To display the room temperature, the desired temperature, the operation mode and the heating status.

Just copy the [yaml](home-assistant/room_temperature.yaml) and paste it in `Manual card`.

```yaml:home-assistant/room_temperature.yaml

```

To display the domestic hot water temperature, just copy the [yaml](home-assistant/domestic_hot_water.yaml) and paste it in `Manual card`.

```yaml:home-assistant/domestic_hot_water.yaml

```

And finally to display the boiler status, just copy the [yaml](home-assistant/boiler_status.yaml) and paste it in `Manual card`.

```yaml:home-assistant/boiler_status.yaml

```

## Limitation

I'ts a readonly integration, we can't modify set-point or any parameters on the boiler.

## License

[MIT](LICENSE)

[img1]: images/home-assistant-card.png
[node-RED-flow]: images/node-RED-flow.png
[node-RED-manage-palette]: images/node-RED-manage-palette.png
[node-red-contrib-credentials]: images/node-red-contrib-credentials.png
[node-RED-import]: images/node-RED-import.png
[node-RED-configure]: images/node-RED-configure.png