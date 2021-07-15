import os

import requests
from flask import Flask
from flask import request
from flask import jsonify


from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

app = Flask(__name__)

ENTRY = "Earth"
CHANNEL = "the_guide"
SUB_STATUS = "show"

pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-3c8ccfa0-c198-4866-a8e8-c73e0b1ca4b2"
pnconfig.subscribe_key = "sub-c-47ff26b0-e48d-11eb-b69b-aa8f176933f4"
pnconfig.uuid = "sec-c-NDU5MTYyMDQtYTliZS00YTgyLWE0NTMtODlmNDg5MjFlYTJj"

pubnub = PubNub(pnconfig)


class MySubscribeCallback(SubscribeCallback):

  def presence(self, pubnub, event):
    print("[PRESENCE: {}]".format(event.event))
    print("uuid: {}, channel: {}".format(event.uuid, event.channel))

  def status(self, pubnub, event):
    if event.category == PNStatusCategory.PNConnectedCategory:
      print("[STATUS: PNConnectedCategory]")
      print("connected to channels: {}".format(event.affected_channels))

  def message(self, pubnub, event):
    print("[MESSAGE received]")

    if event.message["update"] == "42":
      print("The publisher has ended the session.")
      os._exit(0)
    else:
      print("{}: {}".format(event.message["entry"], event.message["update"]))

@app.route("/register_submarine/<sub_name>", methods=['GET'])
def register_submarine(sub_name=''):
    """
    This method is used to register submarines at control centre
    """
    response = requests.post('http://127.0.0.1:5000/add_sub', data={"name": sub_name})
    if response.status_code == 200:
        return jsonify({
            'submarine_name': sub_name , 'status': "registered"
        }), 200
    else:
        return jsonify({
            'submarine_name': sub_name , 'status': "already_registered"
        }), 200


pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(CHANNEL).with_presence().execute()

