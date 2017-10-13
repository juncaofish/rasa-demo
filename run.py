# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
from rasa_dm.agent import Agent
from rasa_dm.domain import TemplateDomain
from rasa_dm.tracker_store import InMemoryTrackerStore
from rasa_dm.channels.rest import HttpInputChannel
from rasa_dm.channels.console import ConsoleInputChannel

from vacation.policy import SimplePolicy
from vacation.restfulbot import TripBotInput
from vacation.interpreter import NERInterpreter

logger = logging.getLogger(__name__)


def run_vacation(serve_forever=True, debug=False, port=9000):
    vacation_domain = TemplateDomain.load("vacation/vacation_domain.yml")
    chat_endpoint = TripBotInput()
    if debug:
        input_channel = ConsoleInputChannel()
    else:
        input_channel = HttpInputChannel(port, "/ai", chat_endpoint)
    tracker_store = InMemoryTrackerStore(vacation_domain)
    agent = Agent(
        vacation_domain,
        policies=[SimplePolicy()],
        interpreter=NERInterpreter(),
        tracker_store=tracker_store)

    if serve_forever:
        agent.handle_channel(input_channel)
    return agent


if __name__ == '__main__':
    logging.basicConfig(level="DEBUG")
    parser = argparse.ArgumentParser(
            prog='This project is used for demonstration of vacation order by interacting with AI customer service.')
    parser.add_argument('--debug', type=bool, default=False, help='debug flag')
    parser.add_argument('--port',  type=int, default=9000, help='web service port, default:9000')
    args = parser.parse_args()
    run_vacation(debug=args.debug, port=args.port)
