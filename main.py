import websocket
import time
import json
import os
import subprocess
import requests


DHT_ADDRESS = "localhost:3000"

def turn(ws, topic_name, topic_uuid, on):

    command = {
        "timestamp": time.time(),
        "command": {
            "command_type": "turn_command",
            "value": {
                "topic_name": topic_name,
                "topic_uuid": topic_uuid,
                "desired_state": on
            }
        }
    }

    ws_req = {
        "RequestPubMessage":
            {
                "value": command
             }
    }

    ws.send(json.dumps(ws_req))


def get_lights_of_room(area_name):
    to_ret = []
    are_lights_on = False

    try:
        ret = requests.get("http://" + DHT_ADDRESS + "/topic_name/domo_light")
        if ret.status_code == 200:
            lights = ret.json()

            for light in lights:

                if light["value"]["area_name"] == area_name:

                    to_ret.append(light["topic_uuid"])

                    if light["value"]["status"] == 1:
                        are_lights_on = True
            return (to_ret, are_lights_on)
    except e:
        print("Error while retrieving lights")
        return []


def on_message(ws, message):

    json_message = json.loads(message)
    if "Persistent" in json_message:
        json_message = json_message["Persistent"]
        if json_message["topic_name"] in ["domo_bistable_button", "domo_pir_sensor"]:
            print("BISTABLE BUTTON CHANGED STATE")
            area_name = json_message["value"]["area_name"]
            (lights, are_lights_on) = get_lights_of_room(area_name)
            show_string = "off"

            if are_lights_on == False:
                show_string = "on"

            if are_lights_on == True:
                show_string = "off"

            print("TURN LIGHTS " + show_string)
            for light in lights:
                turn(ws, "domo_light", light, not are_lights_on)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")


def on_open(ws):
    print("### Connection established ###")


ws = websocket.WebSocketApp("ws://"+ DHT_ADDRESS + "/ws",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

ws.run_forever()
