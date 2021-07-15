import threading

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

submarines = []
ENTRY = "Earth"
CHANNEL = "the_guide"

pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-3c8ccfa0-c198-4866-a8e8-c73e0b1ca4b2"
pnconfig.subscribe_key = "sub-c-47ff26b0-e48d-11eb-b69b-aa8f176933f4"
pnconfig.uuid = "sec-c-NDU5MTYyMDQtYTliZS00YTgyLWE0NTMtODlmNDg5MjFlYTJj"

pubnub = PubNub(pnconfig)


def run_publisher(message):
    """
    This method is used to publish messages to the 
    submarines.
    """
    the_message = {"entry": ENTRY, "update": message}
    envelope = pubnub.publish().channel(CHANNEL).message(the_message).sync()

    if envelope.status.is_error():
        print("[PUBLISH: fail]")
        print("error: %s" % envelope.status.error)
    else:
        print("[PUBLISH: sent]")
        print("timetoken: %s" % envelope.result.timetoken)


@app.route("/submarines", methods=['GET'])
def get_submarines():
    """
    This method is used to fetch the list of the 
    registered submarines
    """
    return jsonify({'submarines': submarines}), 200


@app.route("/add_sub", methods=['POST', 'GET'])
def add_submarine():
    """
    This method is used to add submarines to its 
    registered submarines list
    """
    submarine_name = request.form.get('name')
    if submarine_name not in submarines:
        submarines.append(submarine_name)
    else:
        raise Exception()
    return jsonify({
        'submarine_name': submarine_name, 'status': "added"
    }), 200


@app.route("/message", methods=['POST', 'GET'])
def send_message():
    submarine_name = request.form.get("sub_name")
    message = request.form.get("message")
    if submarine_name in submarines:
        run_publisher(message)
        if "hide" in message:
            submarines.remove(submarine_name)
    else:
        raise Exception()
    return jsonify({
        'submarine_name': submarine_name, 'status': "published"
    }), 200

