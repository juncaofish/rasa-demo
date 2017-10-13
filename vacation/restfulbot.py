from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import json
from flask import Blueprint, request, jsonify

from rasa_dm.channels.channel import UserMessage, OutputChannel
from rasa_dm.channels.rest import HttpInputComponent

logger = logging.getLogger(__name__)


class RestTripBot(OutputChannel):
    """A bot that uses rest to communicate."""

    def __init__(self):
        self.message = jsonify({"status": -1})

    def send_text_message(self, recipient_id, elements):
        self.message = jsonify({"status": recipient_id, "result": elements})


class TripBotInput(HttpInputComponent):
    """Http input for trip bot."""

    def __init__(self):
        pass

    def blueprint(self, on_new_message):

        tripbot = Blueprint('tripbot', __name__)

        @tripbot.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @tripbot.route("/tripbot", methods=['GET', 'POST'])
        def chat():
            if request.method == 'GET':
                return jsonify({"status": "ok"})
            if request.method == 'POST':
                output = request.stream.read()
                uid = request.args.get("uid", "default")
                output = json.loads(output)
                output_chanel = RestTripBot()
                on_new_message(UserMessage(output["text"], output_chanel, uid))
                return output_chanel.message
        return tripbot
